with arcpy.da.UpdateCursor('钻孔点合并_Dissolve',['MAX_层号','CONCATENATE_岩土名称','CONCATENATE_岩土颜色','所有分层信息','钻孔编号']) as cursor:
    for row in cursor:
        yantu_list = row[1].split(';')
        #print(yantu_list)
        houdu_list = row[2].split(';')
        #print(houdu_list)
        all_ceng = []
        for ceng in range(row[0]):
            ceng_ID = ceng + 1            
            yantu_name = yantu_list[ceng]
            houdu = houdu_list[ceng]
            this_ceng = '{}层：{}（{}）'.format(ceng_ID,yantu_name,houdu)
            all_ceng.append(this_ceng)
        new_field = row[4]
        for c in all_ceng:
            new_field = '{}\n{}'.format(new_field,c)
        print(new_field)
        row[3] = new_field
        cursor.updateRow(row)
    print('finish!')
