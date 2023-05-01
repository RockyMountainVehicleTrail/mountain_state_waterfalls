# mountain_state_waterfalls
A project to find all waterfalls in the mountain states and there heights

The first step is to copy all the waterfalls and rivers to one feature class for each data set.

The hydrography data is not bound to a state so there is some overlap and the above files will result in duplicate features.
This is accomplished by rivers_mt_states and waterfalls_mt_states.  I createad the destination feature class manually.

You can run a command like below to remove the duplicate features in each feature class.
arcpy.management.DeleteIdentical("rivers_mt_Clip_200R", "permanent_identifier", None, 0)





