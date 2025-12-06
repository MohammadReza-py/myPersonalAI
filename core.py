import re
from openai import OpenAI
from urllib.request import urlopen

class AgentCore:
    def __init__(self, api_token, model):
        self.api_token = api_token
        self.model = model
        self.client = OpenAI(api_key=self.api_token, base_url="https://api.metisai.ir/openai/v1")

    def extract_links(self, text):
        pattern = r'https?://[^\s"]+'
        links = re.findall(pattern, text)
        return links

    def capture_the_flag(self, question):
        if self.extract_links(question.get('content')):
            link = self.extract_links(question.get('content'))[0]
            page = urlopen(link)
            html_bytes = page.read()
            html = html_bytes.decode("utf-8")
            question = question.get('content').replace(link, html)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[question],  # [{"role": "user", "content": f"calculate {question}. just print answer"}],
            max_tokens=100,
            temperature=0.1
        )
        return response.choices[0].message.content.strip()