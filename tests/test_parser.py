import os.path
import unittest

from parser.parser import CsvReader, WeekFormatter, Parser

TEST_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'test_files'))

class TestParserTests(unittest.TestCase):

    def test_parses_succeessfully(self):
        reader = CsvReader(os.path.join(TEST_DIR, '3.csv'))
        formatter = WeekFormatter()
        parser = Parser(reader, formatter)
        actual = parser.parse()
        expected = [
            {'square': 9, 'day': 'mon', 'value': 3, 'description': 'third_desc 9'},
            {'square': 9, 'day': 'tue', 'value': 3, 'description': 'third_desc 9'},
            {'square': 4, 'day': 'wed', 'value': 2, 'description': 'third_desc 4'},
            {'double': 4, 'day': 'thu', 'value': 2, 'description': 'third_desc 4'},
            {'double': 2, 'day': 'fri', 'value': 1, 'description': 'third_desc 2'}
        ]
        for dct1, dct2 in zip(expected, actual):
            self.assertDictEqual(dct1, dct2)

if __name__ == '__main__':
    unittest.main()
