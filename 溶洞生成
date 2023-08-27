arcpy.env.overwriteOutput = True

rongdong_ID = 5

rongdong_top = r'K:\GIS\Projects\ThreeD_GeoLayers\Data\溶洞.gdb\溶洞{}_top'.format(rongdong_ID)
rongdong_bottom = r'K:\GIS\Projects\ThreeD_GeoLayers\Data\溶洞.gdb\溶洞{}_bottom'.format(rongdong_ID)
region = r'K:\GIS\Projects\ThreeD_GeoLayers\Data\溶洞.gdb\溶洞{}范围'.format(rongdong_ID)

TIN_top = r'K:\GIS\Projects\ThreeD_GeoLayers\Data\溶洞\TIN_溶洞{}_top'.format(rongdong_ID)
TIN_bottom = r'K:\GIS\Projects\ThreeD_GeoLayers\Data\溶洞\TIN_溶洞{}_bottom'.format(rongdong_ID)

projection_info = 'PROJCS["CGCS2000_3_Degree_GK_CM_117E",GEOGCS["GCS_China_Geodetic_Coordinate_System_2000",DATUM["D_China_2000",SPHEROID["CGCS2000",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Gauss_Kruger"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",117.0],PARAMETER["Scale_Factor",1.0],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]],VERTCS["Yellow_Sea_1985",VDATUM["Yellow_Sea_1985"],PARAMETER["Vertical_Shift",0.0],PARAMETER["Direction",1.0],UNIT["Meter",1.0]];-5123200 -10002100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision'

out_multi_patch = r'K:\GIS\Projects\ThreeD_GeoLayers\Data\溶洞.gdb\溶洞多面体{}'.format(rongdong_ID)

arcpy.ddd.CreateTin(TIN_top, projection_info, "{} Z Mass_Points <None>".format(rongdong_top), "DELAUNAY") # 根据钻孔三维点生成TIN
arcpy.ddd.CreateTin(TIN_bottom, projection_info, "{} Z Mass_Points <None>".format(rongdong_bottom), "DELAUNAY") # 根据钻孔三维点生成TIN
print('溶洞{}的两个TIN已生成'.format(rongdong_ID))

if arcpy.Exists(out_multi_patch):
    arcpy.management.Delete(out_multi_patch)
    print('文件已存在，已删除{}'.format(out_multi_patch))
arcpy.ddd.ExtrudeBetween(TIN_top, TIN_bottom, region, out_multi_patch)
print('溶洞{}多面体已生成'.format(rongdong_ID))
