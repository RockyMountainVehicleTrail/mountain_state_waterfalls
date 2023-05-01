import arcpy
from arcgis_helper import print_fields, clone_fc

sr = arcpy.SpatialReference('Projected Coordinate Systems/UTM/BLM (US Feet)/NAD 1983 BLM Zone 12N (US Feet)')

arcpy.env.workspace = 'C:\\Users\\Mark\\Documents\\ArcGIS\\Projects\\MyProject1\\MyProject1.gdb'

temp_buff_fc = 'temp_waterfall_buffer'
temp_river_fc = r"C:\Users\Mark\Documents\ArcGIS\Projects\MyProject1\MyProject1.gdb\rivers_mt_temp"

buffer_fc = 'waterfalls_mt_PairwiseBuffer_100R'
buff_fields = print_fields(buffer_fc)
buff_fields.append('SHAPE@')
arcpy.Delete_management(temp_buff_fc)
clone_fc(buffer_fc, temp_buff_fc, arcpy.env.workspace)

river_fc = 'waterfalls_mt_PairwiseDissolveCopyWithin10FtWatefall'
river_fields = print_fields(river_fc)
river_fields.append('SHAPE@')

buff_cur = arcpy.da.SearchCursor(buffer_fc, buff_fields)

count = 0
# can't have 2 insert cursors at the same time so put the results of one into a dictionary
# and then add it to the waterfall feature class later
buff_heigh_dict = {}

for wf_buff in buff_cur:

    # if count > 5:
    #     break
    count = count + 1
    buff_ins_cur = arcpy.da.InsertCursor(temp_buff_fc, buff_fields)
    buff_ins_cur.insertRow(wf_buff)
    del buff_ins_cur
    arcpy.Delete_management(temp_river_fc)
    arcpy.analysis.PairwiseClip(river_fc, temp_buff_fc, temp_river_fc, None)
    num_rivers = int(arcpy.GetCount_management(temp_river_fc).getOutput(0))
    if num_rivers > 1:
        single_river_cur = arcpy.da.SearchCursor(temp_river_fc, river_fields)
        high_point = 0
        low_point = 10000
        for part in single_river_cur.next()[-1]:
            for point in part:
                high_point = max(point.Z, high_point)
                low_point = min(point.Z, low_point)
        print(high_point - low_point)
        buff_heigh_dict[wf_buff[0]] = {'elevation': high_point - low_point,
                                       'num_rivers_in_buffer': num_rivers}
        buff_ins_cur = arcpy.da.UpdateCursor(temp_buff_fc, buff_fields)
        for buff in buff_ins_cur:
            buff_ins_cur.deleteRow()
        # pl = single_river_cur.next()[-1].getPart(0)
        # high_point = 0
        # low_point = 10000
        # for point in pl:
        #     high_point = max(point.Z, high_point)
        #     low_point = min(point.Z, low_point)
        # print(high_point - low_point)
        # buff_heigh_dict[wf_buff[0]] = {'elevation':high_point - low_point,
        #                                'num_rivers_in_buffer': num_rivers}
        # buff_ins_cur = arcpy.da.UpdateCursor(temp_buff_fc, buff_fields)

with open(r'C:\Users\Mark\Downloads\height2.csv', 'w') as ofile:
    for k in buff_heigh_dict.keys():
        ofile.write('{}`{}`{}\n'.format(k, buff_heigh_dict[k]['elevation'],
                                      buff_heigh_dict[k]['num_rivers_in_buffer']))

waterfall_fc = 'waterfalls_mt'
waterfall_fields = print_fields(waterfall_fc)
# wfc = arcpy.da.SearchCursor(waterfall_fc, waterfall_fields)
waterfall_upd_cur = arcpy.da.UpdateCursor(waterfall_fc, waterfall_fields)
for waterfall in waterfall_upd_cur:
    if waterfall[-1] in buff_heigh_dict.keys():
        waterfall[-1] = buff_heigh_dict[waterfall[0]]['elevation'] * 3
        waterfall_upd_cur.updateRow(waterfall)


del waterfall_upd_cur
del single_river_cur
del buff_cur
del buff_ins_cur





# for wf_buff in buff_cur:
#     if count > 5:
#         break
#     count = count + 1
#     buff_ins_cur = arcpy.da.InsertCursor(temp_buff_fc, buff_fields)
#     buff_ins_cur.insertRow(wf_buff)
#     del buff_ins_cur
#     arcpy.Delete_management(temp_river_fc)
#     arcpy.analysis.PairwiseClip(river_fc, temp_buff_fc, temp_river_fc, None)
#     single_river_cur = arcpy.da.SearchCursor(temp_river_fc, river_fields)
#     pl = single_river_cur.next()[-1].getPart(0)
#     high_point = 0
#     low_point = 10000
#     for point in pl:
#         high_point = max(point.Z, high_point)
#         low_point = min(point.Z, low_point)
#     print(high_point - low_point)
#     buff_heigh_dict[wf_buff[0]] = high_point - low_point
#     buff_ins_cur = arcpy.da.UpdateCursor(temp_buff_fc, buff_fields)
#     for buff in buff_ins_cur:
#         buff_ins_cur.deleteRow()









# arcpy.analysis.PairwiseClip(r"Waterfalls\Waterfall_flow_line_with_z", "temp_waterfall_buffer", r"C:\Users\Mark\Documents\ArcGIS\Projects\MyProject1\MyProject1.gdb\Waterfall_flow__PairwiseClip", None)








