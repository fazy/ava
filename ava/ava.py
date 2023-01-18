#!/usr/bin/env python3

import argparse
import os
import sys

from ava.chat import ChatClient
from ava.config import CHATBOT_NAME, CONFIG_DIR
from ava.profile import ProfileLoader
from typing import Dict, Any


def main():
    args = parse_args()
    api_key = get_openai_api_key()

    profile_loader = ProfileLoader(args['profile_dir'])
    try:
        profile = profile_loader.read_profile(args['profile'])
    except RuntimeError as e:
        exit_with_error(e)

    client = ChatClient(api_key, profile)

    if args['interactive']:
        if not sys.stdin.isatty():
            exit_with_error("Interactive mode requires stdin to be a terminal; "
                            "this could also be caused by piping stdin to this program.")
        client.converse_interactively()
    else:
        client.converse_non_interactively(
            profile, args['in_file'], args['out_file'])


def parse_args() -> Dict[str, Any]:
    parser = argparse.ArgumentParser(
        description=f'{CHATBOT_NAME}: CLI tool for interacting with OpenAI\'s chat.')
    parser.add_argument(
        '--profile',
        help='Select which configuration profile to use. If not specified, the default profile is used.')
    parser.add_argument(
        '--profile-dir', default=f"{CONFIG_DIR}/profiles",
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


def exit_with_error(message):
    print(message)
    sys.exit(1)


if __name__ == '__main__':
    main()
