# encoding=utf-8
import sys
import requests
from prettytable import PrettyTable

table = PrettyTable(["名称", "净流入比", "累计涨幅", "流通值(亿)", "总市值(亿)", "市净率", "市盈率", "换手率", "趋势"])
#table = PrettyTable(["名称", "净流入比", "累计涨幅", "流通值(亿)", "总市值(亿)", "市净率", "市盈率", "换手率"])


def checker(list_):
    temp = []
    flag = 1 if list_[1] > list_[0] else 0
    increase = decrease = 0
    for m, n in enumerate(list_):
        if flag:
            try:
                if list_[m] < list_[m + 1]:
                    increase += 1
                else:
                    increase = 0
                    decrease = 1
                    flag = 0
            except IndexError:
                pass
        else:
            try:
                if list_[m] > list_[m + 1]:
                    decrease += 1
                else:
                    decrease = 0
                    increase = 1
                    flag = 1
            except IndexError:
                pass


    return "\033[0;31;40m^:{0}\33[0m".format(str(increase)) if increase > decrease else "\033[0;32;40mv:{0}\33[0m".format(str(decrease))


with open("./code_core.log", "r", encoding="utf-8") as f:
    tmp_list = f.readlines()

date_list = []
for row in tmp_list:
    if row.split(",")[1] not in date_list:
        date_list.append(row.split(",")[1])

index = -int(sys.argv[1])
date_list = date_list[index:]
#print(date_list)
tm_dict = {}
for i in tmp_list:
    #print(i)
    x_list = i.split(",")
    #print(x_list)
    if x_list[1] in date_list:
        if tm_dict.get(x_list[0]):
            tm_dict[x_list[0]][0] += 1
            if "%" in x_list[2]:
                tm_dict[x_list[0]][1] += float(x_list[2][:-1])/100
            else:
                tm_dict[x_list[0]][1] += float(x_list[2][:-1])
            try:
                tm_dict[x_list[0]][2] += float(x_list[5].strip())
                tm_dict[x_list[0]][3].append(x_list[6].strip())
            except Exception as e:
                tm_dict[x_list[0]][2] += 0.0
        else:
            #print(x_list)
            if "%" in x_list[2]:
                increase_num = float(x_list[2][:-1])/100
            else:
                increase_num = float(x_list[2][:-1])
            try:
                add_flow = float(x_list[5].strip())
                price_l =  x_list[6].strip()
            except Exception as e:
                add_flow = 0.0
                price_l = []
            tm_dict[x_list[0]] = [1, increase_num, add_flow, price_l]
            

#print(tm_dict)
verbose_dict = {}       
for k,v in tm_dict.items():
    if int(sys.argv[1]) == v[0]:
        trend = checker(v[3])
        #print(trend)
        verbose_dict[k] = str(round(v[1]*100, 2)) + "| " + str(v[2]) + "| " + trend
        #verbose_dict[k] = str(round(v[1]*100, 2)) + "| " + str(v[2])

#print(verbose_dict)
code_param_list = []
for code in verbose_dict.keys():
    if "0" == code[0]:
        code_param_list.append("sz" + code[:6])
    else:
        code_param_list.append("sh" + code[:6])

url = "https://web.sqt.gtimg.cn/utf8/q={0}&r=0.4137883905173720412".format(",".join(code_param_list))

basic_res = requests.get(url)
#print(basic_res.text)
res_list = basic_res.text.split(";")
#print(len(res_list))
tmp_list = []
for code_str in res_list[:-1]:
    x_list = code_str.split("~")
    #print(x_list)
    #print("#####################")
    tmp_list.append(x_list[44] + "| " + x_list[45] + "| " + x_list[46] + "| " + x_list[39] + "| "  + x_list[38])
#print(tmp_list)
last_list = list(map(lambda x,y: x + "| " + str(round(float(verbose_dict[x].split("| ")[1])/(float(y.split("| ")[1])*100000000) * 100, 4)) + "%| " + verbose_dict[x].split("| ")[0] + "| " + y + "| " + verbose_dict[x].split("| ")[2], verbose_dict.keys(), tmp_list))
#last_list = list(map(lambda x,y: x + "| " + str(round(float(verbose_dict[x].split("| ")[1])/(float(y.split("| ")[1])*100000000) * 100, 4)) + "%| " + verbose_dict[x].split("| ")[0] + "| " + y, verbose_dict.keys(), tmp_list))

for i in last_list:
    table.add_row(i.split("| "))
    #print(i)

for k in table.align.keys():
    table.align[k] = 'l'
print(table)
