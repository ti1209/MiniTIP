from common.filter import options


class Filter:
    def __init__(self):
        self.filter_options = dict()
        for attr in self.__dir__():
            attr = getattr(self, attr)
            if isinstance(attr, options.FilterOption):
                self.filter_options[attr.option_name] = attr

    def __call__(self, option_name, field_source, filter_value=None):
        filter_option = self.filter_options.get(option_name)
        assert filter_option, 'Invalid filter option: {0}'.format(option_name)
        return filter_option(field_source, filter_value)


class StringFilter(Filter):
    filter_type = 'STR'

    contains_option = options.ContainsOption()
    not_contain_option = options.NotContainOption()
    begins_option = options.BeginsOption()
    not_begin_option = options.NotBeginOption()
    ends_option = options.EndsOption()
    not_end_option = options.NotEndOption()
    equals_option = options.EqualsOption()
    not_equal_option = options.NotEqualOption()
    null_option = options.StringNullOption()
    not_null_option = options.NotStringNullOption()
    regex_option = options.RegexOption()


class IntegerFilter(Filter):
    filter_type = 'INT'

    less_than_equals_option = options.LessThanEqualsOption()
    greater_than_equals_option = options.GreaterThanEqualsOption()
    equals_option = options.EqualsOption()
    not_equal_option = options.NotEqualOption()
    null_option = options.NullOption()
    not_null_option = options.NotNullOption()


class DateFilter(Filter):
    filter_type = 'DT'

    date_range_option = options.DateRangeOption()
    date_equals_option = options.DateEqualsOption()
    not_date_equal_option = options.NotDateEqualOption()
    less_than_eqauls_option = options.DateLessThanEqualsOption()
    greater_than_equals_option = options.DateGreaterThanEqualsOption()
    null_option = options.NullOption()
    not_null_option = options.NotNullOption()


class BooleanFilter(Filter):
    filter_type = 'TF'
    true_option = options.TrueOption()
    false_option = options.FalseOption()
