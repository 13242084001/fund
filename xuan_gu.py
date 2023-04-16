# coding=utf-8
import requests
import random
import io
import logging
import json
import datetime, time, sys
from statistics import mean
#import code_dict
#加上日线ma，周线ma实时计算
#sys.stdout = io.TextIOWrapper(io.BufferedWriter(sys.stdout.buffer, 5), encoding='utf-8')

logging.basicConfig(level=logging.DEBUG, format="%(message)s", filename="./xuangu0410.log", filemode="a")



user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29",
                   "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
                   'Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)', 'Mozilla/5.0 (compatible; U; ABrowse 0.6;  Syllable) AppleWebKit/420+ (KHTML, like Gecko)', 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)', 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR   3.5.30729)', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0;   Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;   SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; Acoo Browser; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; Avant Browser)', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1;   .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; Maxthon; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)', 'Mozilla/4.0 (compatible; Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729); Windows NT 5.1; Trident/4.0)', 'Mozilla/4.0 (compatible; Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727); Windows NT 5.1; Trident/4.0; Maxthon; .NET CLR 2.0.50727; .NET CLR 1.1.4322; InfoPath.2)',
                   'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB6; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)']

headers = {"user-agent": random.choice(user_agent_list),}

#近5年的周五日期列表
week_list = ['2023-04-14', '2023-04-07', '2023-03-31', '2023-03-24', '2023-03-17', '2023-03-10', '2023-03-03', '2023-02-24', '2023-02-17', '2023-02-10', '2023-02-03', '2023-01-20', '2023-01-13', '2023-01-06', '2022-12-30', '2022-12-23', '2022-12-16', '2022-12-09', '2022-12-02', '2022-11-25', '2022-11-18', '2022-11-11', '2022-11-04', '2022-10-28', '2022-10-21', '2022-10-14', '2022-09-30', '2022-09-23', '2022-09-16', '2022-09-09', '2022-09-02', '2022-08-26', '2022-08-19', '2022-08-12', '2022-08-05', '2022-07-29', '2022-07-22', '2022-07-15', '2022-07-08', '2022-07-01', '2022-06-24', '2022-06-17', '2022-06-10', '2022-06-02', '2022-05-27', '2022-05-20', '2022-05-13', '2022-05-06', '2022-04-29', '2022-04-22', '2022-04-15', '2022-04-08', '2022-04-01', '2022-03-25', '2022-03-18', '2022-03-11', '2022-03-04', '2022-02-25', '2022-02-18', '2022-02-11', '2022-01-28', '2022-01-21', '2022-01-14', '2022-01-07', '2021-12-31', '2021-12-24', '2021-12-17', '2021-12-10', '2021-12-03', '2021-11-26', '2021-11-19', '2021-11-12', '2021-11-05', '2021-10-29', '2021-10-22', '2021-10-15', '2021-10-08', '2021-09-30', '2021-09-24', '2021-09-17', '2021-09-10', '2021-09-03', '2021-08-27', '2021-08-20', '2021-08-13', '2021-08-06', '2021-07-30', '2021-07-23', '2021-07-16', '2021-07-09', '2021-07-02', '2021-06-25', '2021-06-18', '2021-06-11', '2021-06-04', '2021-05-28', '2021-05-21', '2021-05-14', '2021-05-07', '2021-04-30', '2021-04-23', '2021-04-16', '2021-04-09', '2021-04-02', '2021-03-26', '2021-03-19', '2021-03-12', '2021-03-05', '2021-02-26', '2021-02-19', '2021-02-10', '2021-02-05', '2021-01-29', '2021-01-22', '2021-01-15', '2021-01-08', '2020-12-31', '2020-12-25', '2020-12-18', '2020-12-11', '2020-12-04', '2020-11-27', '2020-11-20', '2020-11-13', '2020-11-06', '2020-10-30', '2020-10-23', '2020-10-16', '2020-10-09', '2020-09-30', '2020-09-25', '2020-09-18', '2020-09-11', '2020-09-04', '2020-08-28', '2020-08-21', '2020-08-14', '2020-08-07', '2020-07-31', '2020-07-24', '2020-07-17', '2020-07-10', '2020-07-03', '2020-06-24', '2020-06-19', '2020-06-12', '2020-06-05', '2020-05-29', '2020-05-22', '2020-05-15', '2020-05-08', '2020-04-30', '2020-04-24', '2020-04-17', '2020-04-10', '2020-04-03', '2020-03-27', '2020-03-20', '2020-03-13', '2020-03-06', '2020-02-28', '2020-02-21', '2020-02-14', '2020-02-07', '2020-01-23', '2020-01-17', '2020-01-10', '2020-01-03', '2019-12-27', '2019-12-20', '2019-12-13', '2019-12-06', '2019-11-29', '2019-11-22', '2019-11-15', '2019-11-08', '2019-11-01', '2019-10-25', '2019-10-18', '2019-10-11', '2019-09-30', '2019-09-27', '2019-09-20', '2019-09-12', '2019-09-06', '2019-08-30', '2019-08-23', '2019-08-16', '2019-08-09', '2019-08-02', '2019-07-26', '2019-07-19', '2019-07-12', '2019-07-05', '2019-06-28', '2019-06-21', '2019-06-14', '2019-06-06', '2019-05-31', '2019-05-24', '2019-05-17', '2019-05-10', '2019-04-30', '2019-04-26', '2019-04-19', '2019-04-12', '2019-04-04', '2019-03-29', '2019-03-22', '2019-03-15', '2019-03-08', '2019-03-01', '2019-02-22', '2019-02-15', '2019-02-01', '2019-01-25', '2019-01-18', '2019-01-11', '2019-01-04', '2018-12-28', '2018-12-21', '2018-12-14', '2018-12-07', '2018-11-30', '2018-11-23', '2018-11-16', '2018-11-09', '2018-11-02', '2018-10-26', '2018-10-19', '2018-10-12', '2018-09-28', '2018-09-21', '2018-09-14', '2018-09-07', '2018-08-31', '2018-08-24', '2018-08-17', '2018-08-10', '2018-08-03', '2018-07-27', '2018-07-20', '2018-07-13', '2018-07-06', '2018-06-29', '2018-06-22', '2018-06-15', '2018-06-08', '2018-06-01', '2018-05-25', '2018-05-18', '2018-05-11', '2018-05-04', '2018-04-27', '2018-04-20', '2018-04-13', '2018-04-04']




