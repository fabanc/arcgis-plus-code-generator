import arcpy
from openlocationcode import openlocationcode as olc

# https://github.com/google/open-location-code/blob/master/python/openlocationcode_test.py


def check_spatial_reference(feature_class):
    sr = arcpy.Describe(feature_class).spatialReference
    if sr.factoryCode != 4326:
        raise ValueError('The input feature class must be in WHS84 (WKID 4326)')


def validate_plus_code_length(code):

    # Those are the number of digit required from the specifications.
    valid_codes_length = [
        2,  # Level 0
        4,  # Level 1
        6,  # Level 2
        8,  # Level 3
        10,  # Level 4
        11,  # Level 5
        12  # Level 6
    ]

    if code not in valid_codes_length:
        raise ValueError('Valid Plus Code must be one of the following value: {}'.format(
            ', '.join([str(code) for code in valid_codes_length])
        ))


def validate_code_field_length(feature_class, plus_code_field, code_length):
    fields = [field for field in arcpy.ListFields(feature_class) if field.name.lower() == plus_code_field.lower()]
    if fields is None or len(fields) == 0:
        raise Exception('The field {} does not exist'.format(plus_code_field))

    field = fields[0]
    if field.type != 'String':
        raise Exception('The field for plus code must be of type String')

    if field.length < 9:
        raise Exception('The field {} must at the minimum have a length of 9'.format(plus_code_field))

    if field.length < (code_length + 1):
        raise Exception('The field {} is not long enough. Field Length: {} - Plus Code Length: {} - Plus Code Length Required: {}'.format(
            field.name,
            field.length,
            code_length,
            code_length + 1
        ))


def generate_plus_code(feature_class, plus_code_field, code_length):
    """
    Generate the plus code based on a input feature class. The centroid of the geometry is used.

    :param feature_class: The input feature class. The EPSG must be 4326
    :param plus_code_field: The field that will contain the plus codes.
    :param code_length: The maximum length for the plus code.
    :return:
    """

    # Make sure that the input feature class is in the appropriate format.
    check_spatial_reference(feature_class)

    # Validate that the plus code is a valid value
    validate_plus_code_length(code_length)

    # Validate the field is long enough to accomodate the code.
    validate_code_field_length(feature_class, plus_code_field, code_length)

    count = 0
    with arcpy.da.UpdateCursor(feature_class, ['SHAPE@XY', plus_code_field, 'OID@']) as input_cursor:
        for input_row in input_cursor:

            oid = input_row[-1]
            count += 1

            if count % 100000 == 0:
                arcpy.AddMessage('Processed {} rows so far ...'.format(count))

            try:
                longitude = input_row[0][0]
                latitude = input_row[0][1]
                plus_code = olc.encode(latitude, longitude, code_length)
                input_row[1] = plus_code
                input_cursor.updateRow(input_row)
            except Exception as ex:
                arcpy.AddWarning(
                    'Something went wrong with feature OID: {} - Error Message: {}'.format(oid, ex.message)
                )


if __name__ == '__main__':
    input_feature_class = arcpy.GetParameterAsText(0)
    output_plus_code_field = arcpy.GetParameterAsText(1)
    output_code_length = int(arcpy.GetParameterAsText(2))
    try:
        generate_plus_code(input_feature_class, output_plus_code_field, output_code_length)
    except Exception as ex:
        arcpy.AddError(ex)

