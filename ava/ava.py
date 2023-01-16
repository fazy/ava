#!/usr/bin/env python3

import argparse
import openai
import os
import sys

from typing import Dict, Any
from profile import ProfileLoader

CHATBOT_NAME = 'Ava'
CONFIG_DIR = os.path.expanduser('~/.ava')


def main():
    args = parse_args()
    openai.api_key = get_openai_api_key()

    profile_loader = get_profile_loader(args['profile_dir'])
    try:
        profile = profile_loader.read_profile(args['profile'])
    except RuntimeError as e:
        exit_with_error(e)

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


def get_profile_loader(profile_dir: str) -> ProfileLoader:
    if profile_dir is None:
        profile_dir = f"{CONFIG_DIR}/profiles"

    return ProfileLoader(profile_dir)


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
    parser.add_argument(
        '--profile-dir',
        help='The directory where the profiles are stored. If not specified, the default is ~/.ava/profiles.'
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--in-file', help='An optional file to read the message from')
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
