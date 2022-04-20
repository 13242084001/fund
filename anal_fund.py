# coding=utf-8
#输入基金代码，打印个季度持仓及基本信息
from bs4 import BeautifulSoup
import sys
import requests
import random
from prettytable import from_html
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')


def anla_chi_cang_html(fund):
    zcgm_url = "http://fundf10.eastmoney.com/ccmx_{0}.html".format(fund,)
    headers_0 = { "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                  "Accept-Encoding": "gzip, deflate",
                  "Accept-Language": "zh-CN,zh;q=0.9",
                  #"Cache-Control": "max-age=0",
                  "Connection": "keep-alive",
                  #"Cookie": "EMFUND1=null; EMFUND3=null; EMFUND2=null; EMFUND4=null; EMFUND5=null; qgqp_b_id=7143716b34a58fe86b3f407c67112b77; st_si=67265165850040; st_asi=delete; ASP.NET_SessionId=kjs5xcotsllp3aekv0qsedi0; EMFUND0=null; EMFUND6=03-07%2016%3A39%3A44@%23%24%u6613%u65B9%u8FBE%u6807%u666E%u6D88%u8D39%u54C1%u6307%u6570A@%23%24118002; EMFUND7=04-01%2017%3A29%3A29@%23%24%u534E%u590F%u80FD%u6E90%u9769%u65B0%u80A1%u7968A@%23%24003834; EMFUND9=04-08%2010%3A05%3A17@%23%24%u534E%u6CF0%u67CF%u745E%u4E9A%u6D32%u9886%u5BFC%u4F01%u4E1A%u6DF7%u5408@%23%24460010; td_cookie=4006508035; EMFUND8=04-08 14:22:38@#$%u8D22%u901A%u4EF7%u503C%u52A8%u91CF%u6DF7%u5408@%23%24720001; st_pvi=59649223508013; st_sp=2022-03-07%2016%3A39%3A44; st_inirUrl=http%3A%2F%2Ffund.eastmoney.com%2F118002.html; st_sn=101; st_psi=20220408142249287-112200305283-9155663238",
                  "Host": "fundf10.eastmoney.com",
                  #"Referer": "http://fund.eastmoney.com/",
                  "Upgrade-Insecure-Requests": "1",
                  "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
            }
    res = requests.get(zcgm_url, headers=headers_0)
    #print(res.text)
    soup = BeautifulSoup(res.text, "html.parser")
    des_div = soup.find("div", class_="bs_gl")
    for a in des_div.find_all("a"):
        a.replace_with("%s" % a.string)

    for span in des_div.find_all("span"):
        span.replace_with("%s" % span.string)
    for label in des_div.find_all("label"):
        print(label.text.strip())
    print(" ")
    print(" ")

    headers = {"Accept": "*/*",
               "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "zh-CN,zh;q=0.9",
               "Connection": "keep-alive",
               "Cookie": "EMFUND1=null; EMFUND2=null; EMFUND3=null; EMFUND4=null; EMFUND5=null; EMFUND6=null; qgqp_b_id=7143716b34a58fe86b3f407c67112b77; st_si=67265165850040; st_asi=delete; ASP.NET_SessionId=kjs5xcotsllp3aekv0qsedi0; EMFUND0=null; EMFUND7=03-07%2016%3A39%3A44@%23%24%u6613%u65B9%u8FBE%u6807%u666E%u6D88%u8D39%u54C1%u6307%u6570A@%23%24118002; EMFUND8=04-01%2017%3A29%3A29@%23%24%u534E%u590F%u80FD%u6E90%u9769%u65B0%u80A1%u7968A@%23%24003834; EMFUND9=04-07 15:24:57@#$%u8D22%u901A%u4EF7%u503C%u52A8%u91CF%u6DF7%u5408@%23%24720001; st_pvi=59649223508013; st_sp=2022-03-07%2016%3A39%3A44; st_inirUrl=http%3A%2F%2Ffund.eastmoney.com%2F118002.html; st_sn=29; st_psi=2022040715251816-112200305283-8374870842; td_cookie=3924229445",
               "Host": "fundf10.eastmoney.com",
               "Referer": "http://fundf10.eastmoney.com/ccmx_{0}.html".format(fund,),
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
}
    chi_cang_url = "http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code={0}&topline=10&year=&month=&rt={1}".format(fund, str(random.uniform(0, 1)))
    res = requests.get(chi_cang_url, headers=headers)
    res_str = res.text.split("\"")[1]
    if not res_str:
        return []
    soup = BeautifulSoup(res_str, "html.parser")
    for a in soup.find_all("a"):
        a.replace_with("%s" % a.string)
    for span in soup.find_all("span"):
        span.replace_with("%s" % span.string)
    #four_chi_cang_10_tr = soup.find_all("tbody")[0].find_all("tr")
    four_chi_cang_table_all = soup.find_all("table", class_="w782 comm tzxq")
    code_list = []
    #print(four_chi_cang_10_tr)
    for table in four_chi_cang_table_all:
        tb = from_html(str(table))
        print(tb[0])
        #for tr in tbody.find_all("tr"):
         #   td = tr.find_all("td")[2]
          #  if td.a:
           #     if str(td).split(".")[2][-1] in ["0", "1"]:
            #        code = td.a.string
             #       print(td)
              #      code_list.append(code)
            
    return code_list

fund = str(sys.argv[1])
anla_chi_cang_html(fund)
