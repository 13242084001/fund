# coding=utf-8
#获取每天净流入股票及当日基本行情数据
from bs4 import BeautifulSoup
import sys
import requests
import random
from prettytable import from_html
import io
import json
import datetime, time


sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')


code_list = []

user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29",
                   "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
                   'Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)', 'Mozilla/5.0 (compatible; U; ABrowse 0.6;  Syllable) AppleWebKit/420+ (KHTML, like Gecko)', 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)', 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR   3.5.30729)', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0;   Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;   SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; Acoo Browser; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; Avant Browser)', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1;   .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; Maxthon; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)', 'Mozilla/4.0 (compatible; Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729); Windows NT 5.1; Trident/4.0)', 'Mozilla/4.0 (compatible; Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727); Windows NT 5.1; Trident/4.0; Maxthon; .NET CLR 2.0.50727; .NET CLR 1.1.4322; InfoPath.2)',
                   'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB6; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)']

headers = {"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "cache-control": "max-age=0",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="100", "Microsoft Edge";v="100"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": random.choice(user_agent_list),
            }


headers_1 = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "prov=cn020; city=0755; weather_city=gd_sz; region_ver=1; vjuids=435bdeccd.18009294dca.0.c8691def982dc; vjlast=1649421143.1649462987.13",
            "Host": "app.finance.ifeng.com",
            "Referer": "https://app.finance.ifeng.com/list/stock.php?t=hs&f=chg_pct&o=desc&p=2",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": random.choice(user_agent_list)
        }

headers_2 = {"Referer": "https://finance.sina.com.cn",
             "User-Agent": random.choice(user_agent_list)
    }

def get_all_code(n=1):
    try:
        with open(r"code.txt", "r", encoding="utf-8") as f:
            codes = f.readlines()
            #code_list.extend(eval(codes))
            code_list.extend(codes)
            return 0
    except Exception as e:
        base_url = "http://app.finance.ifeng.com/list/stock.php?t=hs&f=chg_pct&o=desc&p={0}".format(n)
        res = requests.get(base_url, headers=headers_1)
        res_str = res.text
        #print(res_str)
        soup = BeautifulSoup(res_str, "html.parser")
        trs = soup.find_all("table")[0].find_all("tr")[1:]
        for tr in trs[:-1]:
            tds = tr.find_all("td")
            code = tds[0].a.string + tds[1].a.string
            #print(code)
            if ("3" != code[0]) and ("688" != code[:3]) and ("ST" not in code):
                code_list.append(code)
        if "下一页" in str(trs[-1]):
            #print(11111)
            time.sleep(random.randint(1,3))
            return get_all_code(n+1)
        return None
    

def get_money_flow(code):
    #url = "http://api.guxun168.com/moneyflow?code={0}&start={1}&end={2}&token=XeYJdHSSa7IC6rVY".format(code[:6], datetime.datetime.now().strftime("%Y%m%d"), datetime.datetime.now().strftime("%Y%m%d"))
    fina_code, get_price_code = ("1." + code[:6], "sh" + code[:6]) if "6" == code[0] else ("0." + code[:6], "sz" + code[:6])
    code_price_url = "http://hq.sinajs.cn/list={0}".format(get_price_code)
    url = "https://emdatah5.eastmoney.com/dc/ZJLX/getZJLXData?secid={0}&fields=f57,f58,f135,f136,f137,f138,f139,f140,f141,f142,f143,f144,f145,f146,f147,f148,f149,f86&ut=".format(fina_code)
    res = requests.get(url, headers=headers)
    flow_dict = res.json()
    net_mf_amount = flow_dict.get("data").get("f137")
    get_price_res = requests.get(code_price_url, headers=headers_2)
    try:
        price_data = get_price_res.text.split(",")[1:-2]
        code_data = code.strip() + "," + str(net_mf_amount) + "," + ",".join(price_data)
        with open(r"code_data.log", "a", encoding="utf-8") as f:
            f.write(code_data)
            f.write("\n")
        if float(net_mf_amount) > 0:
            increase = round((float(price_data[2]) - float(price_data[1]))/float(price_data[1])*100, 4)
            increase_today = round((float(price_data[2]) - float(price_data[0]))/float(price_data[0])*100, 4)
            zhen_fu = round((float(price_data[3]) - float(price_data[4]))/float(price_data[4])*100, 4)
            with open(r"code_core.log", "a", encoding="utf-8") as f:
                f.write(code.strip() + "," + str(datetime.date.today()) + "," + str(increase ) + "%," + str(increase_today) + "%," + str(zhen_fu) + "%," + str(net_mf_amount) + "," + price_data[2])
                f.write("\n")
    except Exception as e:
        print(e)
    print(code.strip(), "net_mf_amount:" + str(net_mf_amount))



if __name__ == "__main__":
    get_all_code()
    print(code_list)
    #print(len(code_list))
    for code in code_list:
        time.sleep(random.choice([1, 0.6, 0.25, 0.05, 0.1]))
        get_money_flow(code)

