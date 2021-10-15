import os
import json
import requests
import textwrap
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

# Twitter Analyticsの情報を取得するためのクラス
class TwitterAnalytics:
  def __init__(self, username, auth_token):
      self.username = username
      self.auth_token = auth_token
 
  # データを取得
  def fetch_data(self, category, start_time, end_time):
      url = f"https://analytics.twitter.com/user/{self.username}/home/{category}.json?start_time={start_time}&end_time={end_time}"
      headers = { "Cookie": f"auth_token={self.auth_token}; lang=ja" }

      return requests.get(url, headers=headers)

# 取得したいデータのカテゴリを指定
category = "summary"

# 取得開始日時と取得終了日時をUnixtimeで指定
start_time = 1631836800000
end_time = 1634256000000

# リクエストを送信
ta = TwitterAnalytics(os.getenv("TWITTER_USERNAME"), os.getenv("TWITTER_AUTH_TOKEN"))
res = ta.fetch_data(category, start_time, end_time)

# BeautifulSoupでHTML解析
html = res.json()["html"]
soup = BeautifulSoup(html, "html.parser")

# 各種データを取り出し
metrics = soup.find_all("div", class_ = "home-summary-metric")
tweets = metrics[0]["title"]
tweet_views = metrics[1]["title"]
profile_views = metrics[2]["title"]
mentions = metrics[3]["title"]
followers = metrics[4]["title"]

heredoc = textwrap.dedent("""
    ツイート: {tweets}
    ツイートインプレッション: {tweet_views}
    プロフィールへのアクセス: {profile_views}
    @ツイート: {mentions}
    フォロワー数: {followers}
""").format(
    tweets        = tweets,
    tweet_views   = tweet_views,
    profile_views = profile_views,
    mentions      = mentions,
    followers     = followers
)

print(heredoc)
