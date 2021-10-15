require "bundler/setup"
require "faraday"
require "nokogiri"
require "json"
require "dotenv"

Dotenv.load

# Twitter Analyticsの情報を取得するためのクラス
class TwitterAnalytics
  def initialize(username, auth_token)    
    @client = Faraday.new(url: "https://analytics.twitter.com/user/#{username}/home") do |req|
      req.headers["Cookie"] = "auth_token=#{auth_token}; lang=ja;"
    end
  end

  # データを取得
  def fetch_data(category, start_time, end_time)
    @client.get "#{category}.json?start_time=#{start_time}&end_time=#{end_time}"
  end
end

# 取得したいデータのカテゴリを指定
category = "summary"

# 取得開始日時と取得終了日時をUnixtimeで指定
start_time = 1631836800000
end_time = 1634256000000

# リクエストを送信
ta = TwitterAnalytics.new(ENV["TWITTER_USERNAME"], ENV["TWITTER_AUTH_TOKEN"])
res = ta.fetch_data(category, start_time, end_time)

# NokogiriでHTML解析
html = JSON.parse(res.body)["html"]
doc = Nokogiri::HTML(html)

# 各種データを取り出し
metrics = doc.css(".home-summary-metric")
tweets = metrics[0].attr("title")
tweet_views = metrics[1].attr("title")
profile_views = metrics[2].attr("title")
mentions = metrics[3].attr("title")
followers = metrics[4].attr("title")

heredoc = <<~EOS
  ツイート: #{tweets}
  ツイートインプレッション: #{tweet_views}
  プロフィールへのアクセス: #{profile_views}
  @ツイート: #{mentions}
  フォロワー数: #{followers}
EOS

puts heredoc
