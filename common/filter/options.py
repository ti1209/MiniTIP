from datetime import timedelta

from django.db.models import Q

from common.datetime import str_to_datetime


class FilterOption:
    def __init__(self):
        self.option_name = getattr(self, 'option_name')
        self.option_lookup = getattr(self, 'option_lookup')
        self.verbose_name = getattr(self, 'verbose_name')
        self.separator = '__'

    def __call__(self, field_source, filter_value):
        NotImplementedError(
            'FilterOption:{0} - "__call__" method is not implemented'.format(
                self.__class__
            )
        )


class ContainsOption(FilterOption):
    option_name = 'contain'
    option_lookup = 'icontains'
    verbose_name = 'Contains'
    is_nullable = False

    def __call__(self, field_source, filter_value):
        field_source = self.separator.join([field_source, self.option_lookup])
        return Q(**{field_source: filter_value})


class NotContainOption(FilterOption):
    option_name = '!contain'
    option_lookup = 'icontains'
    verbose_name = 'Dose Not Contain'
    is_nullable = False

    def __call__(self, field_source, filter_value):
        field_source = self.separator.join([field_source, self.option_lookup])
        return ~Q(**{field_source: filter_value})


class BeginsOption(FilterOption):
    option_name = 'begin'
    option_lookup = 'istartswith'
    verbose_name = 'Begins With'
    is_nullable = False

    def __call__(self, field_source, filter_value):
        field_source = self.separator.join([field_source, self.option_lookup])
        return Q(**{field_source: filter_value})


class NotBeginOption(FilterOption):
    option_name = '!begin'
    option_lookup = 'istartswith'
    verbose_name = 'Dose Not Begin With'
    is_nullable = False

    def __call__(self, field_source, filter_value):
        field_source = self.separator.join([field_source, self.option_lookup])
        return ~Q(**{field_source: filter_value})


class EndsOption(FilterOption):
    option_name = 'end'
    option_lookup = 'iendswith'
    verbose_name = 'Ends With'
    is_nullable = False

    def __call__(self, field_source, filter_value):
        field_source = self.separator.join([field_source, self.option_lookup])
        return Q(**{field_source: filter_value})


class NotEndOption(FilterOption):
    option_name = '!end'
    option_lookup = 'iendswith'
    verbose_name = 'Dose Not End With'
    is_nullable = False

    def __call__(self, field_source, filter_value):
        field_source = self.separator.join([field_source, self.option_lookup])
        return ~Q(**{field_source: filter_value})


class LessThanEqualsOption(FilterOption):
    option_name = 'ilte'
    option_lookup = 'lte'
    verbose_name = 'Less Than Equals'
    is_nullable = False

    def __call__(self, field_source, filter_value):
        field_source = self.separator.join([field_source, self.option_lookup])
        return Q(**{field_source: filter_value})


class GreaterThanEqualsOption(FilterOption):
    option_name = 'igte'
    option_lookup = 'gte'
    verbose_name = 'Greater Than Equals'
    is_nullable = False

    def __call__(self, field_source, filter_value):
        field_source = self.separator.join([field_source, self.option_lookup])
        return Q(**{field_source: filter_value})


class DateRangeOption(FilterOption):
    option_name = 'date_range'
    option_lookup = 'range'
    verbose_name = 'Date Range'
    is_nullable = False

    def __call__(self, field_source, filter_value):
        start_date_string, end_date_string = filter_value.split(' - ')
        start_date = str_to_datetime(start_date_string)
        end_date = str_to_datetime(end_date_string) + timedelta(days=1)

        field_source = self.separator.join([field_source, self.option_lookup])
        return Q(**{field_source: (start_date, end_date)})


class DateEqualsOption(FilterOption):
    option_name = 'date_equal'
    option_lookup = 'date'
    verbose_name = 'Equals'
    is_nullable = False

    def __call__(self, field_source, filter_value):
        field_source = self.separator.join([field_source, self.option_lookup])
        return Q(**{field_source: str_to_datetime(filter_value)})


class NotDateEqualOption(FilterOption):
    option_name = '!date_equal'
    option_lookup = 'date'
    verbose_name = 'Dose Not Equal'
    is_nullable = False

    def __call__(self, field_source, filter_value):
        field_source = self.separator.join([field_source, self.option_lookup])
        return ~Q(**{field_source: str_to_datetime(filter_value)})


class DateLessThanEqualsOption(FilterOption):
    option_name = 'date_lte'
    option_lookup = 'lte'
    verbose_name = 'Less Than Equals'
    is_nullable = False

    def __call__(self, field_source, filter_value):
        field_source = self.separator.join([field_source, self.option_lookup])
        return Q(**{field_source: str_to_datetime(filter_value)})


class DateGreaterThanEqualsOption(FilterOption):
    option_name = 'date_gte'
    option_lookup = 'gte'
    verbose_name = 'Greater Than Equals'
    is_nullable = False

    def __call__(self, field_source, filter_value):
        field_source = self.separator.join([field_source, self.option_lookup])
        return Q(**{field_source: str_to_datetime(filter_value)})


class EqualsOption(FilterOption):
    option_name = 'equal'
    option_lookup = ''
    verbose_name = 'Equals'
    is_nullable = False

    def __call__(self, field_source, filter_value):
        return Q(**{field_source: filter_value})


class NotEqualOption(FilterOption):
    option_name = '!equal'
    option_lookup = ''
    verbose_name = 'Dose Not Eqaul'
    is_nullable = False

    def __call__(self, field_source, filter_value):
        return ~Q(**{field_source: filter_value})


class NullOption(FilterOption):
    option_name = 'null'
    option_lookup = ''
    verbose_name = 'Null'
    is_nullable = True

    def __call__(self, field_source, filter_value):
        return Q(**{field_source: None})


class NotNullOption(FilterOption):
    option_name = '!null'
    option_lookup = ''
    verbose_name = 'Not Null'
    is_nullable = True

    def __call__(self, field_source, filter_value):
        return ~Q(**{field_source: None})


class StringNullOption(FilterOption):
    option_name = 'snull'
    option_lookup = ''
    verbose_name = 'Null'
    is_nullable = True

    def __call__(self, field_source, filter_value):
        return Q(**{field_source: None}) | Q(**{field_source: ""})


class NotStringNullOption(FilterOption):
    option_name = '!snull'
    option_lookup = ''
    verbose_name = 'Not Null'
    is_nullable = True

    def __call__(self, field_source, filter_value):
        return ~Q(**{field_source: None}) & ~Q(**{field_source: ""})


class TrueOption(FilterOption):
    option_name = 'true'
    option_lookup = ''
    verbose_name = 'True'
    is_nullable = True

    def __call__(self, field_source, filter_value):
        return Q(**{field_source: True})


class FalseOption(FilterOption):
    option_name = 'false'
    option_lookup = ''
    verbose_name = 'False'
    is_nullable = True

    def __call__(self, field_source, filter_value):
        return Q(**{field_source: False})


class RegexOption(FilterOption):
    option_name = 'regex'
    option_lookup = 'regex'
    verbose_name = 'Regex'
    is_nullable = False

    def __call__(self, field_source, filter_value):
        field_source = self.separator.join([field_source, self.option_lookup])
        return Q(**{field_source: filter_value})
