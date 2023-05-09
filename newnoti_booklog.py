import argparse
import requests
from bs4 import BeautifulSoup
import json
import datetime

DEBUG_MODE = True

# TODO エラー処理考える

parser = argparse.ArgumentParser()
parser.add_argument('--id', help='Booklog user id',type=str,required=True)
parser.add_argument('--month', help='Month of registration',type=int,required=True)

args = parser.parse_args()
user_id = args.id
month = args.month

# リストを取得(とりあえず100件に制限)　→　sort順を確認する必要がある
api_res=requests.get(f"https://api.booklog.jp/v2/json/{user_id}?count=100")
json_res=json.loads(api_res.text)
books=json_res['books']

if DEBUG_MODE:
    print(json_res)

#本の情報を取得
for book in books:
    html = requests.get(book['url'])
    soup = BeautifulSoup(html.content, "html.parser")

    register_date = register_date=soup.find(class_='read-day-status-area').find('span').text
    
    if DEBUG_MODE:
        print(register_date)

    # TODO 月でフィルタリングしてOKなら　著者、表紙を追加取得して配列に格納する
    #amazon_link =soup.find(class_='itemInfoElm').find('a').get('href')
    

# TODO markdownのテーブル型式でリストを作成する。長いタイトル、著者名は...で表示する