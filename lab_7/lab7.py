import arcpy
arcpy.env.overwriteOutput = True

# assign bands
source = r"D:\博士资料\26 spring\GEOG675\wang-online-GEOG676-SPRING2026\lab_7"
band1 = arcpy.sa.Raster(source + r"\blue.tif")  # blue
band2 = arcpy.sa.Raster(source + r"\green.tif")  # green
band3 = arcpy.sa.Raster(source + r"\red.tif")  # red
band4 = arcpy.sa.Raster(source + r"\nir08.tif")  # NIR
combined = arcpy.CompositeBands_management(
    [band1, band2, band3, band4],
    source + r"\output_combined.tif"
)

# Hillshade
azimuth = 315
altitude = 45
shadows = "NO_SHADOWS"
z_factor = 1
arcpy.ddd.HillShade(
    source + r"\dem_30m.tif",
    source + r"\output_Hillshade.tif",
    azimuth,
    altitude,
    shadows,
    z_factor
)

# Slope
output_measurement = "DEGREE"
z_factor = 1
arcpy.ddd.Slope(
    source + r"\dem_30m.tif",
    source + r"\output_Slop.tif",
    output_measurement,
    z_factor
)

print("success!")