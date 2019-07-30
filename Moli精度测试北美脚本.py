# -*- coding:utf-8 -*-
import xlrd, xlwt, xlutils
import requests,json
from xlutils.copy import copy
import time
import datetime

# xsfile = r'./MoliAccurancyData/TestCase5Domain.xls'
xsfile = r'E:\Moli\测试用例\python脚本\Moli精度脚本\Moli精度数据\US\USTestCase5Domain.xls' #北美测试集
# xsfile = r'E:\Moli\测试用例\python脚本\Moli精度脚本\Moli精度数据\IN\TestCase5Domain.xls' #印度测试集
# xsfile = r'E:\Moli\测试用例\python脚本\Moli精度脚本\测试集\线上测试全集\TestCase5Domain.xls' #线上数据全集
# xsfile = r'E:\Moli\测试用例\python脚本\Moli精度脚本\测试集\线上测试全集\TestCase5Domain全集(未筛选上线subintent）.xls' #线上数据全集
workbook = xlrd.open_workbook(xsfile, formatting_info= True,encoding_override='utf-8')
worksheet = workbook.sheet_by_name('TestCase')
cbook = copy(workbook)
csheet = cbook.get_sheet('TestCase')

# 设置字体颜色为红色
style_red = xlwt.XFStyle() #初始化excel全局样式
font_red = xlwt.Font()     #初始化font样式
font_red.colour_index = 2  #为font进行赋值
style_red.font = font_red       #将赋值好的font 传递给excel全局样式


# 设置字体颜色为绿色
style_green = xlwt.XFStyle()
font_green = xlwt.Font()
font_green.colour_index = 50
style_green.font = font_green

# 引入时间戳作为userid
ticks = time.time()



URL = r'http://10.110.147.198:9090/moliAgent/caap/centralcontrol'
row = 2

# 发送请求，并接受返回json串
def request(URL,message):
    payload = {
        "chnl": "pc",
        "isDebug": "true",
        "lan": "en",
        "geo": "US",
        "query": {
            "id": "c6c5f342-2ea1-4c",
            "msg": message,
            "type": "text"
        },
        "timestamp": 1542073217352,
        "userInfo": {
            "chnlUsrId":ticks ,
            "firstName": "",
            "ipAddress": "103.244.59.4",
            "lastName": "",
            "location": "",
            "timeZone": ""
        }
    }
    recieption = requests.post(URL, json=payload).json()
    recieption_statuscode = requests.get(URL, json=payload).status_code
    return recieption, recieption_statuscode

# 逐层判断并获取domain、intent、subintent信息
def rjson(recieption):
    # global recieption_subintent
    # 将接受过来的request返回的参数（元组）中的元素分别取出并使用
    recieption_json = recieption[0]
    recieption_statuscode = recieption[1]
    # 请求失效的异常处理
    if  recieption_statuscode != 200:
        csheet.write(row,13,'请求失败',style_red)
        recieption_domain = "empty"
        recieption_intent = "empty"
        recieption_subintent = "empty"
    # 正常流程下的数据判断及获取
    else:
        if recieption_json.__contains__("data"):
            if recieption_json["data"].__contains__("nluResult"):
                if recieption_json["data"]["nluResult"].__contains__("semanticFrames"):
                    recieption_domain = []
                    recieption_intent = []
                    recieption_subintent = []
                    for i in recieption_json["data"]["nluResult"]["semanticFrames"]:
                        if i.__contains__("domain"):
                            recieption_domain.append(i["domain"]["name"])
                            if i.__contains__("intent"):
                                recieption_intent.append(i["intent"]["code"])
                                if i.__contains__("subintent"):
                                    recieption_subintent.append(i["subintent"]["code"])
                                else:
                                    recieption_subintent = "empty"
                                    csheet.write(row,11,"未找到SubIntentCode", style_red)
                                    print('未找到subintent')
                            else:
                                recieption_intent = "empty"
                                recieption_subintent = "empty"
                                csheet.write(row, 8, "未找到IntentCode", style_red)

                        else:
                            recieption_domain = "empty"
                            recieption_intent = "empty"
                            recieption_subintent = "empty"
                            csheet.write(row, 6, "未找到Domain", style_red)
                else:
                    csheet.write(row, 15, "未找到semanticFrames", style_red)
            else:
                csheet.write(row, 14, "未找到nluResult", style_red)
        else:
            csheet.write(row, 13, "未找到data", style_red)
    return recieption_domain,recieption_intent,recieption_subintent


