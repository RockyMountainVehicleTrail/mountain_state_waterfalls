import arcpy


def clone_fc(in_fc, out_fc, wksp):
    """
    Clones a Feature class
    :param in_fc:
    :param out_fc:
    :param wksp:
    :return:
    """
    desc = arcpy.Describe(in_fc)
    create_fc = arcpy.CreateFeatureclass_management(wksp, out_fc, desc.shapeType,
                                                    spatial_reference=desc.spatialReference)
    in_fields = arcpy.ListFields(in_fc)

    for field in in_fields:
        # print(field)
        if field.name not in ('OBJECTID', 'OBJECTID1', 'SHAPE', 'SHAPE_Length', 'Shape'):
            if field.type == 'String':
                arcpy.AddField_management(create_fc, field.name, field.type, field_length=field.length)
            else:
                arcpy.AddField_management(create_fc, field.name, field.type)


def print_fields(fc, p=True):
    """
    Orginally I made this to print the fields in a feature class.  However I decided to return a list of the fields
    as it makes creating Cursors much easier
    :param fc: input feature class
    :param p: Boolean wether or not to print
    :return: a list of fields in the feature class
    """
    fields = arcpy.ListFields(fc)
    field_list = []
    for field in fields:
        if p:
            print("{0} is a type of {1} with a length of {2}"
                  .format(field.name, field.type, field.length))
        field_list.append(field.name)

    return field_list
