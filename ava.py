#!/usr/bin/env python3

"""Command line tool that uses the OpenAI library to interact with their chat API

Usage:
    ava.py [--prompt=<prompt>] [--out-file=<out-file>] [--interactive]
where:
    --prompt is an optional prompt to send before the message (if supplied, multiple will can be used, in order)
    --in-file is an optional file to write the message from, otherwise stdin is used
    --out-file is an optional file to write the response to, otherwise stdout is used
    If --interactive is specified, don't exit but read the next message from stdin
"""

import argparse
from typing import Dict, Any

def main():
    config = parse_args()
    print(config)


def parse_args() -> Dict[str, Any]:
    parser = argparse.ArgumentParser(description='Send a message to the openai chat API')
    parser.add_argument('--prompt', help='An optional prompt to send before the message (if supplied, multiple will can be used, in order)')
    parser.add_argument('--in-file', help='An optional file to write the message from')
    parser.add_argument('--out-file', help='An optional file to write the response to')
    parser.add_argument('--interactive', help='If specified, don\'t exit but read the next message from stdin', action='store_true')

    args = parser.parse_args()
    return vars(args)


if __name__ == '__main__':
    main()
