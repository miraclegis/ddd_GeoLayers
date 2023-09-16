import random
import datetime

workspace = r'K:\GIS\Projects\ThreeD_GeoLayers\Data\溶洞库.gdb'
excel_in = r'K:\GIS\Projects\ThreeD_GeoLayers\郭君海\溶洞位置202309.xlsx'
table_in = workspace + r'\溶洞列表'

# 查看多面体的高度
def check_multi_patch_height(input_feature_class):
    with arcpy.da.UpdateCursor(input_feature_class, ["SHAPE@"]) as cursor:
        z_list = []
        for row in cursor:
            partID = 0
            for part in row[0]:
                partID += 1
                # print('面{}:'.format(partID))
                pntID = 0
                for pnt in part: 
                    pntID += 1
                    # print('点{}:{}，其z坐标为{}'.format(pntID,pnt,pnt.z))
                    z_list.append(pnt.z)
        z_max = max(z_list)
        z_min = min(z_list)
        z_max_min = z_max - z_min
        z_value = sum(z_list) / len(z_list)
        # print('最高z值：{}'.format(z_max))
        # print('最低z值：{}'.format(z_min))
        # print('平均z值：{}'.format(z_value))
        # print('本多面体高度为：{:.3}'.format(z_max - z_min))
        return [z_max,z_min,z_max_min,z_value]
        
# 移动到新的xy位置        
def move_multi_patch_to_xy(input_feature_class,new_x,new_y):
    with arcpy.da.UpdateCursor(input_feature_class, ["SHAPE@XY"]) as cursor:
        for row in cursor:
            x = row[0][0]  # 现有X坐标
            y = row[0][1]  # 现有Y坐标
            print('当前x坐标：{}'.format(x))
            print('当前y坐标：{}'.format(y))

            # 在此处修改X、Y和Z坐标，例如：
            row[0] = (new_x,new_y)

            # 更新要素
            cursor.updateRow(row)
            print('移动到{}'.format(row[0]))

arcpy.conversion.ExcelToTable(excel_in , table_in, "溶洞列表", 1, '')
print('溶洞位置excel已导入')


with arcpy.da.SearchCursor(table_in,['OID@','钻孔编号','溶洞类型','X','Y','厚度','中心高度']) as cursor:
    for row in cursor:
        print('当前溶洞为钻孔{}，溶洞类型为{},x:{},y:{},其厚度为{}，中心高度为{}'.format(row[1],row[2],row[3],row[4],row[5],row[6]))
        
        # 随机选一个溶洞形状，复制一份
        ID = random.randint(1, 5)
        print('现在从5个溶洞模型中随机选一个：{}号溶洞多面体'.format(ID))
        rongdong = workspace + r'\溶洞多面体{}'.format(ID)
        rongdong_copy = workspace + r'\溶洞多面体_{}_{}'.format(row[1],row[0])
        if arcpy.Exists(rongdong_copy):
            arcpy.management.Delete(rongdong_copy)
            print('文件已存在，已删除{}'.format(rongdong_copy))
        arcpy.management.CopyFeatures(rongdong, rongdong_copy, '', None, None, None)
        
        # 查询当前随机选中的溶洞形状信息
        z_output = check_multi_patch_height(rongdong_copy)
        z_value = z_output[3]
        print('该溶洞的z_max:{}; z_min:{}; 厚度：{}; 中心高程：{}'.format(z_output[0],z_output[1],z_output[2],z_value))
        
        # 修改溶洞位置
        move_multi_patch_to_xy(rongdong_copy,row[4],row[3])
        arcpy.management.Adjust3DZ(rongdong_copy, "NO_REVERSE", row[6] - z_value, '', '')
        print('------------------------------------------')
print(datetime.datetime.now())
