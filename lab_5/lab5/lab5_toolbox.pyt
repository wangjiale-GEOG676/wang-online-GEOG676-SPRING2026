# -*- coding: utf-8 -*-

import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Building Proximity"
        self.description = "Determines which buildings on TAMU's campus are near a targeted building"
        self.canRunInBackground = False
        self.category = "Building Tools"

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
            displayName="GDB Folder",
            name="GDBFolder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )
        param1 = arcpy.Parameter(
            displayName="GDB Name",
            name="GDBName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param2 = arcpy.Parameter(
            displayName="Garage CSV File",
            name="GarageCSVFile",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )
        param3 = arcpy.Parameter(
            displayName="Garage Layer Name",
            name="GarageLayerName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param4 = arcpy.Parameter(
            displayName="Campus GDB",
            name="Campus_GDB",
            datatype="DEType",
            parameterType="Required",
            direction="Input"
        )
        param5 = arcpy.Parameter(
            displayName="Buffer Distance",
            name="BufferDistance",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input"
        )

        params = [param0, param1, param2, param3, param4, param5]
        return params
        

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        arcpy.env.overwriteOutput = True

        # -----------------------------
        # Inputs from toolbox params
        # -----------------------------
        folder_path = parameters[0].valueAsText          # GDB folder
        gdb_name = parameters[1].valueAsText             # GDB name, e.g., Test.gdb
        csv_path = parameters[2].valueAsText             # garages.csv
        garage_layer_name = parameters[3].valueAsText    # e.g., Garage_Points
        campus = parameters[4].valueAsText               # Campus.gdb
        buffer_distance = float(parameters[5].value)     # e.g., 150

        # Build GDB path
        gdb_path = folder_path + "\\" + gdb_name

        # Create GDB
        arcpy.CreateFileGDB_management(folder_path, gdb_name)

        # -----------------------------
        # Make XY Event Layer (WGS84)
        # -----------------------------
        garages = arcpy.MakeXYEventLayer_management(
            csv_path, "X", "Y", garage_layer_name,
            arcpy.SpatialReference(4326)  # WGS84
        )

        # Write to GDB
        arcpy.FeatureClassToGeodatabase_conversion(garages, gdb_path)
        garage_points = gdb_path + "\\" + garage_layer_name

        # -----------------------------
        # Copy campus buildings into our GDB
        # (kept consistent with your script)
        # -----------------------------
        buildings_campus = campus + "\\Structures"
        buildings = gdb_path + "\\Buildings"
        arcpy.Copy_management(buildings_campus, buildings)

        # -----------------------------
        # Reproject garages to match buildings
        # -----------------------------
        spatial_ref = arcpy.Describe(buildings).spatialReference
        garage_reproj = gdb_path + "\\Garage_Points_reprojected"
        arcpy.Project_management(garage_points, garage_reproj, spatial_ref)

        # -----------------------------
        # Buffer garages
        # -----------------------------
        garage_buffer = gdb_path + "\\Garage_Points_buffered"
        arcpy.Buffer_analysis(
            garage_reproj,
            garage_buffer,
            "{} Meters".format(buffer_distance)
        )

        # -----------------------------
        # Intersect buffer with buildings
        # -----------------------------
        intersect_out = gdb_path + "\\Garage_Building_Intersection"
        arcpy.Intersect_analysis([garage_buffer, buildings], intersect_out, "ALL")

        # -----------------------------
        # Output CSV to the same folder as the GDB folder
        # -----------------------------
        arcpy.TableToTable_conversion(
            intersect_out,
            folder_path,
            "nearbyBuildings.csv"
        )

        messages.addMessage("Done. Output: " + folder_path + "\\nearbyBuildings.csv")

        return None

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
