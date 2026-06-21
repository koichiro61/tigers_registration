import sys
import re
import csv
from typing import List
import requests
from bs4 import BeautifulSoup

def main():
    reg_history_url = 'https://hanshintigers.jp/game/regist/history.html'
    csv_file_name = 'tigers_reg_history.csv'
    
    soup = get_soup(reg_history_url)
    div_reg_history_table = soup.find('div', id='reg-history-table')
    trs = div_reg_history_table.find_all('tr')

    with open(csv_file_name, mode='w', encoding='utf_8', newline='') as outf:
        csv_writer = csv.writer(outf)
        print(f'Writing {csv_file_name}', file=sys.stderr)
        csv_writer.writerow(['日付', 
                            '登録_背番号', '登録_名前', '登録_守備位置', 
                            '抹消_背番号', '抹消_名前', '抹消_守備位置'])
        regdate= ''
        
        # 各行ごとの処理
        for tr in trs:
            tds = tr.find_all('td')
            tdlist = []
            #カラムの内容をリスト変数 tdlist にセット
            for td in tds:
                t = td.text
                if t == '\xa0': #なぜかカタカナスペース
                    t = ''
                tdlist.append(t)
                
            if len(tdlist) == 7:    #カラム数が7の行だけ扱う
                if tdlist[0] == '':             #日付が空欄のとき
                     tdlist[0] = regdate    #前のレコードの日付引き継ぐ
                else:
                    regdate = tdlist[0]     #引き継ぎ用に日付を保存
            
                csv_writer.writerow(tdlist)
            #各行ごとの処理終わり

def get_soup(url: str) -> BeautifulSoup:
    html = get_contents(url)
    soup = BeautifulSoup(html, 'html.parser')
    return soup

  
def get_contents(url: str, proxies: dict = None) -> str:
    user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) '\
    +'AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/22A5316k'\
    +' [FBAN/FBIOS;FBAV/475.0.0.31.110;FBBV/627850395;FBDV/iPhone13,2;'\
    +'FBMD/iPhone;FBSN/iOS;FBSV/18.0;FBSS/3;FBID/phone;FBLC/pt_BR;FBOP/5;FBRV/0]'
    try:
        r = requests.get(url, verify=True, headers={
                         'User-Agent': user_agent}, proxies=proxies, timeout=10)
        r.encoding = r.apparent_encoding
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(e, file=sys.stderr)
        sys.exit(-1)
    print(r.encoding)
    return r.text
    
if __name__ == '__main__':
    main()
