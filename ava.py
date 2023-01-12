#!/usr/bin/env python3

"""Command line tool that uses the OpenAI library to interact with their chat API

Usage:
    ava.py [--prompt=<prompt>] [--out-file=<out-file>] [--interactive]
where:
    --prompt is an optional prompt to send before the message (if supplied, multiple will can be used, in order)
    --in-file is an optional file to write the message from, otherwise stdin is used
    --out-file is an optional file to write the response to, otherwise stdout is used
    If --interactive is specified, don't exit but read the next message from stdin

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


def main():
    args = parse_args()
    config = load_config()
    print(config)

    openai.api_key = get_openai_api_key()
    input = read_input(args)
    response = prompt(input, config)
    print(response)


def read_input(args: Dict[str, Any]):
    if args['in_file']:
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
        description='Send a message to the openai chat API')
    parser.add_argument(
        '--prompt', help='An optional prompt to send before the message (if supplied, multiple will can be used, in order)')
    parser.add_argument(
        '--in-file', help='An optional file to write the message from')
    parser.add_argument(
        '--out-file', help='An optional file to write the response to')
    parser.add_argument(
        '--interactive', help='If specified, don\'t exit but read the next message from stdin', action='store_true')

    args = parser.parse_args()
    return vars(args)


def get_openai_api_key():
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        raise Exception('OPENAI_API_KEY environment variable is not set')
    return api_key


if __name__ == '__main__':
    main()
