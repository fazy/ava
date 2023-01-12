#!/usr/bin/env python3

"""Command line tool that uses the OpenAI library to interact with their chat API

Usage:
    ava.py [--prompt=<prompt>] [--out-file=<out-file>] [--interactive]
where:
    --prompt is an optional prompt to send before the message (if supplied, multiple will can be used, in order)
    --in-file is an optional file to write the message from, otherwise stdin is used; it cannot be used with --interactive
    --out-file is an optional file to write the response to, otherwise stdout is used
    --interactive causes the program to not exit but read the next message from stdin; it cannot be used with --in-file

The config file is expected to be at ~/.ava/config and should be in the format (shown here with defaults):

```
[config]
engine = "text-davinci-003"
temperature = 0.7
n = 1
frequency_penalty = 0
presence_penalty = 0
max_tokens = 3200
```
"""

import argparse
import openai
import os
import sys
import toml

from typing import Dict, Any

CHATBOT_NAME = 'Ava'


def main():
    args = parse_args()
    config = load_config()
    openai.api_key = get_openai_api_key()

    if args['interactive']:
        if not sys.stdin.isatty():
            exit_with_error("Interactive mode requires stdin to be a terminal; "
                            "this could also be caused by piping stdin to this program.")

        converse_interactively(config)
    else:
        first_user_input = read_first_user_input(args)
        response = prompt(first_user_input, config)
        write_output(args, response)


def exit_with_error(message):
    print(message)
    sys.exit(1)


def write_output(args: Dict[str, Any], response: str):
    formatted = format_response(response)

    if args['out_file']:
        with open(args['out_file'], 'w') as f:
            f.write(formatted)
    else:
        print(formatted)


def format_response(response: Dict) -> str:
    message = get_response_text(response)
    return message.lstrip().rstrip() + "\n"


def get_response_text(response) -> str:
    return response['choices'][0]['text']


def converse_interactively(config):
    conversation = ''

    print(f">>> Enter your first message. A blank message ends the conversation.\n")
    while True:
        user_input = input("You:\n")
        if user_input == '':
            break
        conversation += '\n\n' + user_input

        response = prompt(conversation, config)
        print(f"\n{CHATBOT_NAME}:\n{format_response(response)}")
        conversation += '\n\n' + get_response_text(response)


def read_first_user_input(args: Dict[str, Any]):
    if args['in_file'] is not None:
        with open(args['in_file'], 'r') as f:
            return f.read()
    else:
        return sys.stdin.read()


def prompt(prompt: str, config: Dict) -> str:
    return openai.Completion.create(
        engine=config['engine'],
        prompt=prompt,
        temperature=config['temperature'],
        n=config['n'],
        frequency_penalty=config['frequency_penalty'],
        presence_penalty=config['presence_penalty'],
        max_tokens=config['max_tokens'],
    )


def load_config():
    config = {
        'engine': 'text-davinci-003',
        'temperature': 0.7,
        'n': 2,
        'frequency_penalty': 0,
        'presence_penalty': 0,
        'max_tokens': 3200
    }

    try:
        with open(os.path.expanduser('~/.ava/config'), 'r') as f:
            data = toml.load(f)

            if data.get('config'):
                config.update(data['config'])

    except FileNotFoundError:  # no config file found, use defaults
        pass

    return config


def parse_args() -> Dict[str, Any]:
    parser = argparse.ArgumentParser(
        description=f'{CHATBOT_NAME}: CLI tool for interacting with OpenAI\'s chat.')
    parser.add_argument(
        '--prompt', help='An optional prompt to send before the message (if supplied, multiple can be used, in order)')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--in-file', help='An optional file to write the message from')
    group.add_argument('--interactive', help='If specified, don\'t exit but read the next message from stdin',
                       action='store_true')
    parser.add_argument(
        '--out-file', help='An optional file to write the response to')

    args = parser.parse_args()

    return vars(args)


def get_openai_api_key():
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        raise Exception('OPENAI_API_KEY environment variable is not set')
    return api_key


if __name__ == '__main__':
    main()
