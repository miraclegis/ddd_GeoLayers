aprx = arcpy.mp.ArcGISProject("CURRENT")
map = aprx.activeMap
print('当前激活地图为：{}'.format(map.name))


arcpy.env.overwriteOutput = True

# 栅格向外扩展一个像素
def raster_expand_cell(raster_input,raster_output):
    raster_domain_line = 'raster_domain_line'
    raster_domain_polygon = 'raster_domain_polygon'
    raster_domain_line_buffer = 'raster_domain_line_buffer'
    raster_domain_polygon_buffer = 'raster_domain_polygon_buffer'
    aprx = arcpy.mp.ArcGISProject("CURRENT")
    map = aprx.activeMap
    
    
    arcpy.ddd.RasterDomain(raster_input, raster_domain_line, "LINE")
    arcpy.ddd.RasterDomain(raster_input, raster_domain_polygon, "POLYGON")
    
    arcpy.analysis.Buffer(raster_domain_line, raster_domain_line_buffer, "10 Meters", "LEFT", "ROUND", "NONE", None, "PLANAR")
    arcpy.analysis.Buffer(raster_domain_polygon,  raster_domain_polygon_buffer, "10 Meters", "FULL", "ROUND", "ALL", None, "PLANAR")
    
    nibble_raster = arcpy.sa.Nibble(raster_input, raster_input, "DATA_ONLY", "PROCESS_NODATA", None)
    
    out_raster = arcpy.sa.ExtractByMask(nibble_raster, raster_domain_polygon_buffer, "INSIDE", raster_domain_polygon_buffer)
    out_raster.save(raster_output)
    
    layer_to_remove =['raster_domain_polygon_buffer','raster_domain_line_buffer','raster_domain_polygon','raster_domain_line']
    for layer in map.listLayers():
        if layer.name in layer_to_remove:
            map.removeLayer(layer)
    arcpy.management.MakeRasterLayer(raster_output, "DEM_layer_nipple")[0]
    
    
zk_info = r'K:\GIS\Projects\ThreeD_GeoLayers\Data\北区地质体.gdb\北区17个原始钻孔数据和12个延伸钻孔'
TIN_surface = r'K:\GIS\Projects\ThreeD_GeoLayers\Data\北区TIN_surface'
DEM_surface = r'K:\GIS\Projects\ThreeD_GeoLayers\Data\北区地质体.gdb\北区DEM_surface'
DEM_surface_nipple = r'K:\GIS\Projects\ThreeD_GeoLayers\Data\北区地质体.gdb\北区DEM_surface_nipple'
projection_info = 'PROJCS["CGCS2000_3_Degree_GK_CM_117E",GEOGCS["GCS_China_Geodetic_Coordinate_System_2000",DATUM["D_China_2000",SPHEROID["CGCS2000",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Gauss_Kruger"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",117.0],PARAMETER["Scale_Factor",1.0],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]],VERTCS["Yellow_Sea_1985",VDATUM["Yellow_Sea_1985"],PARAMETER["Vertical_Shift",0.0],PARAMETER["Direction",1.0],UNIT["Meter",1.0]];-5123200 -10002100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision'
region = r'K:\GIS\Projects\ThreeD_GeoLayers\Data\北区地质体.gdb\北区边界面_按钻孔重画'

# 地表层生成栅格
# 钻孔点生成TIN（按照边界hard clip），TIN转栅格
arcpy.ddd.CreateTin(TIN_surface, projection_info, r"{} FIRST_层顶高程 Mass_Points <None>;{} <None> Hard_Clip <None>".format(zk_info, region), "DELAUNAY")
print('根据所有钻孔的孔口高程生成地表层的TIN')
arcpy.ddd.TinRaster(TIN_surface, DEM_surface, "FLOAT", "LINEAR", "CELLSIZE", 1, 2) # 栅格分辨率2米
print('地表层的TIN转成栅格，栅格分辨率2米')
raster_expand_cell(DEM_surface,DEM_surface_nipple)
print('地表层栅格外扩一个像素')

        
# DEM_surface_nipple_layer = arcpy.management.MakeRasterLayer(DEM_surface_nipple, "DEM_surface_nipple")[0]
# map.addLayer(DEM_surface_nipple_layer)
print('finish')




arcpy.env.overwriteOutput = True

