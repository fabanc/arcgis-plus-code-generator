# arcgis-plus-code-generator


# Description

This tool exposes the open location code API create by google and uses it to generate Plus Codes on ArcGIS feature classes. The API documentation is there: https://github.com/google/open-location-code

Detailed information about Plus Codes and the KML Service that Google Provides can be found there: https://grid.plus.codes/

This tool is a side effect of a project I have done for work. I have explored different solutions with FME and QGIS, but this was by far the fastest solution. It can generate plus code on points, and polygon feature classes.

# System Requirements

This tool is developed and tested for ArcGIS Pro. I have tested for ArcGIS Pro 2.7.

Your python environment must be of 3.x (tested with 3.7, but I assume it work with 3.6 too). 

The open location code library for Python must be installed in your python environment. In short
`pip install openlocationcode`. For detailed instructions: https://github.com/google/open-location-code/tree/master/python

# How to use

Use the tool box in ArcGIS Pro. There is built in help in the tool metadata, and the tool is configured to guide you and minimize input errors.

# How to contribute

This tool has been done in rush. Though is works, it does not match my standards or the industry standards in terms of unit testing or documentation.
If you want to help, or have any suggestion, log an issue, and a pull request if you feel bold enough.




