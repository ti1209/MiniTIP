from collections import OrderedDict
from copy import deepcopy

from django.utils.encoding import force_text
from rest_framework import serializers
from rest_framework.fields import empty

from common.filter.filters import StringFilter


class DataTableSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance, data, **kwargs)
        self._is_fields_serialize = False

    @property
    def is_fields_serialize(self):
        return self._is_fields_serialize

    @is_fields_serialize.setter
    def is_fields_serialize(self, is_serialize):
        self._is_fields_serialize = is_serialize

    @property
    def metadata_info(self):
        serializer_class = self.__class__
        return self.get_metadata_info(serializer_class)

    @property
    def datatable_fields(self):
        metadata_info = self.metadata_info
        # print(dict(self.get_datatable_fields(metadata_info)))
        return self.get_datatable_fields(metadata_info)

    @property
    def filterable_fields(self):
        metadata_info = self.metadata_info
        return self.get_filterable_fields(metadata_info)

    @property
    def exportable_fields(self):
        metadata_info = self.metadata_info
        return self.get_exportable_fields(metadata_info)

    def get_datatable_fields(self, metadata_info):
        datatable_fields = OrderedDict()

        for key, info in metadata_info.items():
            datatable_field = OrderedDict()

            children = info.get('children')
            child_field_key = info.get('child_field')

            if children:
                child_fields = self.get_datatable_fields(children)
                for child_key, child_field in child_fields.items():
                    source = '__'.join([info['source'], child_key])
                    child_field['data'] = key
                    child_field['child_field'] = child_key
                    child_field['class'] = source
                    child_field['source'] = source

                    sub_key = '.'.join([key, child_key])
                    child_field['name'] = sub_key
                    datatable_fields[sub_key] = child_field

            if info['visible']:
                datatable_field['data'] = key
                datatable_field['name'] = key
                datatable_field['source'] = info['source']
                datatable_field['class'] = info['source']
                datatable_field['title'] = info['label']
                datatable_field['only_multi_tenant'] = info['only_multi_tenant']

                orderable = info.get('orderable')
                filterable = info.get('filterable')

                if orderable is False:
                    datatable_field['orderable'] = False

                if filterable is False:
                    datatable_field['searchable'] = False

                if child_field_key:
                    key = '.'.join([key, child_field_key])
                    datatable_field['name'] = key
                    datatable_field['child_field'] = child_field_key

                datatable_fields[key] = datatable_field

        return datatable_fields

    def get_filterable_fields(self, metadata_info):
        filterable_fields = OrderedDict()

        for key, info in metadata_info.items():
            filterable_field = OrderedDict()

            source = info['source']
            children = info.get('children')
            child_field_key = info.get('child_field')
            only_multi_tenant = info.get('only_multi_tenant')

            if children:
                child_fields = self.get_filterable_fields(children)
                for child_key, child_field in child_fields.items():
                    sub_key = '.'.join([key, child_key])
                    source = '__'.join([source, child_field['source']])
                    child_field['source'] = source
                    filterable_fields[sub_key] = child_field

            if info.get('filterable'):
                filter_class = info.get('filter_class')
                dt_filter = filter_class()

                if self.is_fields_serialize:
                    filterable_field['filter_options'] = [
                        {
                            'option_name': filter_option.option_name,
                            'verbose_name': filter_option.verbose_name,
                            'is_nullable': filter_option.is_nullable
                        }
                        for filter_option in dt_filter.filter_options.values()
                    ]

                else:
                    filterable_field['filter_class'] = info['filter_class']

                if child_field_key:
                    key = '.'.join([key, child_field_key])

                verbose_name = info.get('label')
                filter_type = filter_class.filter_type
                filterable_field['source'] = source
                filterable_field['filter_type'] = filter_type
                filterable_field['verbose_name'] = verbose_name
                filterable_field['only_multi_tenant'] = only_multi_tenant
                filterable_fields[key] = filterable_field

        return filterable_fields

    def get_exportable_fields(self, metadata_info):
        exportable_fields = OrderedDict()

        for key, info in metadata_info.items():
            exportable_field = OrderedDict()

            verbose_name = info.get('label')
            children = info.get('children')
            child_field_key = info.get('child_field')
            only_multi_tenant = info.get('only_multi_tenant')

            exportable_field['verbose_name'] = verbose_name
            exportable_field['only_multi_tenant'] = only_multi_tenant

            if children:
                child_fields = self.get_exportable_fields(children)
                for child_key, child_field in child_fields.items():
                    sub_key = '.'.join([key, child_key])
                    exportable_fields[sub_key] = child_field

            elif child_field_key:
                key = '.'.join([key, child_field_key])
                exportable_fields[key] = exportable_field

            if info.get('exportable'):
                exportable_fields[key] = exportable_field

        return exportable_fields

    def get_metadata_info(self, serializer_class,
                          parent_key=str(), parent_source=str()):
        metadata_info = OrderedDict()
        meta_class = getattr(serializer_class, 'Meta')
        serializer = serializer_class()

        if not isinstance(serializer, DataTableSerializer):
            return metadata_info

        if not hasattr(meta_class, 'metadata'):
            return metadata_info

        metadata = deepcopy(getattr(meta_class, 'metadata'))

        fields = serializer.fields
        for key, field in fields.items():
            if key not in metadata.keys():
                continue

            data = metadata[key]
            source = data['source']

            if parent_key:
                key = '.'.join([parent_key, key])

            if parent_source:
                source = '__'.join([parent_source, source])

            is_base_serializer = hasattr(field, 'fields')

            if is_base_serializer:
                field_class = field.__class__
                sub_metadata = self.get_metadata_info(field_class, key, source)
                metadata_info.update(sub_metadata)

            else:
                data['source'] = source
                metadata_info[key] = self.get_field_info(field, data, key)

        return metadata_info

    def get_field_info(self, field, data, key):
        field_info = OrderedDict()

        assert data.get('source'), (
            "Field({0}) should include a `source` in "
            "metadata of class({1})".format(key, field.__class__)
        )

        source = data['source']
        visible = data.get('visible')
        orderable = data.get('orderable')
        filterable = data.get('filterable')
        exportable = data.get('exportable')
        filter_class = data.get('filter_class')
        child_field = data.get('child_field')
        only_multi_tenant = data.get('only_multi_tenant')

        is_related_field = isinstance(field, serializers.ManyRelatedField)
        is_list_serializer = isinstance(field, serializers.ListSerializer)

        if is_related_field:
            assert child_field, (
                "ManyRelatedField({0}) should include a `child_field` in "
                "metadata of class({1})".format(key, field.parent.__class__)
            )
            field_info['child_field'] = child_field
            source = '__'.join([source, child_field])

        elif is_list_serializer:
            if child_field:
                field_info['child_field'] = child_field
                source = '__'.join([source, child_field])

            else:
                visible = False
                orderable = False
                filterable = False
                exportable = False
                filter_class = None

                field_class = field.child.__class__
                child_metadata = self.get_metadata_info(field_class)

                if child_metadata:
                    field_info['children'] = child_metadata

        field_info['source'] = source
        field_info['visible'] = True if visible is None else visible
        field_info['orderable'] = True if orderable is None else orderable
        field_info['exportable'] = True if exportable is None else exportable
        field_info['only_multi_tenant'] = only_multi_tenant or False

        field_info['filterable'] = filterable
        field_info['filter_class'] = filter_class

        if filterable and not filter_class:
            field_info['filter_class'] = StringFilter

        elif not filterable and filter_class:
            field_info['filterable'] = True

        fields_attrs = (
            'label',
            'read_only',
            'write_only',
            'help_text',
            'min_length',
            'max_length',
            'min_value',
            'max_value',
        )

        for attr in fields_attrs:
            value = getattr(field, attr, None)
            if value is not None and value is not "":
                field_info[attr] = value

        if hasattr(field, 'choices'):
            field_info['choices'] = [
                {
                    'value': choice_value,
                    'verbose_name': force_text(choice_name, strings_only=True)
                }
                for choice_value, choice_name in field.choices.items()
            ]

        return field_info