# 对比domain并写入
def comparison_domain(recieption):
    # 入参为rjson返回的包含三个元素的一个元组对象，需要拆开元组获取需要的对象，下方intent及subintent同理
    pointer = []
    recieption_domain = recieption[0]
    right_domain = worksheet.cell_value(row,5).split('|')
    if recieption_domain != 'empty':
        for j in right_domain:
        # if reflection[worksheet.cell_value(row, 5)] in recieption_domain:
            if reflection[j] in recieption_domain:
                p = True
                pointer.append(p)
                break
            else:
                p = False
                pointer.append(p)
        if True in pointer:
            # "|".join()函数可以将""中的符号作为列表、字符串、元组、字典中的分隔符插入
            csheet.write(row, 6, "|".join(recieption_domain), style_green)
        else:
            csheet.write(row, 6, "|".join(recieption_domain), style_red)
    else:
        print('第',row+1,'行domain为空')


# 对比intent并写入
def comparison_intent(recieption):
    pointer = []
    recieption_intent = recieption[1]
    right_intent = worksheet.cell_value(row,7).split('|')
    if recieption_intent != 'empty':
        for j in right_intent:
            # if reflection[worksheet.cell_value(row, 5)] in recieption_domain:
            if j in recieption_intent:
                p = True
                pointer.append(p)
                break
            else:
                p = False
                pointer.append(p)
        if True in pointer:
            csheet.write(row, 8, "|".join(recieption_intent), style_green)
        else:
            csheet.write(row, 8, "|".join(recieption_intent), style_red)
    else:
        print('第', row + 1, '行intent为空')


# 对比subintent并写入
def comparison_subintent(recieption):
    # 用于返回列表与内容列表是否存在相同项的判断计数
    pointer = []
    recieption_subintent = recieption[2]
    right_subintent = worksheet.cell_value(row,10).split('|')
    if recieption_subintent != 'empty':
        for j in right_subintent:
            # if reflection[worksheet.cell_value(row, 5)] in recieption_domain:
            if j in recieption_subintent:
                p = True
                pointer.append(p)
                break
            else:
                p = False
                pointer.append(p)
        if True in pointer:
            csheet.write(row, 11, "|".join(recieption_subintent), style_green)
            global right_count
            right_count += 1
        else:
            csheet.write(row, 11, "|".join(recieption_subintent), style_red)
            global wrong_count
            wrong_count += 1
    else:
        print('第', row + 1, '行subintent为空')
    return right_count, wrong_count

# 针对domain没有code构建映射键值对
reflection = {'After sale': 'after_sale' , 'fact': 'fact', 'How to': 'how_to', 'Pre sale': 'pre_sale', 'Trouble Shooting': 'trouble_shooting'}
# 循环发送请求，并在控制台打印运行信息

localtime_start = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(localtime_start)
# 用于计算正确及错误subintent数量
right_count = 0
wrong_count = 0

while row < worksheet.nrows:
    csheet.write(row,2,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    message = worksheet.cell_value(row,4)
    return_message = request(URL, message)
    try:
        code = rjson(return_message)
        comparison_domain(code)
        # print(code[0])
        comparison_intent(code)
        # print(code[1])
        a = comparison_subintent(code)
    except:
        csheet.write(row, 12, str(return_message[0]), style_red)
    right_count = a[0]
    wrong_count_count = a[1]
    # print(code[2])
    json_data = return_message[0]
    csheet.write(row, 12, str(json_data))
    # print('当前第', row + 1, '行', '共', worksheet.nrows, '行')
    csheet.write(row, 3, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print(code[0])
    print(code[1])
    print(code[2])
    print('This is the ', row + 1, 'row', 'Totally', worksheet.nrows, 'rows')
    print('-'*40)
    row += 1

# cbook.save(r'./MoliAccurancyResult/AccuracyTestResult.xls')
result = 'Total',worksheet.nrows-2,'rows',right_count,'Pass',wrong_count,'Fail','Accurate Rate is ', '%.2f%%' %(right_count/(worksheet.nrows-2)*100)
csheet.write(row+1,0,result)
cbook.save(r'./Moli精度结果/USAccuracyTestResult.xls') # 北美结果
# cbook.save(r'./Moli精度结果/INAccuracyTestResult.xls') # 印度结果
# cbook.save(r'./Moli精度结果/ALLAccuracyTestResult.xls')
loacaltime_end = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print('Finished',loacaltime_end,'！'*40)
# print('Total',worksheet.nrows-2,'rows',right_count,'Pass',wrong_count,'Fail','Accurate Rate is ', '%.2f%%' %(right_count/(worksheet.nrows-2)*100))
print(result)