import unicodecsv as csv
from rest_framework.renderers import BaseRenderer
from six import text_type

from MiniTIP import settings


class CSVRenderer(BaseRenderer):
    media_type = 'text/csv'
    format = 'csv'

    def render(self, data, media_type=None, renderer_context=None):
        if not isinstance(data, list):
            data = [data]

        writer_opts = renderer_context.get('writer_opts', {})
        header = getattr(self, 'header') or renderer_context.get('header', None)
        labels = getattr(self, 'labels') or renderer_context.get('labels', None)

        encoding = renderer_context.get(
            'encoding', settings.DEFAULT_CHARSET
        )

        table = self.tablize(data, header=header, labels=labels)
        csv_buffer = Echo()
        csv_writer = csv.writer(csv_buffer, encoding=encoding, **writer_opts)

        for row in table:
            yield csv_writer.writerow(row)

    def tablize(self, data, header=None, labels=None):
        """
        Convert a list of data into a table.

        If there is a header provided to tablize it will efficiently yield each
        row as needed. If no header is provided, tablize will need to process
        each row in the data in order to construct a complete header. Thus, if
        you have a lot of data and want to stream it, you should probably
        provide a header to the renderer (using the `header` attribute, or via
        the `renderer_context`).
        """
        # Try to pull the header off of the data, if it's not passed in as an
        # argument.
        if not header and hasattr(data, 'header'):
            header = data.header

        if data:
            # First, flatten the data (i.e., convert it to a list of
            # dictionaries that are each exactly one level deep).  The key for
            # each item designates the name of the column that the item will
            # fall into.
            data = self.flatten_data(data)

            # Get the set of all unique headers, and sort them
            # (unless already provided).
            if not header:
                # We don't have to materialize the data generator unless we
                # have to build a header.
                data = tuple(data)
                header_fields = set()
                for item in data:
                    header_fields.update(list(item.keys()))
                header = header_fields

            # Return your "table", with the headers as the first row.
            if labels:
                yield [labels.get(x, x) for x in header]
            else:
                yield header

            # Create a row for each dictionary, filling in columns for which the
            # item has no data with None values.
            for item in data:
                row = [item.get(key, None) for key in header]
                yield row

        elif header:
            # If there's no data but a header was supplied, yield the header.
            if labels:
                yield [labels.get(x, x) for x in header]
            else:
                yield header

        else:
            # Generator will yield nothing if there's no data and no header
            pass

    def flatten_data(self, data):
        for item in data:
            flat_item = self.flatten_item(item)
            yield flat_item

    def flatten_item(self, item):
        if isinstance(item, list):
            flat_item = self.flatten_list(item)
        elif isinstance(item, dict):
            flat_item = self.flatten_dict(item)
        else:
            flat_item = {'': item}

        return flat_item

    def flatten_list(self, flist):
        flat_list = dict()

        for index, item in enumerate(flist):
            flat_item = self.flatten_item(item)
            nested_items = self.nest_flat_items(flat_item)

            for key, nested_item in nested_items.items():
                nested_item = str(nested_item)
                data = (flat_list.get(key) + '\n' + nested_item
                        if flat_list.get(key) else nested_item)
                flat_list.update({key: data})

        return flat_list

    def flatten_dict(self, fdict):
        flat_dict = {}
        for key, item in fdict.items():
            key = text_type(key)
            flat_item = self.flatten_item(item)
            nested_item = self.nest_flat_items(flat_item, key)
            flat_dict.update(nested_item)

        return flat_dict

    @staticmethod
    def nest_flat_items(flat_item, prefix=None):
        level_sep = '.'
        nested_item = {}

        for header, val in flat_item.items():
            nested_header = (
                (level_sep.join([prefix, header]) if header else prefix)
                if prefix else header
            )
            nested_item[nested_header] = val

        return nested_item


class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """

    @staticmethod
    def write(value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value
