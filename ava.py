#!/usr/bin/env python3

"""Command line tool that uses the OpenAI library to interact with their chat API

Usage:
    ava.py [--profile=<profile>] [--out-file=<out-file>] [--interactive]
where:
    --profile is the name of the configuration profile to use; if not specified, the default profile is used
    --in-file is an optional file to write the message from, otherwise stdin is used; it cannot be used with --interactive
    --out-file is an optional file to write the response to, otherwise stdout is used
    --interactive causes the program to not exit but read the next message from stdin; it cannot be used with --in-file

To use profiles, copy the profiles from example-profiles to ~/.ava/profiles. Each profile configures the model and includes a template for the initial prompt. The placeholder {{__INPUT__}} is replaced with the user's input (file, stdin or interactive prompt).

The default profile is used if no profile is specified. A profile needn't have all the settings, which are inherited in order:

- ~/.ava/profiles/<profile>.toml (if specified)
- ~/.ava/profiles/default.toml
- the built-in default

The config file is expected to be at ~/.ava/config and should be in the format (shown here with defaults):

```
[config]
engine = "text-davinci-003"
temperature = 0.7
n = 1
frequency_penalty = 0
presence_penalty = 0
max_tokens = 2000
```
"""

import argparse
import openai
import os
import sys
import toml

from typing import Dict, Any

CHATBOT_NAME = 'Ava'
CONFIG_DIR = os.path.expanduser('~/.ava')


def main():
    args = parse_args()
    openai.api_key = get_openai_api_key()

    profile = read_profile(args['profile'])

    if args['interactive']:
        if not sys.stdin.isatty():
            exit_with_error("Interactive mode requires stdin to be a terminal; "
                            "this could also be caused by piping stdin to this program.")

        converse_interactively(profile)
    else:
        first_user_input = read_first_user_input(args)
        response = prompt(first_user_input, profile)
        write_output(args, response)


def exit_with_error(message):
    print(message)
    sys.exit(1)


def read_profile(profile: str) -> Dict[str, Any]:
    config = {
        "engine": "text-davinci-003",
        "temperature": 0.3,
        "n": 1,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "max_tokens": 1000,
        "prompt_template": "{{__INPUT__}}"
    }

    if os.path.exists(get_profile_path("default")):
        merge_config_from_file(config, "default")

    if profile != 'default' and profile is not None:
        merge_config_from_file(config, profile)

    return config


def merge_config_from_file(config: Dict, profile: str) -> Dict:
    profile_file_path = get_profile_path(profile)
    try:
        with open(profile_file_path) as f:
            config.update(
                {k: v for k, v in toml.load(f).items() if k in config})
    except:
        exit_with_error(
            f"Error reading profile {profile}, file {profile_file_path}")

    return config


def get_profile_path(profile: str) -> str:
    if profile == 'default':
        return f"{CONFIG_DIR}/profiles/default.toml"
    else:
        return f"{CONFIG_DIR}/profiles/{profile}.toml"


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


def converse_interactively(profile: Dict):
    conversation = ''

    print(f">>> Enter your first message. A blank message ends the conversation.\n")
    while True:
        user_input = input("You:\n")
        if user_input == '':
            break
        conversation += '\n\n' + user_input

        response = prompt(conversation, profile)
        print(f"\n{CHATBOT_NAME}:\n{format_response(response)}")
        conversation += '\n\n' + get_response_text(response)


def read_first_user_input(args: Dict[str, Any]):
    if args['in_file'] is not None:
        with open(args['in_file'], 'r') as f:
            return f.read()
    else:
        return sys.stdin.read()


def prompt(prompt: str, profile: Dict) -> str:
    return openai.Completion.create(
        engine=profile['engine'],
        prompt=render_prompt(profile['prompt_template'], prompt),
        temperature=profile['temperature'],
        n=profile['n'],
        frequency_penalty=profile['frequency_penalty'],
        presence_penalty=profile['presence_penalty'],
        max_tokens=profile['max_tokens'],
    )


def render_prompt(prompt_template: str, user_input: str) -> str:
    return prompt_template.replace('{{__INPUT__}}', user_input)


def parse_args() -> Dict[str, Any]:
    parser = argparse.ArgumentParser(
        description=f'{CHATBOT_NAME}: CLI tool for interacting with OpenAI\'s chat.')
    parser.add_argument(
        '--profile',
        help='Select which configuration profile to use. If not specified, the default profile is used.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--in-file', help='An optional file to write the message from')
    group.add_argument('--interactive', help='If specified, don\'t exit but read the next message from stdin',
                       action='store_true')
    parser.add_argument(
        '--out-file', help='An optional file to write the response to')

    args = parser.parse_args()

    if sys.stdin.isatty():
        if not args.in_file and not args.interactive:
            parser.error(
                'At least one of --in-file or --interactive must be specified')

    return vars(args)


def get_openai_api_key():
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        raise Exception('OPENAI_API_KEY environment variable is not set')
    return api_key


if __name__ == '__main__':
    main()
