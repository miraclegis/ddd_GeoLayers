# 设置环境和初始变量
print('start...')
arcpy.env.overwriteOutput = True
# geo_layers_ID = ['1—0—0', '2—0—0', '2—1—0', '3—0—0', '4—0—0', '5—0—0', '5—0—1', '6—0—0', '6—0—2', '6—1—0', '7—0—0', '7—1—0', '8—0—0', '9—0—0', '10—0—0', '11—0—0', '12—0—0', '13—0—0', '14—0—0', '14—1—0', '15—0—0', '15—0—1', '16—0—0', '17—0—0', '17—1—0', '18—0—0']
# 注意地层顺序要正确，15-0-0在15-0-1之下，17-0-0在17-1-0之下，只有这两个调换下顺序
geo_layers_ID = ['1—0—0', '2—0—0', '3—0—0', '4—0—0', '5—0—0', '6—0—0', '6—0—2', '6—1—0', '7—0—0', '11—0—0', '12—0—0', '13—0—0', '15—0—1', '15—0—0', '17—1—0', '17—0—0', '18—0—0']



# 根据钻孔分层信息表，逐层提取转点，用点创建TIN
for gl in geo_layers_ID: 
    # 输入文件名
    gl_table_input = r"K:\GIS\Projects\ThreeD_GeoLayers\三维地质模型3\三维地质模型3.gdb\南区_分层汇总表"    # 输入的原始数据表
    gl_buffer200_point = r'K:\GIS\Projects\ThreeD_GeoLayers\Data\三维地质体基础数据.gdb\南区边界_buffer200米沿线20个点'  # 南区边界缓冲200米后沿边界等距生成20个点

    # 中间数据名
    gl_table_select = r"K:\GIS\Projects\ThreeD_GeoLayers\三维地质模型3\三维地质模型3.gdb\南区_分层汇总表_TableSelect"   # 选中某一层后输出的表
    gl_table_point = r"K:\GIS\Projects\ThreeD_GeoLayers\三维地质模型3\三维地质模型3.gdb\南区_分层汇总表_XYTableToPoint"  # 根据某一层表输出的点
    gl_table_point_idw = r"K:\GIS\Projects\ThreeD_GeoLayers\三维地质模型3\三维地质模型3.gdb\南区_分层汇总表_XYTableToPoint_IDW"  # 根据某一层表输出的点    
    gl_buffer200_point_extract_value = r"K:\GIS\Projects\ThreeD_GeoLayers\三维地质模型3\三维地质模型3.gdb\南区边界_buffer200米沿线20个点_提取idw值"  # 南区边界缓冲200米后沿边界等距生成20个点，提取idw值后的点
    gl_point_merge = r"K:\GIS\Projects\ThreeD_GeoLayers\三维地质模型3\三维地质模型3.gdb\南区_钻孔点和插值点合并" # 钻孔点和插值点合并
    TIN_output = r"K:\GIS\Projects\ThreeD_GeoLayers\三维地质模型3\南区TIN_{}_bottom".format(gl).replace('—','_') # 根据点转成的TIN
    projection_info = 'PROJCS["CGCS2000_3_Degree_GK_CM_117E",GEOGCS["GCS_China_Geodetic_Coordinate_System_2000",DATUM["D_China_2000",SPHEROID["CGCS2000",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Gauss_Kruger"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",117.0],PARAMETER["Scale_Factor",1.0],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]],VERTCS["Yellow_Sea_1985",VDATUM["Yellow_Sea_1985"],PARAMETER["Vertical_Shift",0.0],PARAMETER["Direction",1.0],UNIT["Meter",1.0]];-5123200 -10002100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision'
    
    # 工具处理步骤
    arcpy.analysis.TableSelect(gl_table_input, gl_table_select, "分层编号 = '{}'".format(gl)) # 从原始大表中选中某一地层的所有钻孔行，输出表
    arcpy.management.XYTableToPoint(gl_table_select, gl_table_point, "Y", "X", "层底高程_m_", projection_info) # 将输出表转成钻孔三维点
    # 每层的钻孔点反距离权重插值，设置环境中的范围为南区边界buffer200米
    with arcpy.EnvManager(extent='13108599.7454716 4307085.2262842 13114286.1947111 4311344.7345985 PROJCS["WGS_1984_Web_Mercator_Auxiliary_Sphere",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Mercator_Auxiliary_Sphere"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",0.0],PARAMETER["Standard_Parallel_1",0.0],PARAMETER["Auxiliary_Sphere_Type",0.0],UNIT["Meter",1.0]]'):
        arcpy.ddd.Idw(gl_table_point, "层底高程_m_", gl_table_point_idw, 8.00, 2, "VARIABLE 12", None)
    arcpy.sa.ExtractValuesToPoints(gl_buffer200_point, gl_table_point_idw, gl_buffer200_point_extract_value, "NONE", "VALUE_ONLY") # idw插值的结果提取到点中
    arcpy.management.CalculateField(gl_buffer200_point_extract_value, "层底高程_m_", "!RASTERVALU!", "PYTHON3", '', "DOUBLE", "NO_ENFORCE_DOMAINS") # 将提取的值赋值到“层底高程”字段中，方便下一步的点合并
    arcpy.management.Merge([gl_buffer200_point_extract_value,gl_table_point], gl_point_merge)
    arcpy.ddd.CreateTin(TIN_output, projection_info, "{} 层底高程_m_ Mass_Points <None>".format(gl_point_merge), "DELAUNAY") # 根据钻孔三维点生成TIN
    print('地层{}的层底TIN已生成'.format(gl))