# 地层生成
layer_number = 1


zk_info = r'K:\GIS\Projects\ThreeD_GeoLayers\Data\北区地质体.gdb\北区17个原始钻孔数据和12个延伸钻孔'
zk_info_layer = r'K:\GIS\Projects\ThreeD_GeoLayers\Data\北区地质体.gdb\北区29个钻孔_layer{:02}'.format(layer_number)
TIN_surface = r'K:\GIS\Projects\ThreeD_GeoLayers\Data\北区TIN_surface'
DEM_surface = r'K:\GIS\Projects\ThreeD_GeoLayers\Data\北区地质体.gdb\北区DEM_surface'
DEM_surface_nipple = r'K:\GIS\Projects\ThreeD_GeoLayers\Data\北区地质体.gdb\北区DEM_surface_nipple'
projection_info = 'PROJCS["CGCS2000_3_Degree_GK_CM_117E",GEOGCS["GCS_China_Geodetic_Coordinate_System_2000",DATUM["D_China_2000",SPHEROID["CGCS2000",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Gauss_Kruger"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",117.0],PARAMETER["Scale_Factor",1.0],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]],VERTCS["Yellow_Sea_1985",VDATUM["Yellow_Sea_1985"],PARAMETER["Vertical_Shift",0.0],PARAMETER["Direction",1.0],UNIT["Meter",1.0]];-5123200 -10002100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision'
region = r'K:\GIS\Projects\ThreeD_GeoLayers\Data\北区地质体.gdb\北区边界面_按钻孔重画'


# 下面的地层层底生成

# 先把有第一层的钻孔从zk_info表中提取出来，生成点文件
arcpy.management.CopyFeatures(zk_info, zk_info_layer, '', None, None, None)

with arcpy.da.UpdateCursor(zk_info_layer,['钻孔编号','COUNT_钻孔编号', 'CONCATENATE_地层编号', 'FIRST_层顶高程', 'CONCATENATE_层顶高程', 'CONCATENATE_层底高程', 'CONCATENATE_层底埋深', 'FIRST_X', 'FIRST_Y','埋深']) as cursor:
    for row in cursor:
        layerID_list = row[2].split(';')
        if str(layer_number) in layerID_list:
            layer_index = layerID_list.index(str(layer_number))
            this_layer_deepth_list = row[6].split(';')
            row[9] = eval(this_layer_deepth_list[layer_index])
            print('发现一个钻孔：{}'.format(row[0]))
            cursor.updateRow(row)
        else:
            cursor.deleteRow()
            print('删掉一个钻孔：{}'.format(row[0]))        


workspace = r'K:\GIS\Projects\ThreeD_GeoLayers\Data\北区地质体.gdb'
arcpy.management.CreateFeatureclass(workspace, '北区Layer{:02}_extent'.format(layer_number), "POLYGON", None, "DISABLED", "DISABLED", 'PROJCS["CGCS2000_3_Degree_GK_CM_117E",GEOGCS["GCS_China_Geodetic_Coordinate_System_2000",DATUM["D_China_2000",SPHEROID["CGCS2000",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Gauss_Kruger"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",117.0],PARAMETER["Scale_Factor",1.0],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]];-5123200 -10002100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision', '', 0, 0, 0, '')
print('创建了一个空的面要素类，现在手动加辅助点，设置辅助点的厚度为0.01')            
# 修改点文件，加上一些辅助点（手动输入厚度为0.01）.手动连线，绘制成本层的边界面

print('finish')



