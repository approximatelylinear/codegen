
from functools import cache

from openai import OpenAI

from codegen.settings import OPENAI_API_KEY

MODEL = "gpt-3.5-turbo"

@cache
def make_client():
    return OpenAI(api_key=OPENAI_API_KEY)


class Generator:
    def __init__(self, client=None, model=None):
        if client is None:
            self.client = make_client()
        else:
            self.client = client
        self.model = model or MODEL

    def generate(self, system_prompt, user_prompt=None):
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        if user_prompt:
            messages.append({"role": "user", "content": user_prompt})
        print(f"Messages: {messages}")
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )

        return completion.choices[0].message.content


def test():
    generator = Generator("gpt-3.5-turbo")
    print(generator.generate(
        "Compose a poem that explains the concept of recursion in programming."))


if __name__ == '__main__':
    test()