# mountain_state_waterfalls
A project to find all waterfalls in the mountain states and there heights

The first step is to copy all the waterfalls and rivers (Flowlines) to one feature class for each data set.

The idea behind this is that all waterfalls are along a river so if you check the high and low point with a given distance of a waterfall you should be able to approximate it's height.

The hydrography data is not perfectly bound to a state so there is some overlap and the above files will result in duplicate features.
This is accomplished by rivers_mt_states.py and waterfalls_mt_states.py.  I createad the destination feature class manually.

You can run a command similar to below to remove the duplicate features in each feature class.
arcpy.management.DeleteIdentical("rivers_mt_Clip_200R", "permanent_identifier", None, 0)

The river data is quite large so to make it more manageable I manually created a buffer (in ArcGIS Pro) with a 200 foot radius.  I also made buffers of 150 and 100 foot radii.  The methodolgy I am using is not exact however, after spot checking some waterfalls, using the difference between the high and low points in a 100 foot buffer along a river seems a good approximation.  Since the process is automated 150 foot radius is easy to do as well.

The river data does not have a Z value.  ArcGIS has a ready made profile tool that can add this information.  However, it only takes 1000 features at a time.  split_fc.py will split the feature class into multiple feature classes that are under 1000 features.  They can then be submitted to get the profile data.

After obtaining th Z data from the ready built profile tool I performed a pairwise dissolve and then filtered the rivers to only thos within 10 feet of a water fall.

With the river (Flowline) dataset being prepared I ran waterfall_heights.py to estimate the heights of the waterfalls.
