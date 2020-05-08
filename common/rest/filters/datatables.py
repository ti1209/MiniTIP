from collections import OrderedDict

from django.db.models import Q
from rest_framework.filters import BaseFilterBackend


class DatatableFilterBackend(BaseFilterBackend):
    def __init__(self):
        self.filterable_fields = None

    def filter_queryset(self, request, queryset, view):
        """
        :param request:
        :param queryset:
        :param view:
        :return:
        """

        if (request.accepted_renderer.format != 'datatables'
                and request.accepted_renderer.format != 'csv'):
            return queryset

        if not request.GET.get('draw'):
            return queryset

        total_count = view.get_queryset().count()
        setattr(view, '_datatables_total_count', total_count)

        serializer = view.get_serializer()
        if not hasattr(serializer, 'datatable_fields'):
            return queryset

        if not hasattr(serializer, 'filterable_fields'):
            return queryset

        datatable_fields = serializer.datatable_fields
        filterable_fields = serializer.filterable_fields

        # if not request.user.tipconsoleprofile.is_multi_tenant():
        #     only_multi_tenant_datatable_fields = list()
        #     only_multi_tenant_filterable_fields = list()
        #
        #     for key, datatable_field in datatable_fields.items():
        #         if datatable_field.get('only_multi_tenant'):
        #             only_multi_tenant_datatable_fields.append(key)
        #
        #     for key, filterable_field in datatable_fields.items():
        #         if filterable_field.get('only_multi_tenant'):
        #             only_multi_tenant_filterable_fields.append(key)
        #
        #     for key in only_multi_tenant_datatable_fields:
        #         datatable_fields.pop(key)
        #
        #     for key in only_multi_tenant_filterable_fields:
        #         filterable_fields.pop(key)

        dt_filter = DatatableFilter(request, filterable_fields)
        dt_order = DatatableOrder(request, datatable_fields)

        all_qs = dt_filter.get_all_queryset_filter()
        qs = all_qs if all_qs else dt_filter.get_queryset_filter()

        if qs:
            queryset = queryset.filter(qs)
            filtered_count = queryset.count()

        else:
            filtered_count = total_count

        setattr(view, '_datatables_filtered_count', filtered_count)

        order = dt_order.get_order()
        queryset = queryset.order_by(order)

        return queryset


class DatatableFilter:
    def __init__(self, request, filterable_fields):
        self.filterable_fields = filterable_fields
        self.getter = request.query_params.get
        self.filtered_fields = self.get_filtered_fields()

    def get_queryset_filter(self):
        q = Q()
        filterable_keys = self.filterable_fields.keys()

        for field_key, field in self.filtered_fields.items():
            if field_key not in filterable_keys:
                raise DatatableFilterFieldNameError(
                    'Invalid field source({0}).'.format(
                        field['field_name']
                    )
                )

            filter_option = field.get('filter_option')
            filter_value = field.get('filter_value')

            filterable_field = self.filterable_fields[field_key]
            field_source = filterable_field['source']
            dt_filter = filterable_field['filter_class']()
            q = q & dt_filter(filter_option, field_source, filter_value)

        return q

    def get_all_queryset_filter(self):
        q = Q()

        filter_value = self.getter('search[value]')
        if not filter_value:
            return q

        for filterable_field in self.filterable_fields.values():
            filter_option = 'contain'
            filter_class = filterable_field['filter_class']

            if filter_class.filter_type == "STR":
                filter_source = filterable_field['source']
                dt_filter = filter_class()
                q = q | dt_filter(filter_option, filter_source, filter_value)

        return q

    def get_filtered_fields(self):
        fields = OrderedDict()

        for i in range(len(self.filterable_fields)):
            col = 'columns[%d][%s]'

            field_key = self.getter(col % (i, 'name'))
            if not field_key:
                continue

            search_col = col % (i, 'search')
            search_value = self.getter('%s[%s]' % (search_col, 'value'))

            if search_value:
                sub_index = search_value.find("+")
                filter_option = search_value[:sub_index]
                filter_value = search_value[sub_index + 1:]

                fields[field_key] = {
                    'filter_option': filter_option,
                    'filter_value': filter_value
                }

        return fields


class DatatableOrder:
    def __init__(self, request, datatable_fields):
        self.datatable_fields = datatable_fields
        self.getter = request.query_params.get

    def get_order(self, field_key=None, order_dir=None):
        col = 'order[0][{0}]'
        column_index = self.getter(col.format('column'))
        order_dir = order_dir or self.getter(col.format('dir'))

        col = 'columns[%s][%s]'
        name = self.getter(col % (column_index, 'name'))
        field_key = field_key or name

        datatable_field = self.datatable_fields.get(field_key)
        source = datatable_field.get('source')

        if not source:
            raise DatatableFilterOrderError(
                'Invalid order option(field_key: {0}).'.format(field_key)
            )

        order = source if order_dir == "asc" else "-" + source

        return order


class DatatableFilterBackendException(Exception):
    pass


class DatatableFilterFieldNameError(DatatableFilterBackendException):
    pass


class DatatableFilterOptionError(DatatableFilterBackendException):
    pass


class DatatableFilterOrderError(DatatableFilterBackendException):
    pass
