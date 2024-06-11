import os
import csv
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from flask import Flask, render_template, request


f = open("Passwords.txt", "r")
passwords = list(csv.reader(f, delimiter=","))
api_base = passwords[0][0]
api_key= passwords[1][0]
deployment_name = passwords[2][0]
api_version = "2024-02-01"



def image_response(url):
    client = AzureOpenAI(
        api_key=api_key,
        api_version=api_version,
        base_url=f"{api_base}/openai/deployments/{deployment_name}"
    )

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": [
                {
                    "type": "text",
                    "text": "Describe the following image with 20 words in Chinese"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": url
                    }
                }
            ]}
        ],
        max_tokens=2000
    )

    return response.choices[0].message.content



app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')

    url = request.form.get('url')
    return render_template(
        'index.html',
        response = image_response(url),
        image = url)


if __name__ == '__main__':
    app.run()


