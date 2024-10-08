from flask import Flask, render_template, request
from datetime import datetime
import json

app = Flask(__name__)

# Load news data from JSON file
def load_news_data():
    with open('news_data.json', 'r') as file:
        news_data = json.load(file)
    return news_data

# Extract unique topics for the topic cloud
def extract_topics(news_data):
    topics = set()
    for date, news_items in news_data.items():
        for item in news_items:
            topics.add(item['topic'])
    return sorted(topics)

@app.route('/')
def home():
    # Load news data from the JSON file
    news_by_date = load_news_data()
    all_topics = extract_topics(news_by_date)

    # Get the selected topic from query parameters (default is "all")
    selected_topic = request.args.get('topic', 'all')

    # Filter news items based on the selected topic
    if selected_topic != 'all':
        filtered_news = {}
        for date, news_items in news_by_date.items():
            filtered_news[date] = [item for item in news_items if item['topic'] == selected_topic]
        news_by_date = filtered_news

    # Get current and previous day for demonstration
    today = datetime.now().strftime("%d-%b-%y")
    yesterday = (datetime.now().replace(day=datetime.now().day - 1)).strftime("%d-%b-%y")

    # If today or yesterday do not exist in the data, add empty lists
    news_by_date.setdefault(today, [])
    news_by_date.setdefault(yesterday, [])

    return render_template('index.html', news_by_date=news_by_date, all_topics=all_topics, selected_topic=selected_topic, datetime=datetime)

if __name__ == '__main__':
    app.run(debug=True)
