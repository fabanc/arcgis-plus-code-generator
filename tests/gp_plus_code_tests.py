import arcpy
import unittest
import tempfile
import os
import sys

sys.path.append(os.path.abspath('../scripts'))

from scripts import gp_open_location_geocode as gp
from lib import custom_errors


CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')


class ErrorTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.schema = os.path.join(
            CURRENT_FOLDER,
            'data',
            'error_cases_template.xml'
        )

        database_name = 'ErrorCases.gdb'
        cls.file_database = os.path.join(OUTPUT_FOLDER, database_name)
        cls.feature_class = os.path.join(cls.file_database, 'invalid_projection')

        if arcpy.Exists(cls.file_database):
            arcpy.Delete_management(cls.file_database)

        # Create the file geodatabase
        arcpy.management.CreateFileGDB(
            out_folder_path=OUTPUT_FOLDER,
            out_name=database_name
        )

        # Import XML template
        arcpy.management.ImportXMLWorkspaceDocument(
            cls.file_database,
            in_file=cls.schema,
            import_type='SCHEMA_ONLY'
        )

    def test_invalid_projection(self):
        self.assertRaises(ValueError, gp.generate_plus_code, self.feature_class, 'PLUS_CODE', 8)


    def test_field_length_shorter_than_code_length(self):
        feature_class = os.path.join(self.file_database, 'field_length_shorter_than_code_length')
        self.assertRaises(custom_errors.FieldTooShort, gp.generate_plus_code, feature_class, 'PLUS_CODE', 11)

    def test_field_length_too_short(self):
        feature_class = os.path.join(self.file_database, 'field_length_too_short')
        self.assertRaises(custom_errors.FieldTooShort, gp.generate_plus_code, feature_class, 'PLUS_CODE', 4)

    def test_field_invalid_type(self):
        feature_class = os.path.join(self.file_database, 'field_bad_type')
        self.assertRaises(custom_errors.FieldTypeError, gp.generate_plus_code, feature_class, 'PLUS_CODE', 4)

if __name__ == '__main__':
    unittest.main()
