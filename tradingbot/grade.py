import pandas as pd
from textblob import TextBlob
from technical import technicalAnalysis

def analyze_sentiment(news):
    # Initialize variables to store the sentiment scores
    total_sentiment = 0
    num_articles = 0

    # Iterate over the articles
    for article in news:
        title = article.get("title", "")
        content = article.get("content", "")
        sentiment = analyze_sentiment_text(title + ' ' + content)
        total_sentiment += sentiment
        num_articles += 1

    # Calculate the average sentiment score
    avg_sentiment = total_sentiment / num_articles if num_articles > 0 else 0

    return avg_sentiment

def analyze_sentiment_text(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

def calculate_price_change(df):
    # Calculate price change as percentage
    price_change = (df['close'].iloc[-1] - df['close'].iloc[0]) / df['close'].iloc[0] * 100
    return price_change

def normalize_volume(volume, max_volume):
    # Normalize volume to range 0-1
    volume_normalized = volume / max_volume
    return volume_normalized

def normalize_sentiment(sentiment):
    # Normalize sentiment to range 0-1
    sentiment_normalized = (sentiment + 1) / 2
    return sentiment_normalized

def scale_grade(grade):
    # Scale the grade to the range 1-10
    scaled_grade = (grade + 1) * 4.5 + 1

    # Ensure the grade is within the range 1-10
    scaled_grade = max(1, min(10, scaled_grade))

    return scaled_grade

def grade_stock(df, volume, sentiment):
    # Define weights for different factors
    weight_price = 0.3
    weight_volume = 0.2
    weight_sentiment = 0.2
    weight_technical = 0.3  # New weight for technical analysis

    # Calculate price change as percentage
    price_change = (df['close'].iloc[-1] - df['close'].iloc[0]) / df['close'].iloc[0] * 100

    # Normalize volume to range 0-1
    volume_normalized = volume / df['volume'].max()

    # Normalize sentiment to range 0-1
    sentiment_normalized = (sentiment + 1) / 2

    # Perform technical analysis
    technical_df = technicalAnalysis(get_stock_data, symbol)  # Assuming you have access to this function

    # Example: Use RSI as a technical indicator
    rsi = technical_df['RSI'].iloc[-1]

    # Normalize technical indicator (you may need to adjust this based on the specific indicator)
    technical_normalized = rsi / 100

    # Calculate grade
    grade = (
        weight_price * price_change +
        weight_volume * volume_normalized +
        weight_sentiment * sentiment_normalized +
        weight_technical * technical_normalized
    ) / (weight_price + weight_volume + weight_sentiment + weight_technical)

    # Scale the grade to the range 1-10
    scaled_grade = scale_grade(grade)

    return scaled_grade

def buy_sell_signals(scaled_grade):
    if scaled_grade >= 8:
        return 'Buy'
    elif scaled_grade <= 2:
        return 'Sell'
    else:
        return 'Hold'
