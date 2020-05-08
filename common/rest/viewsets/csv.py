from rest_framework.response import Response

from common.rest.filters.datatables import DatatableOrder
from common.rest.renderers.csv import CSVRenderer


class CSVViewSet:
    def __init__(self):
        self.filter_queryset = getattr(self, 'filter_queryset')
        self.get_queryset = getattr(self, 'get_queryset')
        self.get_serializer = getattr(self, 'get_serializer')
        self.paginate_queryset = getattr(self, 'paginate_queryset')
        self.get_paginated_response = getattr(self, 'get_paginated_response')

        self.renderer_classes = None

    def csv_export(self, request):
        csv_renderer_class = CSVRenderer

        serializer = self.get_serializer()
        exportable_fields = serializer.exportable_fields
        datatable_fields = serializer.datatable_fields
        dt_order = DatatableOrder(request, datatable_fields)

        profile = request.user.tipconsoleprofile
        is_single_tenant_user = profile.is_single_tenant()
        is_multi_tenant_user = profile.is_multi_tenant()

        csv_renderer_class.header = [
            key for key, field in exportable_fields.items()
            if is_multi_tenant_user or
               (is_single_tenant_user and not field['only_multi_tenant'])
        ]

        csv_renderer_class.labels = {
            key: field.get('verbose_name')
            for key, field in exportable_fields.items()
            if is_multi_tenant_user or
               (is_single_tenant_user and not field['only_multi_tenant'])
        }

        queryset = self.get_queryset()
        getter = request.query_params.get

        columns_option = getter('columns_option')
        filtering_option = getter('filtering_option')
        ordering_option = getter('ordering_option')
        paging_option = getter('paging_option')
        ordering_field = getter('ordering_specify_field')
        ordering_dir = getter('ordering_specify_dir')

        if columns_option == "current":
            csv_fields = exportable_fields.keys()
            columns_order = request.GET.get('columns_order').split(',')
            columns_order = filter(lambda x: x in csv_fields, columns_order)
            csv_renderer_class.header = list(columns_order)

        if filtering_option == "current":
            queryset = self.filter_queryset(queryset)

        order = (
            dt_order.get_order(ordering_field, ordering_dir)
            if ordering_option == "specify"
            else dt_order.get_order()
        )
        queryset = queryset.order_by(order)

        if paging_option == "current":
            queryset = self.paginate_queryset(queryset)

        self.renderer_classes = [csv_renderer_class]
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
