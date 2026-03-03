import os
import requests
import json
from my_token import TOKEN
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

title_news = input("Enter word to search in the title: ")
url = "https://newsapi.org/v2/everything"
today = datetime.today()
seven_days_ago = today - timedelta(days=7)
if title_news.strip() == "":
    q = "Python"  # значение по умолчанию
else:
    q = title_news.strip()

params = {
        "q": q,
        "sortBy": "popularity",
        "apiKey": TOKEN,
        "from": seven_days_ago.strftime("%Y-%m-%d"),
        "to": today.strftime("%Y-%m-%d")
}

response = requests.get(url, params=params)
data = response.json()
found = 0
if response.status_code != 200:
    raise Exception(f"Ошибка: {response.status_code}")
else:
    if data["status"] != "ok":
        raise Exception(f"Ошибка API: {data['message']}")
    else:
        print(
            f"News search results for: {q}\n"
            f"Period: {seven_days_ago.strftime('%Y-%m-%d')} -> {today.strftime('%Y-%m-%d')}"
        )
        filename = "titles.json"
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                try:
                    records = json.load(file)
                except json.JSONDecodeError:
                    records = {}
        else:
            records = {}
        records[q] = []
        articles = sorted(data["articles"], key=lambda x:x["publishedAt"], reverse=False)
        for article in articles:
            if not title_news or title_news.lower() in article["title"].lower():
                records[q].append({
                    "Date":article["publishedAt"],
                    "Title": article["title"],
                    "Author": article.get("author"),
                    "URL": article["url"]
                })
                found += 1
        if found == 0:
            print(f"Word {q} not found in titles")
        else:
            print(f"{found} news items were found and recorded in the file")
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(records, file, ensure_ascii=False, indent=4)