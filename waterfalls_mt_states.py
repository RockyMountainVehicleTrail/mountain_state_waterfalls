"""
Combine all the waterfals from the mountain states
The waterfall data comes from the USGS National Map Hydrography data
code 487 is the code for waterfalls.
"""

import arcpy
import os
from arcgis_helper import print_fields, clone_fc

waterfall_fc = 'waterfalls_mt'
sr = arcpy.SpatialReference('Projected Coordinate Systems/UTM/BLM (US Feet)/NAD 1983 BLM Zone 12N (US Feet)')

arcpy.env.workspace = 'C:\\Users\\Mark\\Documents\\ArcGIS\\Projects\\MyProject1\\MyProject1.gdb'

base_dir = 'C:\\Users\\Mark\\Documents\\tnmp'

file_list = []
file_dir_list = []
file_dir_set = set()
walk = arcpy.da.Walk(base_dir, datatype="FeatureClass", type="Point")

for dirpath, dirnames, filenames in walk:
    for filename in filenames:
        if 'NHD' in dirpath:
            print(dirpath, dirnames, filenames)
            if 'NHDPoint' in filenames:
                file_dir_list.append([dirpath, 'NHDPoint'])
                file_list.append(filenames)
                file_dir_set.add(os.path.join(dirpath, 'NHDPoint'))

wfields = print_fields(next(iter(file_dir_set)))
wfields.append('SHAPE@')
ins_cur = arcpy.da.InsertCursor(waterfall_fc, wfields)
for fgdb in file_dir_set:
    search_cur = arcpy.da.SearchCursor(fgdb, wfields)
    for pt in search_cur:
        if pt[-3] == 487:
            # print(pt[-5])
            ins_cur.insertRow(pt)
    print(fgdb)
del ins_cur
del search_cur




