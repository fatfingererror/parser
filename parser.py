import re
import csv


class CsvReader:
    def __init__(self, fname):
        self.fname = fname

    def read(self):
        with open(self.fname) as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)
            data = next(reader)
        return zip(headers, data)


class Parser:
    def __init__(self, reader, formatter):
        self.reader = reader
        self.formatter = formatter

    def parse(self):
        """orchestrates parsing by calling the reader and the formatter"""
        raw_data = self.reader.read()
        cleaned_data = self.formatter.format(raw_data)
        return cleaned_data


class WeekFormatter:

    weekdays = ['mon', 'tue', 'wed', 'thu', 'fri']
    weekday_range = 'mon-thu'
    weekday_regex = '|'.join(weekdays)
    weekday_range_regex = re.compile('^({0})-({0})$'.format(weekday_regex))
    allowed_fields = {'description'}

    @staticmethod
    def create_extra_field(day_idx, value):
        if day_idx < 3:
            return {'square': value**2}
        else:
            return {'double': value*2}

    @staticmethod
    def format_day_value(value):
        return int(value)

    @staticmethod
    def format_desc_values(data):
        base_part = data['description']
        numeric_part = data['square'] if 'square' in data else data['double']
        data['description'] = ' '.join([base_part, str(numeric_part)])

    def format(self, raw_data):
        common = {}
        cleaned_data = []
        for header, value in raw_data:
            matched = re.match(self.weekday_range_regex, header)
            if matched:
                start, end = matched.groups()
                start_idx = self.weekdays.index(start)
                end_idx = self.weekdays.index(end)
                for idx in range(start_idx, end_idx+1):
                    dct = {}
                    dct['day'] = self.weekdays[idx]
                    dct['value'] = self.format_day_value(value)
                    dct.update(self.create_extra_field(idx, dct['value']))
                    cleaned_data.append(dct)
            elif header in self.weekdays:
                dct = {}
                dct['day'] = header
                idx = self.weekdays.index(header)
                dct['value'] = self.format_day_value(value)
                dct.update(self.create_extra_field(idx, dct['value']))
                cleaned_data.append(dct)
            elif header in self.allowed_fields:
                common[header] = value
        for data in cleaned_data:
            data.update(common)
            self.format_desc_values(data)
        return cleaned_data
