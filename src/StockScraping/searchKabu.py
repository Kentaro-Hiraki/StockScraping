import requests
from bs4 import BeautifulSoup

def main(url):
    stocks = []
    # ページをリクエスト
    response = requests.get(url)
    response.encoding = 'utf-8'

    # BeautifulSoupでHTMLをパース
    soup = BeautifulSoup(response.text, 'html.parser')

    # 年初来安値一覧のテーブルを見つける
    table = soup.find('table', {'class': 'stock_table'})

    # テーブルから銘柄情報を取得
    # stocks = []
    for row in table.find_all('tr')[1:]:  # ヘッダー行をスキップ
        columns = row.find_all((["td", "th"]))
        if columns and len(columns) > 5:  # 必要なカラムが存在するか確認
            code = columns[0].text.strip()
            name = columns[1].text.strip()
            price = columns[5].text.strip().replace(',', '')
            yield_percent = columns[12].text.strip().replace('%', '')
            try:
                yield_percent = float(yield_percent)
                if yield_percent >= 4.0:  # 利回りが4%以上の銘柄をフィルタリング
                    stocks.append({
                        'コード': code,
                        '銘柄名': name,
                        '株価': price,
                        '利回り': yield_percent
                    })
            except ValueError:
                continue  # 利回りが数値でない場合はスキップ

    # 結果を表示
    for stock in stocks:
        print(f"コード: {stock['コード']}, 銘柄名: {stock['銘柄名']}, 株価: {stock['株価']}, 利回り: {stock['利回り']}%")


# かぶたんの年初来安値一覧ページのURLを指定
page_number = 0;
for i in range (20):
    page_number = page_number + 1
    url = 'https://kabutan.jp/warning/?mode=3_4&market=0&capitalization=-1&stc=&stm=0&page=' + str(page_number)
    main(url)
