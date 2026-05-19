import requests
from groq import Groq  

# Step 1 — get raw news
def get_news(topic):
    api_key='Api_key'
    url=f'https://newsapi.org/v2/everything?q={topic}&apiKey={api_key}&pageSize=5'
    response=requests.get(url)
    data=response.json()
    return data  

# Step 2 — extract only titles
def extract_headlines(news):
    articles=news['articles']
    headline=[]
    for article in articles:
        headline.append(article['title'])
    return headline

# Step 3 — send titles to AI
def generate_briefing(headlines):
    client=Groq(api_key='your api_key')
    prompt=f'Based on this headlines list: {headlines} generate 3 point briefing'
    response=client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[{'role':'user', 'content':prompt}]
    )
    return response.choices[0].message.content

# Step 4 — save to file
def save_briefing(topic, briefing):
    filename=f'{topic}_briefing.txt'
    with open(filename, 'w') as file:
        file.write(f'Topic: {topic}\n')
        file.write('='*50 + '\n')
        file.write(briefing)
    print(f'Briefing saved to {filename}')
       
topic=input('Enter you topic: ')
news=get_news(topic)
headlines=extract_headlines(news)
briefing=generate_briefing(headlines)  
print(briefing)
save_briefing(topic, briefing)















































#   response=requests.get(url)
#     data=response.json()
#     return data

# def extract_headlines(news):
#     articles=news['articles']
#     for article in articles:
#         print(article['title'])
#         print(article['description'])
#         print('-----') 

# topic=input("Enter your topic: ")
# news=get_news(topic)
# extract_headlines(news)