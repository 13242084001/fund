# encoding=utf-8

from functools  import reduce


#判断连续上涨还是下跌
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


    return "^:{0}".format(str(increase)) if increase > decrease else "v:{0}".format(str(decrease))



with open("code_data.log", "r") as f:
    price_list = f.readlines()

price_dict = {}
for row in price_list:
    if row.split(",")[0] not in price_dict:
        price_dict[row.split(",")[0]] = [row.split(",")[4]]
    else:
        price_dict[row.split(",")[0]].append(row.split(",")[4])

#print(price_dict)

code_5_10_dict = {}

for k,v in price_dict.items():
    if len(v) > 10:
        ma5 = reduce(lambda x,y:float(x) + float(y), v[-5:])/5
        ma10 = reduce(lambda x,y:float(x) + float(y), v[-10:])/10
        old_ma5 = reduce(lambda x,y:float(x) + float(y), v[-6:-1])/5
        old_ma10 = reduce(lambda x,y:float(x) + float(y), v[-11:-1])/10
        if old_ma5 < old_ma10 and ma5 > ma10:
            res = checker(v)
            if res.split(":")[0] == "^" and int(res.split(":")[1]) >= 3:
                print(k)
  
    
