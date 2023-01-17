import openai

from config import CHATBOT_NAME
from typing import Dict, Any


class ChatClient():
    def __init__(self, api_key: str, profile: Dict):
        openai.api_key = api_key
        self.profile = profile

    def converse_non_interactively(self, in_file: str, out_file: str):
        first_user_input = read_first_user_input(in_file)
        response = self.prompt(first_user_input)
        write_output(out_file, response)

    def converse_interactively(self):
        conversation = ''

        print(f">>> Enter your first message. A blank message ends the conversation.\n")
        while True:
            user_input = input("You:\n")
            if user_input == '':
                break
            conversation += '\n\n' + user_input

            response = self.prompt(conversation)
            print(f"\n{CHATBOT_NAME}:\n{format_response(response)}")
            conversation += '\n\n' + get_response_text(response)

    def prompt(self, prompt: str) -> str:
        return openai.Completion.create(
            engine=self.profile['engine'],
            prompt=render_prompt(self.profile['prompt_template'], prompt),
            temperature=self.profile['temperature'],
            n=self.profile['n'],
            frequency_penalty=self.profile['frequency_penalty'],
            presence_penalty=self.profile['presence_penalty'],
            max_tokens=self.profile['max_tokens'],
        )


def render_prompt(prompt_template: str, user_input: str) -> str:
    return prompt_template.replace('{{__INPUT__}}', user_input)


def format_response(response: Dict) -> str:
    message = get_response_text(response)
    return message.lstrip().rstrip() + "\n"


def get_response_text(response) -> str:
    return response['choices'][0]['text']


def read_first_user_input(args: Dict[str, Any]):
    if args['in_file'] is not None:
        with open(args['in_file'], 'r') as f:
            return f.read()
    else:
        return sys.stdin.read()


def write_output(args: Dict[str, Any], response: str):
    formatted = format_response(response)

    if args['out_file']:
        with open(args['out_file'], 'w') as f:
            f.write(formatted)
    else:
        print(formatted)
