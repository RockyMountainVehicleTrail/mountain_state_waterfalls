"""
Combine all rivers from the hydrography dataset to one feature class
"""""

import arcpy
import os
from arcgis_helper import print_fields, clone_fc

river_fc = 'rivers_mt'
sr = arcpy.SpatialReference('Projected Coordinate Systems/UTM/BLM (US Feet)/NAD 1983 BLM Zone 12N (US Feet)')

arcpy.env.workspace = 'C:\\Users\\Mark\\Documents\\ArcGIS\\Projects\\MyProject1\\MyProject1.gdb'

base_dir = 'C:\\Users\\Mark\\Documents\\tnmp'

file_list = []
file_dir_list = []
file_dir_set = set()
walk = arcpy.da.Walk(base_dir, datatype="FeatureClass", type="Polyline")

for dirpath, dirnames, filenames in walk:
    for filename in filenames:
        if 'NHD' in dirpath:
            print(dirpath, dirnames, filenames)
            if 'NHDFlowline' in filenames:
                file_dir_list.append([dirpath, 'NHDPoint'])
                file_list.append(filenames)
                file_dir_set.add(os.path.join(dirpath, 'NHDFlowline'))

rfields = print_fields(next(iter(file_dir_set)))
rfields.append('SHAPE@')
ins_cur = arcpy.da.InsertCursor(river_fc, rfields)
for fgdb in file_dir_set:
    search_cur = arcpy.da.SearchCursor(fgdb, rfields)
    for row in search_cur:
        ins_cur.insertRow(row)
    print(fgdb)
del ins_cur
del search_cur