print('finish...')


# 根据TIN拉伸成多面体
layer_count = len(geo_layers_ID) # 分层的数量，[分层数量 - 1] 才是拉伸的多面体数量
# 输入文件名
region = r'K:\GIS\Projects\ThreeD_GeoLayers\Data\三维地质体基础数据.gdb\南区边界面'

# 第1层地层，上表面使用地形图生成的TIN
in_tin_top = r'K:\GIS\Projects\ThreeD_GeoLayers\三维地质模型3\南区TIN_1_0_0_top'
in_tin_bottom = r'K:\GIS\Projects\ThreeD_GeoLayers\三维地质模型3\南区TIN_1_0_0_bottom'

for i in range(layer_count):   
    # 输出文件名
    out_multi_patch = r'K:\GIS\Projects\ThreeD_GeoLayers\三维地质模型3\三维地质模型3.gdb\南区GeoLayer_{}'.format(geo_layers_ID[i].replace('—','_'))    
    # 两层TIN之间拉伸
    if arcpy.Exists(out_multi_patch):
        arcpy.management.Delete(out_multi_patch)
        print('文件已存在，已删除{}'.format(out_multi_patch))
    arcpy.ddd.ExtrudeBetween(in_tin_top, in_tin_bottom, region, out_multi_patch)
    
    print('输入:\n{}\n{}'.format(in_tin_top,in_tin_bottom))
    print('输出:\n{}'.format(out_multi_patch))
    print('- - - - - - - - - -')
    
    # 输入文件名，最后一层不用输出名字
    if i != layer_count - 1:
        in_tin_top = r'K:\GIS\Projects\ThreeD_GeoLayers\三维地质模型3\南区TIN_{}_bottom'.format(geo_layers_ID[i]).replace('—','_')
        in_tin_bottom = r'K:\GIS\Projects\ThreeD_GeoLayers\三维地质模型3\南区TIN_{}_bottom'.format(geo_layers_ID[i+1]).replace('—','_')    
print('finish...')


# 三维图层样式修改
aprx = arcpy.mp.ArcGISProject('current')
mymap = aprx.listMaps('基础数据地图_3D')[0] 
my_3d_layers = mymap.listLayers('*GeoLayer*')

ddd_layers_styles = [r'K:\GIS\Projects\ThreeD_GeoLayers\Data\三维橙色图层.lyrx', r'K:\GIS\Projects\ThreeD_GeoLayers\Data\三维红色图层.lyrx', r'K:\GIS\Projects\ThreeD_GeoLayers\Data\三维蓝色图层.lyrx', r'K:\GIS\Projects\ThreeD_GeoLayers\Data\三维绿色图层.lyrx']
for i in range(len(my_3d_layers)):
    arcpy.management.ApplySymbologyFromLayer(my_3d_layers[i], ddd_layers_styles[i % 4], None, "DEFAULT")
    print('{}图层颜色设置完毕'.format(my_3d_layers[i]))
print('finish...')



print('finish!')
