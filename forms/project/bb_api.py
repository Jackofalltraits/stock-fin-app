import requests

url = "https://bloomberg-market-and-financial-news.p.rapidapi.com/stock/get-statistics"

querystring = {"id":"aapl:us"}

headers = {
    'x-rapidapi-key': "f62abdf26amsh0771a5e75100452p1f9a04jsn7425db33550d",
    'x-rapidapi-host': "bloomberg-market-and-financial-news.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)
print(response.text)