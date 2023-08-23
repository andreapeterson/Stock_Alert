from botocore.vendored import requests
import config
import json
import boto3

alphavantage_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "AMZN",
    "apikey": config.ALPHA_API_KEY}

news_parameters = {
    "sortBy": "relevancy",
    "apiKey": config.NEWS_API_KEY,
    "q": "Amazon"}


def lambda_handler(event, context):
    # SET-UP
    response = requests.get("https://www.alphavantage.co/query", params=alphavantage_parameters)
    response.raise_for_status()
    data = response.json()
    time_series_daily = data["Time Series (Daily)"]
    time_series_daily_list = [(key, value) for key, value in time_series_daily.items()]

    yesterday_closing_price = float(time_series_daily_list[1][1]["4. close"])
    day_before_yesterday_closing_price = float(time_series_daily_list[2][1]["4. close"])

    # MATH
    difference = abs(yesterday_closing_price - day_before_yesterday_closing_price)

    if difference > 0:
        emoji = "🔺"
    else:
        emoji = "🔻"

    percentage_difference = (difference / day_before_yesterday_closing_price) * 100

    # NEWS ALERT
    if percentage_difference > 5:
        response2 = requests.get("https://newsapi.org/v2/everything", params=news_parameters)
        response2.raise_for_status()
        data2 = response2.json()["articles"][:3]
        formatted_articles = [f"Headline: {article['title']}. \nBrief Description: {article['description']}" for article
                              in data2]
        for article in formatted_articles:
            client = boto3.client('sns')
            result = client.publish(TopicArn=config.TOPIC_ARN, Message=article,
                                    Subject=f"AMZN: {emoji}{percentage_difference}%")

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
