from groq import Groq


def get_api(prompt):
    client = Groq(api_key='api key')
    response = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[{'role': 'user', 'content': prompt}]
    )
    return response.choices[0].message.content


def save_file(content):
    filename = 'AI_quote.txt'
    with open(filename, 'w') as file:
        file.write(content + '\n')
        file.write('='*50 +'\n')


topic = input('Enter your motivational topic: ')
prompt = f"Give me motivational quote about {topic}"
quote = get_api(prompt)
print(quote)
save_file(quote)