#找最近交易日的日期
url = "http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=sz000002&scale=5&ma=5&datalen=1023"
day_list = []
res = requests.get(url=url)
for li in res.json():
    day = li.get("day")[:10]
    if day not in day_list:
        day_list.append(day)

print(day_list)
day_list = day_list[-2:]

print(day_list)




#当天的上涨排行榜
url =  'http://98.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112402803120599104636_1675409984210&pn=1&pz=3200&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=|0|0|0|web&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1675409984211'

res = requests.get(url=url)
yyx_str = res.text.split('data":')[1].split("})")[0]
#print(yyx_str)
yyx_json = json.loads(yyx_str)
#print(yyx_json)
data = yyx_json.get("diff")
code_list = []
for i in  data:
    #print(i.get("f12")[:2])
    #if "00" == i.get("f12")[:2] and "ST" not in i.get("f14"):
    if i.get("f12")[:2] in ["60", "00"] and "ST" not in i.get("f14") and "-" !=  i.get("f10") and "-" != i.get("f3"):
        code_list.append(i)



for day in day_list[-1:]:
    for i in code_list:
        name = i.get("f14")
        code = i.get("f12")
        zhang_fu = i.get("f3")
        huan_shou = i.get("f8")
        cheng_jiao_liang = i.get("f6")/100000000
        dang_qian_jia = i.get("f2")
        zui_di_jia = i.get("f16")
        zui_gao_jia = i.get("f15")
        kai_pan_jia = i.get("f17")
        shang_ying_xian = (i.get("f15") - i.get("f2"))/i.get("f2")
        #shang_ying_xian = (i.get("f15") / ((dang_qian_jia / (((zhang_fu / 100) + 1))) - 1 - (zhang_fu / 100)
        #liu_tong_zhi = i.get("f21")/100000000
        if 1 < zhang_fu < 6 and cheng_jiao_liang > 1 and dang_qian_jia > kai_pan_jia and shang_ying_xian < 0.05:
            #该股票的20年内的每日基本信息
            his_day_data_url = "http://q.stock.sohu.com/hisHq?code=cn_{0}&start={1}&end={2}".format(code, "20000101", day_list[-2].replace("-", ""))
            print(his_day_data_url)
            #tmp_response_1 = requests.get(url=his_day_data_url, headers=headers).json()[0].get("hq")
            #过去的第5日 10 日 20日 30 日 60日 250日收盘价
            his_5 = his_10 = his_20 = his_30 = his_60 = his_250 = 0
            try:
                tmp_response_1 = requests.get(url=his_day_data_url, headers=headers).json()[0].get("hq")
                #为了计算实时kdj，需要过去的8天内的最高价，最低价跟今日最低最高，做对比，求出9日内最高，最低价
                his_di_list = [zui_di_jia]
                his_gao_list = [zui_gao_jia]
                for hq in tmp_response_1[0:8]:
                    his_di_list.append(float(hq[5]))
                    his_gao_list.append(float(hq[6]))
                his_9_di = min(his_di_list)
                his_9_gao = max(his_gao_list)
                rsv = (dang_qian_jia - his_9_di) / (his_9_gao - his_9_di) * 100
                #print(his_9_di, his_9_gao)
                his_5 = float(tmp_response_1[4][2])
                his_10 = float(tmp_response_1[9][2])
                his_20 = float(tmp_response_1[19][2])
                his_30 = float(tmp_response_1[29][2])
                his_60 = float(tmp_response_1[59][2])
                his_250 = float(tmp_response_1[249][2])
            except Exception as e:
                pass
            #昨日的5、10、20、30、60、250日均线
            ma_url="https://stockapi.com.cn/v1/quota/ma?token=a20428f5bc97e60c6918a15e032079b41a3872df60575e1d&code={0}&date={1}&ma=5,10,20,30,60,250&rehabilitation=100&calculationCycle=100".format(code, day_list[-2])
            
            #获取上周五的5/10/20/30/60/250周均线，其实可以获取昨天的用来计算最新的实时均线
            week_ma_url="https://stockapi.com.cn/v1/quota/ma?token=a20428f5bc97e60c6918a15e032079b41a3872df60575e1d&code={0}&date={1}&ma=5,10,20,30,60,250&rehabilitation=100&calculationCycle=101".format(code, week_list[0])
            #print(week_ma_url)
            
            res_1 = requests.get(url=ma_url)
            res_2 = requests.get(url=week_ma_url)
            #print(res_1.json())
            try:
                #计算最新的日k线均线数据
                ma_data = res_1.json().get("data")
                ma_data_list = []
                if ma_data.get("ma5"):
                    if his_5:
                        ma5 = ((float(ma_data.get("ma5")) * 5 - his_5)  + dang_qian_jia)/5
                        ma_data_list.append(ma5)
                if ma_data.get("ma10"):
                    if his_10:
                        ma10 = ((float(ma_data.get("ma10")) * 10 - his_10)  + dang_qian_jia)/10
                        ma_data_list.append(ma10)
                if ma_data.get("ma20"):
                    if his_20:
                        ma20 = ((float(ma_data.get("ma20")) * 20 - his_20)  + dang_qian_jia)/20
                        ma_data_list.append(ma20)
                if ma_data.get("ma30"):
                    if his_30:
                        ma30 = ((float(ma_data.get("ma30")) * 30 - his_30)  + dang_qian_jia)/30
                        ma_data_list.append(ma30)
                if ma_data.get("ma60"):
                    if his_60:
                        ma60 = ((float(ma_data.get("ma60")) * 60 - his_60)  + dang_qian_jia)/60
                        ma_data_list.append(ma60)
                if ma_data.get("ma250"):
                    if his_250:
                        ma250 = ((float(ma_data.get("ma250")) * 250 - his_250)  + dang_qian_jia)/250
                        ma_data_list.append(ma250)
           
                week_ma_data = res_2.json().get("data")
                #print(week_ma_data)
                week_ma_data_list = []
                if week_ma_data.get("ma5"):
                    #往前第五周周五的收盘价, 计算最新的5周ma
                    w_his_5_url = "http://q.stock.sohu.com/hisHq?code=cn_{0}&start={1}&end={2}".format(code, week_list[4].replace("-", ""), week_list[4].replace("-", ""))
                    #print(w_his_5_url)
                    res = requests.get(w_his_5_url, headers=headers).json()[0].get("hq")[0][2]
                    #print(res)
                    w_his_5 = float(res)
                    #print(ma_data.get("ma5"))
                    w_ma5 = ((float(week_ma_data.get("ma5")) * 5 - w_his_5)  + dang_qian_jia)/5
                    #print(w_ma5)
                    week_ma_data_list.append(w_ma5)
                if week_ma_data.get("ma10"):
                    w_his_10_url = "http://q.stock.sohu.com/hisHq?code=cn_{0}&start={1}&end={2}".format(code, week_list[9].replace("-", ""), week_list[9].replace("-", ""))
                    res = requests.get(w_his_10_url).json()[0].get("hq")[0][2]
                    w_his_10 = float(res)
                    w_ma10 = ((float(week_ma_data.get("ma10")) * 10 - w_his_10)  + dang_qian_jia)/10
                    week_ma_data_list.append(w_ma10)
                if week_ma_data.get("ma20"):
                    w_his_20_url = "http://q.stock.sohu.com/hisHq?code=cn_{0}&start={1}&end={2}".format(code, week_list[19].replace("-", ""), week_list[19].replace("-", ""))
                    res = requests.get(w_his_20_url).json()[0].get("hq")[0][2]
                    w_his_20 = float(res)
                    w_ma20 = ((float(week_ma_data.get("ma20")) * 20 - w_his_20)  + dang_qian_jia)/20
                    week_ma_data_list.append(w_ma20)
                if week_ma_data.get("ma30"):
                    w_his_30_url = "http://q.stock.sohu.com/hisHq?code=cn_{0}&start={1}&end={2}".format(code, week_list[29].replace("-", ""), week_list[29].replace("-", ""))
                    res = requests.get(w_his_30_url).json()[0].get("hq")[0][2]
                    w_his_30 = float(res)
                    w_ma30 = ((float(week_ma_data.get("ma30")) * 30 - w_his_30)  + dang_qian_jia)/30
                    week_ma_data_list.append(w_ma30)
                if week_ma_data.get("ma60"):
                    w_his_60_url = "http://q.stock.sohu.com/hisHq?code=cn_{0}&start={1}&end={2}".format(code, week_list[59].replace("-", ""), week_list[59].replace("-", ""))
                    res = requests.get(w_his_60_url).json()[0].get("hq")[0][2]
                    w_his_60 = float(res)
                    w_ma60 = ((float(week_ma_data.get("ma60")) * 60 - w_his_60)  + dang_qian_jia)/60
                    week_ma_data_list.append(w_ma60)
                #if week_ma_data.get("ma250"):
                    #week_ma_data_list.append(float(week_ma_data.get("ma250")))
                #ma_data_list = [float(x) for x in ma_data_list]
                #print(code, ma_data_list, week_ma_data_list)
                #日线最大的那根
                max_ma = max(ma_data_list)
                #周线最大的那根
                week_max_ma = max(week_ma_data_list)

                len_list = []
                w_len_list = []
                for x in ma_data_list:
                    if (max_ma * 0.97) <= x:
                        len_list.append(x)
                        #logging.info(len(len_list))
                for x in week_ma_data_list:
                    if (week_max_ma * 0.95) <= x:
                        w_len_list.append(x)
                if dang_qian_jia > max_ma  and len(len_list) >= 3 and dang_qian_jia >= week_max_ma and len(w_len_list) >= 3:
                    macd_url = "https://stockapi.com.cn/v1/quota/macd?token=a20428f5bc97e60c6918a15e032079b41a3872df60575e1d&code={0}&cycle=9&date={1}&longCycle=26&shortCycle=12&vipCycleFlag=0&calculationCycle=100".format(code, day_list[-2])
                    macd_res = requests.get(url=macd_url).json().get("data")
                    dif = macd_res.get("dif")[0]
                    dea = macd_res.get("dea")[0]
                    macd = macd_res.get("macd")[0]
                    w_macd_url = "https://stockapi.com.cn/v1/quota/macd?token=a20428f5bc97e60c6918a15e032079b41a3872df60575e1d&code={0}&cycle=9&date={1}&longCycle=26&shortCycle=12&vipCycleFlag=0&calculationCycle=101".format(code, day_list[-2])
                    w_macd_res = requests.get(url=w_macd_url).json().get("data")
                    w_dif = w_macd_res.get("dif")[0]
                    w_dea = w_macd_res.get("dea")[0]
                    w_macd = w_macd_res.get("macd")[0]
                    if macd > -0.05 and w_macd > -0.1:# and (w_dif * w_dea) > 0:
                        kdj_url = "https://stockapi.com.cn/v1/quota/kdj?token=a20428f5bc97e60c6918a15e032079b41a3872df60575e1d&calculationCycle=100&code={0}&cycle=9&cycle1=3&cycle2=3&date={1}&vipCycleFlag=0".format(code, day_list[-2])
                        kdj_res = requests.get(url=kdj_url).json().get("data")
                        k = kdj_res.get("k")[0]
                        d = kdj_res.get("d")[0]
                        j = kdj_res.get("j")[0]
                        to_day_k = k * 2/3 + rsv * 1/3
                        to_day_d = d * 2/3 + to_day_k * 1/3
                        to_day_j = to_day_k * 3 - to_day_d * 2
                        #print(code, his_9_di, his_9_gao, to_day_j, to_day_k, to_day_d)
                        w_kdj_url = "https://stockapi.com.cn/v1/quota/kdj?token=a20428f5bc97e60c6918a15e032079b41a3872df60575e1d&calculationCycle=101&code={0}&cycle=9&cycle1=3&cycle2=3&date={1}&vipCycleFlag=0".format(code, day_list[-2])
                        w_kdj_res = requests.get(url=w_kdj_url).json().get("data")
                        w_k = w_kdj_res.get("k")[0]
                        w_d = w_kdj_res.get("d")[0]
                        w_j = w_kdj_res.get("j")[0]
                        last_day = week_list[9]
                        w_his_gao_list = [zui_gao_jia]
                        w_his_di_list = [zui_di_jia]
                        for day_1 in tmp_response_1:
                            if not day_1[0] == last_day:
                                w_his_di_list.append(float(day_1[5]))
                                w_his_gao_list.append(float(day_1[6]))
                            else:
                                break
                        #print(w_his_di_list, w_his_gao_list)
                        w_his_9_di = min(w_his_di_list)
                        w_his_9_gao = max(w_his_gao_list)
                        w_rsv = (dang_qian_jia - w_his_9_di) / (w_his_9_gao - w_his_9_di) * 100
                        #print(code, j, k, d, w_j, w_k, w_d)
                        to_week_k = w_k * 2/3 + w_rsv * 1/3
                        to_week_d = w_d * 2/3 + to_week_k * 1/3
                        to_week_j = to_week_k * 3 - to_week_d * 2
                        #print(w_his_9_di, w_his_9_gao, to_week_j, to_week_k, to_week_d)
                        if (100 > to_day_j > to_day_k > to_day_d > 45 and to_day_d < 80) and (100 > to_week_j > to_week_k > to_week_d > 45 and to_week_d < 80):
                            #print(code)
                            #gai_nian = code_dict.code_dict.get(code)
                            gai_nian_url = "http://stockpage.10jqka.com.cn/{0}/".format(code)
                            gai_nian = requests.get(gai_nian_url, headers=headers).text.split('dd title="')[1].split('">')[0]
                            #print(gai_nian)
                            logging.info(str(day) + "-->" + str(name) + " -$题材概念: " + gai_nian)
                            #log.info(code_list.index(code))
                            #des_code_list.append(code)
            except Exception as e:
                logging.info("#######", e)
                #print(i.get("f12"))
