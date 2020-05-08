from collections import OrderedDict

from django.core.paginator import InvalidPage
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.request import Request


class DatatablesMixin:
    def __init__(self):
        self.count = None
        self.total_count = None
        self.is_datatable_request = None

    def get_paginated_response(self, data):
        if not self.is_datatable_request:
            get_paginated_response = getattr(
                super(DatatablesMixin, self),
                'get_paginated_response'
            )
            return get_paginated_response(data)

        return Response(
            OrderedDict([
                ('recordsTotal', self.total_count),
                ('recordsFiltered', self.count),
                ('data', data)
            ])
        )

    @staticmethod
    def get_count_and_total_count(queryset, view):
        if hasattr(view, '_datatables_filtered_count'):
            count = getattr(view, '_datatables_filtered_count')

        else:
            count = queryset.count()

        if hasattr(view, '_datatables_total_count'):
            total_count = getattr(view, '_datatables_total_count')

        else:
            total_count = count

        return count, total_count


class DatatablesPaginationBackend(PageNumberPagination, DatatablesMixin):
    def paginate_queryset(self, queryset, request: Request, view=None):
        if (request.accepted_renderer.format != 'datatables' and
                request.accepted_renderer.format != 'csv'):
            self.is_datatable_request = False

            return (
                super(DatatablesPaginationBackend, self).paginate_queryset(
                    queryset, request, view
                )
            )

        length = request.query_params.get('length')

        if length is None or length == '-1':
            return None

        self.count, self.total_count = self.get_count_and_total_count(
            queryset=queryset, view=view
        )

        self.is_datatable_request = True
        self.page_size_query_param = 'length'

        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        start = int(request.query_params.get('start', 0))
        page_number = int(start / page_size) + 1

        try:
            setattr(self, 'page', paginator.page(page_number))

        except InvalidPage:
            msg = self.invalid_page_message.format(
                page_number=page_number
            )
            raise NotFound(msg)

        setattr(self, 'request', request)

        return list(getattr(self, 'page'))
