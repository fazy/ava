# Ava: Experimental Command Line Tool for Interacting with OpenAI's Chat

**Note: This is an experimental tool and not connected with OpenAI. Use at your own cost and risk. Whether or not I maintain it depends on whether I find it useful in practice, but feel free to fork.**

Ava is a command line tool for interacting with OpenAI's chat API. It is primarily intended for providing one-off responses to perform a specific task, specified in a profile config file. There is a rudimentary interactive mode to help test profiles, but other tools do this better and it probably won't get much attention.

## Example uses

* Pipe in text from any source and get a summary:
  `cat input.txt | ava --profile=text-summary`
* Document your code:
  `ava --profile=code-doc --in-file=code.py --out-file=generated_doc.md`

You can create your own profiles to suit your needs. See the [profiles](#profiles) section for more details.

## Limitations

- It only works on moderatly small input files owing to the models' token limits; output will be likewise limited
- Doens't even try to mitigate or handle the above gracefully (yet)
- All the limitations of the underlying OpenAI API; ability to spew out nonsense, etc. (at least you can tune the settings though)
- The example profiles are pretty basic, you'll need to create or tweak them

## Requirements

- Python 3
- OpenAI API key ([docs](https://beta.openai.com/docs/api-reference/authentication))

## Installation

### From source

1. Clone the repository:

```bash
git clone https://github.com/fazy/ava.git
cd ava
```

2. Build and install:

```bash
python -m build
pip install dist/ava-0.1-py3-none-any.whl
```

(if you don't have the build package installed, you can install it with `pip install build`)

3. Copy the profiles to your home directory:

```bash
cp -r example-profiles ~/.ava/profiles
```

Then edit them to suit your needs.

## Usage

For usage details:

`ava --help`

### Non-interactive mode

Provide input on stdin or with the `--in-file` flag:

`ava --in-file=<in-file>`

By default output is sent to stdout. You can also use the --out-file flag to write the response to a file:

`ava --out-file=<out-file>`

You can also specify a configuration profile to use with the `--profile` flag. These needs to be set up in your home directory first, see the [profiles](#profiles) section for more details:

`ava --profile=<profile>`

By default profilesa are loaded from `~/.ava/profiles`. Change the profiles directory with the `--profiles-dir` flag:

`ava --profiles-dir=<profiles-dir>`

### Interactive mode

To converse with the chatbot, use the `--interactive` flag.:

`ava --interactive`

As mentioned above, it's quite basic. You can only enter one line of text at a time. Enter a blank line to exit.

## Profiles

Ava supports profiles for configuring the model and including a template for the initial prompt. The placeholder `{{__INPUT__}}` is replaced with the user's input (file or stdin).

To use profiles, copy the profiles from example-profiles to `~/.ava/profiles`. The default profile is used if no profile is specified. A profile needn't have all the settings, which are inherited in order:

- `~/.ava/profiles/<profile>.toml` (if specified it must exist)
- `~/.ava/profiles/default.toml` (only used if exists)
- the built-in default

Each profile is a TOML file with the following settings, shown here with the built-in defaults:

```
[config]
engine = "text-davinci-003"
temperature = 0.7
n = 1
frequency_penalty = 0
presence_penalty = 0
max_tokens = 2000
prompt_template = "{{__INPUT__}}"
```

## TODO

Lots of things could be better, although there's no guarantee I'll get around to it:

- Handle large input files (truncating, batching?) along with showing token usage
- More complex cases? E.g. a prompt with two parts (data and instructions) or profile variables or similar?
- Improve the example profiles (the current ones were the first ones that worked at all)
- Better interactive mode (e.g. allow multi-line input)
- Housekeeping, build, test, error handling etc.

## Other

Apologies for the unoriginal name, neither myself nor the AI could agree on anything more unique. It is named after the character Ava from the movie Ex Machina.