# 根据点生成TIN，其中设置hard clip,根据刚才的边界面
layer_extent = workspace + r'\北区Layer{:02}_extent'.format(layer_number)
TIN_layer = r'K:\GIS\Projects\ThreeD_GeoLayers\Data\北区TIN_layer{:02}_bottom'.format(layer_number)
Deepth_layer = r'K:\GIS\Projects\ThreeD_GeoLayers\Data\北区地质体.gdb\北区Deepth_layer{:02}'.format(layer_number)
DEM_layer = r'K:\GIS\Projects\ThreeD_GeoLayers\Data\北区地质体.gdb\北区DEM_layer{:02}'.format(layer_number)
# DEM_layer_nipple = r'K:\GIS\Projects\ThreeD_GeoLayers\Data\北区地质体.gdb\北区DEM_layer{:02}_nipple'.format(layer_number)
Deepth_layer_nipple = r'K:\GIS\Projects\ThreeD_GeoLayers\Data\北区地质体.gdb\北区Deepth_layer{:02}_nipple'.format(layer_number)
TIN_layer_nipple = r'K:\GIS\Projects\ThreeD_GeoLayers\Data\北区TIN_layer{:02}_bottom_nipple'.format(layer_number)
TIN_surface_nipple = r'K:\GIS\Projects\ThreeD_GeoLayers\Data\北区TIN_surface_nipple'
DEM_surface_extract = r'K:\GIS\Projects\ThreeD_GeoLayers\Data\北区地质体.gdb\北区DEM_surface_extract_layer{:02}'.format(layer_number)
Point_surface_extract = r'K:\GIS\Projects\ThreeD_GeoLayers\Data\北区地质体.gdb\北区Point_surface_extract_layer{:02}'.format(layer_number)
Point_layer = r'K:\GIS\Projects\ThreeD_GeoLayers\Data\北区地质体.gdb\北区Point_layer{:02}'.format(layer_number)

arcpy.env.snapRaster = DEM_surface_nipple
out_multi_patch = r'K:\GIS\Projects\ThreeD_GeoLayers\Data\北区地质体.gdb\北区_GeoLayer_v2_{:02}'.format(layer_number)

arcpy.ddd.CreateTin(TIN_layer, projection_info, r"{} 埋深 Mass_Points <None>;{} <None> Hard_Clip <None>".format(zk_info_layer, layer_extent), "DELAUNAY")
print('根据各个钻孔和辅助点的埋深生成TIN')

# tin转栅格，外扩一个像素
arcpy.ddd.TinRaster(TIN_layer, Deepth_layer, "FLOAT", "LINEAR", "CELLSIZE", 1, 2) # 栅格分辨率2米
print('埋深的TIN转栅格')
raster_expand_cell(Deepth_layer,Deepth_layer_nipple)
print('埋深栅格外扩一个像素')

# 上层栅格和下层栅格都转TIN（检查一下上层栅格和下层栅格的差值是否都大于0？？）

# 层顶栅格
extract_raster = arcpy.sa.ExtractByMask(DEM_surface_nipple, Deepth_layer_nipple, "INSIDE", projection_info)
extract_raster.save(DEM_surface_extract)
arcpy.management.MakeRasterLayer(DEM_surface_extract, "DEM_surface_extract")[0]
print('按照本层范围提取得到本层的层顶栅格')


# 层底栅格
arcpy.ddd.Minus(DEM_surface_extract, Deepth_layer_nipple, DEM_layer)
print('上层底部栅格减去本层深度栅格，得到本层的底底栅格')


# 本层钻孔点和辅助点提取栅格高程，然后再转TIN
arcpy.sa.ExtractMultiValuesToPoints(zk_info_layer, "{} 层底高程;{} 层顶高程".format(DEM_layer,DEM_surface_extract), "NONE")


# 层顶和层底栅格转点，再生成两个TIN

# arcpy.conversion.RasterToPoint(DEM_surface_extract, Point_surface_extract, "Value")
# arcpy.conversion.RasterToPoint(DEM_layer, Point_layer, "Value")
arcpy.ddd.CreateTin(TIN_surface_nipple, projection_info, r"{} 层顶高程 Mass_Points <None>;{} <None> Hard_Clip <None>".format(zk_info_layer, layer_extent), "DELAUNAY")
print('上层的高程栅格转TIN')

arcpy.ddd.CreateTin(TIN_layer_nipple, projection_info, r"{} 层底高程 Mass_Points <None>;{} <None> Hard_Clip <None>".format(zk_info_layer, layer_extent), "DELAUNAY")
print('本层的底层高程栅格转TIN')

# 两个TIN拉伸得到体
if arcpy.Exists(out_multi_patch):
    arcpy.management.Delete(out_multi_patch)
    print('文件已存在，已删除{}'.format(out_multi_patch))
arcpy.ddd.ExtrudeBetween(TIN_surface_nipple, TIN_layer_nipple, layer_extent, out_multi_patch)
print('两个TIN之间拉伸得到多面体')
arcpy.ddd.IsClosed3D(out_multi_patch)
print('finish')
