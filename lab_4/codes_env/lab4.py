# create a gdb and garage feature
import arcpy

arcpy.env.overwriteOutput = True

# Workspace point to codes_env
arcpy.env.workspace = r'D:\博士资料\26 spring\GEOG675\wang-online-GEOG676-SPRING2026\lab_4\codes_env'

# Lab4 root
folder_path = r'D:\博士资料\26 spring\GEOG675\wang-online-GEOG676-SPRING2026\lab_4'
gdb_name = 'Test.gdb'
gdb_path = folder_path + '\\' + gdb_name

# 创建 GDB
arcpy.CreateFileGDB_management(folder_path, gdb_name)

# 输入 CSV
csv_path = r'D:\博士资料\26 spring\GEOG675\wang-online-GEOG676-SPRING2026\lab_4\data\04\garages.csv'
garage_layer_name = 'Garage_Points'

garages = arcpy.MakeXYEventLayer_management(
    csv_path, 'X', 'Y', garage_layer_name,
    arcpy.SpatialReference(4326)  # WGS84
)

# write GDB
input_layer = garages
arcpy.FeatureClassToGeodatabase_conversion(input_layer, gdb_path)
garage_points = gdb_path + '\\' + garage_layer_name


# open campus gdb, copy building feature to our gdb
campus = r'D:\博士资料\26 spring\GEOG675\wang-online-GEOG676-SPRING2026\lab_4\data\04\Campus.gdb'
buildings_campus = campus + '\\Structures'   
buildings = gdb_path + '\\' + 'Buildings'

arcpy.Copy_management(buildings_campus, buildings)


# Re-Projection
spatial_ref = arcpy.Describe(buildings).spatialReference
arcpy.Project_management(
    garage_points,
    gdb_path + '\\Garage_Points_reprojected',
    spatial_ref
)


# buffer the garages
garageBuffered = arcpy.Buffer_analysis(
    gdb_path + '\\Garage_Points_reprojected',
    gdb_path + '\\Garage_Points_buffered',
    # meters
    "150 Meters"
)


# Intersect our buffer with the buildings
arcpy.Intersect_analysis(
    [garageBuffered, buildings],
    gdb_path + '\\Garage_Building_Intersection',
    'ALL'
)

# output
arcpy.TableToTable_conversion(
    gdb_path + '\\Garage_Building_Intersection',
    r'D:\博士资料\26 spring\GEOG675\wang-online-GEOG676-SPRING2026\lab_4',
    'nearbyBuildings.csv'
)

print("Done. Output:", folder_path + '\\nearbyBuildings.csv')
