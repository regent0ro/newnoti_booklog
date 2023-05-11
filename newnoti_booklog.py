import argparse
import requests
import json
import datetime
import textwrap
from bs4 import BeautifulSoup

# コマンドラインからの引数を格納
parser = argparse.ArgumentParser()
parser.add_argument('--id', help='Booklog user id',type=str,required=True)
parser.add_argument('--year', help='Year of registration',type=int,required=True)
parser.add_argument('--month', help='Month of registration',type=int,required=True)

args = parser.parse_args()
user_id = args.id
month = args.month
year = args.year

# リストを取得(とりあえず100件に制限)　→　sort順を確認する必要がある
api_res=requests.get(f"https://api.booklog.jp/v2/json/{user_id}?count=100")
json_res=json.loads(api_res.text)
books=json_res['books']

#本の情報を取得
new_book_list = []
for book in books:
    html = requests.get(book['url'])
    soup = BeautifulSoup(html.content, "html.parser")

    register_date = soup.find(class_='read-day-status-area').find('span').text
    register_date = datetime.datetime.strptime(register_date, '%Y年%m月%d日')

    #入力した月に登録した本のみ登録
    if register_date.year == year and register_date.month == month:

        #著者は複数人いる場合がある
        author_html = soup.find(class_='item-info-author').find_all('a')

        new_book = {
            'title' : book['title'],
            'author' : ','.join((x.string for x in author_html)),
            'book_cover' : book['image']
        }
        new_book_list.append(new_book)

# 新刊リストがったら
if not new_book_list:
    # markdownのテーブル型式でリストを作成
    new_book_table = (
        '|  タイトル  |  著者  |  表紙  |\n'
        '| ------ | ------ | ------ |\n'
    )

    #TODO textwrap.shorten(str, length, placeholder='...') の利用を考える
    for book in new_book_list:
        new_book_line = f"|  {book['title']}  |  {book['author']}  |  ![{book['title']}]({book['book_cover']} ) |\n"
        new_book_table+= new_book_line
