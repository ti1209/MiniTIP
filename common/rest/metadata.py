from rest_framework.metadata import BaseMetadata


class Metadata(BaseMetadata):
    def __init__(self):
        self.serializer = None

    def determine_metadata(self, request, view):
        if hasattr(view, 'get_serializer'):
            self.serializer = view.get_serializer()
            self.serializer.is_fields_serialize = True

            metatype = request.GET.get('metatype')

            if metatype == 'datatable':
                return self.serializer.datatable_fields

            elif metatype == 'filterable':
                return self.serializer.filterable_fields
