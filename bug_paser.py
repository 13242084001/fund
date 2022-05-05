# coding=utf-8
from bs4 import BeautifulSoup
import sys
import requests
import random
#from get_ua import get_ua 


top_100 = ""

def get_fund(file_name):
    soup = BeautifulSoup(open(file_name, encoding="utf-8"), features="html.parser")
    table_trs = soup.find_all("tr")
    fund_list = []
    for table_tr in table_trs:
        for td in table_tr.find_all("td"):
            if td.a:
            #print(td)
                st = td.a.string
                fund_list.append(td.a.string)
                try:
                    int(st)
                except Exception as e:
                    pass
                break
    #print(file_name)
    return fund_list

count_dict = {}
for file in sys.argv[1:]:
    count_dict[file.split(".")[0]] = get_fund(file)

print(count_dict)

#dict_len = len(count_dict)

#比较各个筛选条件，基金重合代码
def comp():
    comp_list = []
    comp_set = {}
    for v in count_dict.values():
        if comp_set:
            comp_set = comp_set & set(v)
            print(comp_set)
        else:
            comp_set = set(v)
    return comp_set

#获取每只基金持仓股票
def anla_chi_cang_html(fund):
    headers = {"Accept": "*/*",
               "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "zh-CN,zh;q=0.9",
               "Connection": "keep-alive",
               "Cookie": "EMFUND1=null; EMFUND2=null; EMFUND3=null; EMFUND4=null; EMFUND5=null; EMFUND6=null; qgqp_b_id=7143716b34a58fe86b3f407c67112b77; st_si=67265165850040; st_asi=delete; ASP.NET_SessionId=kjs5xcotsllp3aekv0qsedi0; EMFUND0=null; EMFUND7=03-07%2016%3A39%3A44@%23%24%u6613%u65B9%u8FBE%u6807%u666E%u6D88%u8D39%u54C1%u6307%u6570A@%23%24118002; EMFUND8=04-01%2017%3A29%3A29@%23%24%u534E%u590F%u80FD%u6E90%u9769%u65B0%u80A1%u7968A@%23%24003834; EMFUND9=04-07 15:24:57@#$%u8D22%u901A%u4EF7%u503C%u52A8%u91CF%u6DF7%u5408@%23%24720001; st_pvi=59649223508013; st_sp=2022-03-07%2016%3A39%3A44; st_inirUrl=http%3A%2F%2Ffund.eastmoney.com%2F118002.html; st_sn=29; st_psi=2022040715251816-112200305283-8374870842; td_cookie=3924229445",
               "Host": "fundf10.eastmoney.com",
               "Referer": "http://fundf10.eastmoney.com/ccmx_720001.html",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
}
    chi_cang_url = "http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code={0}&topline=10&year=&month=&rt={1}".format(fund, str(random.uniform(0, 1)))
    res = requests.get(chi_cang_url, headers=headers)
    res_str = res.text.split("\"")[1]
    if not res_str:
        return []
    soup = BeautifulSoup(res_str, "html.parser")
    print(res_str)
    four_chi_cang_10_tr = soup.find_all("tbody")[0].find_all("tr")
    code_list = []
    #print(four_chi_cang_10_tr)
    for tr in four_chi_cang_10_tr:
        td = tr.find_all("td")[2]
        if td.a:
            if str(td).split(".")[2][-1] in ["0", "1"]:
                code = td.a.string
                print(td)
        #elif td.span:
        #    code = td.span.string
                code_list.append(code)
            
    return code_list

#获取基金们持仓股票的统计
def find_shares():
    shares_dict  = {}
    for funds in count_dict.values():
        for fund in funds:
            code_list = anla_chi_cang_html(fund)
            for code in code_list:
                if shares_dict.get(code):
                    shares_dict[code] += 1
                else:
                    shares_dict[code] = 1
    final_dict = sorted(shares_dict.items(), key=lambda x:x[1], reverse=True)
    return final_dict

shares = find_shares()
for share in shares:
    print(share)

#comp()
