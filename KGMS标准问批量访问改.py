import xlrd
import xlwt
import requests
import json
import re
import xlutils
from xlutils.copy import copy


xlsfile = r"E:\Moli\测试用例\python脚本\KGMS标准问批量访问脚本\Moli__US\KGMS标准问批量访问数据\Concept_Tree.xls"
# xlsfile = r"E:\Moli\测试用例\python脚本\KGMS标准问批量访问脚本\Moli__US\KGMS标准问批量访问数据\1.xls"
book = xlrd.open_workbook(xlsfile,formatting_info=True)
book_sheet = book.sheet_by_name('Sub intent')

cbook = copy(book)
csheet = cbook.get_sheet('Sub intent')

# 设置单元格样式
pattern_red = xlwt.Pattern()
pattern_red.pattern = xlwt.Pattern.SOLID_PATTERN
pattern_red.pattern_fore_colour = 2
style_red = xlwt.XFStyle()
style_red.pattern = pattern_red


pattern_blue = xlwt.Pattern()
pattern_blue.pattern = xlwt.Pattern.SOLID_PATTERN
pattern_blue.pattern_fore_colour = 4
style_blue = xlwt.XFStyle()
style_blue.pattern = pattern_blue

pattern_pink = xlwt.Pattern()
pattern_pink.pattern = xlwt.Pattern.SOLID_PATTERN
pattern_pink.pattern_fore_colour = 6
style_pink = xlwt.XFStyle()
style_pink.pattern = pattern_pink

pattern_darkred = xlwt.Pattern()
pattern_darkred.pattern = xlwt.Pattern.SOLID_PATTERN
pattern_darkred.pattern_fore_colour = 16
style_darkred = xlwt.XFStyle()
style_darkred.pattern = pattern_darkred



def access_request(URL):
    payload = {
    "chnl": "pc",
    "isDebug": "true",
    "lan": "en",
    "geo":"US",
    "query": {
        "id": "c6c5f342-2ea1-4c",
        "msg": i,
        "type": "text"
    },
    "timestamp": 1542073217352,
    "userInfo": {
        "chnlUsrId": "233f11a6-afa4-4ba2-bdce-3869d5d864",
        "firstName": "",
        "ipAddress": "103.244.59.4",
        "lastName": "",
        "location": "",
        "timeZone": ""
    }
}
    reciept = requests.post(URL, json = payload)
    response_type = reciept.json()['data']['retJSONObject']['messages'][len(reciept.json()['data']['retJSONObject']['messages'])-1]['type']
    return reciept, response_type


# 三列判断时的定义
# def datacompare(a,b,c):
#     if a == b == c:
#         message = {a: 2, 'restart': 0}
#     elif a == b and b != c:
#         message = {a: 2, 'restart': 0, c: 6, 'startover': 0}
#     elif a != b and a == c:
#         message = {a: 2, 'restart': 0, b: 5, 'startover': 0}
#     elif a != b and b == c:
#         message = {a: 2, 'restart': 0, c: 6, 'startover': 0}
#     else:
#         message = {a: 2, 'restart': 0, b: 5, 'startover': 1, c: 6}
#     return message

def datacompare(a,b,c):
    if a == b == c:
        message = {a: 2, 'restart': 0}
    elif a == b and b != c:
        message = {a: 2, 'restart': 0, c: 6, 'startover': 0}
    elif a != b and a == c:
        message = {a: 2, 'restart': 0, b: 5, 'startover': 0}
    elif a != b and b == c:
        message = {a: 2, 'restart': 0, c: 6, 'startover': 0}
    else:
        message = {a: 2, 'restart': 0, b: 5, 'startover': 1, c: 6}
    return message


def comparison(reciept, response_type,i,count_red, count_blue, count_pink, count_darkred):
    try:
        if response_type == payload_type_button:
            response_buttonType = reciept.json()['data']['retJSONObject']['messages'][len(reciept.json()['data']['retJSONObject']['messages']) - 1]['payload'][0]['buttonType']
            if response_buttonType in multi_intent:
                # 推出2007多意图按钮标为红色
                csheet.write(row, message[i], i, style_red)
                count_red += 1
                print(i)
                print('这条case未通过，这是第', row + 1, '行', message[i], '列，共', book_sheet.nrows, '行')
            elif response_buttonType in agent :
                # 推出3001/3002转人工相关按钮标为蓝色
                csheet.write(row, message[i], i, style_blue)
                # count_blue += 1
                print(response_buttonType,'-'*10)
                print(response_type,'-'*10)
                print(reciept.json())
                print(i)
                print('这条case转人工，这是第', row + 1, '行', message[i], '列，共', book_sheet.nrows, '行')
            else:
                print(i)
                print('这是第', row + 1, '行，共', book_sheet.nrows, '行')
        else:
            if reciept.json()['data']['retJSONObject']['vo']['dialogAct'][0]['dialogActID'] not in botActcode:
                # 识别异常（非英语、不理解等标为粉色）
                print(reciept.json()['data']['retJSONObject']['vo']['dialogAct'][0]['dialogActID'])
                print('这是第', row + 1, '行，', i, 'DM返回结果错误，请检查')
                csheet.write(row, message[i], i, style_pink)
                count_pink += 1
            else:
                print(i)
                print('这是第', row + 1, '行，共', book_sheet.nrows, '行')
    except:
        csheet.write(row, message[i], i, style_darkred)
        count_darkred += 1
        print(i)
        print('这是第', row + 1, '行，请求失败，请检查！！！')
    return count_red, count_blue,count_pink, count_darkred
URL = 'http://10.110.147.198:9090/moliAgent/caap/centralcontrol'
row = 1
# 构建多意图按钮列表
multi_intent = ['2007']
payload_type_button = 'button'
payload_type_text = 'text'
# 针对DM不同返回内容构建列表进行排除
botActcode = ['B1119', 'B1521','B1237_os','B1237_rma##imei','B1237_email##phone##imei','B1237_sn##imei']
# 针对人工在线及不在线构建列表进行排查
agent = ['3001', '3002']

# 计数器打印不同类型未通过的数量
count_red = 0
count_blue = 0
count_pink = 0
count_darkred = 0

while row < book_sheet.nrows:
    # 先定义三行数据为a,b,c
    a = book_sheet.cell_value(row, 2)  # subintent
    b = book_sheet.cell_value(row, 5)  # facebookbutton name
    c = book_sheet.cell_value(row, 6)  # answer title name
    message = datacompare(a,b,c)
    for i in message:
        reciept, response_type = access_request(URL)
        count_red, count_blue, count_pink, count_darkred = comparison(reciept, response_type,i,count_red, count_blue, count_pink, count_darkred)
    row += 1
cbook.save(r'E:\Moli\测试用例\python脚本\KGMS标准问批量访问脚本\Moli__US\KGMS标准问批量访问结果\StandardQuestionTestResult111.xls')
print('推出多意图：',count_red,'条')
print('转人工：',count_blue,'条')
print('非英语/不理解：',count_pink,'条')
print('请求失败(返回结果错误)：',count_darkred,'条')
print('测试完成', '!'*100)