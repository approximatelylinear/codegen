
import os
import re
from textwrap import dedent

from codegen.lib.openai import client as openai_client

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(THIS_DIR, '..', 'templates')

CODE_PATTERN = re.compile("""(?:
   (?:\[\[file\]\](?P<filename>.+)\[\[\/file\]\]\s*)
   (?:\[\[code\]\]
     \s*\[\[lang\]\](?P<lang>.+?)\[\[\/lang\]\]
     \s*(?P<code>.+)
   \[\[\/code\]\])
)""", flags=re.VERBOSE|re.DOTALL)


def generate_code(generator, problem, language, files=None, code=None):
    with open(os.path.join(TEMPLATE_DIR, 'code.tmpl')) as f:
        template = f.read()

    system_prompt = template.format(
        language=language,
        files=files or 'No files provided',
        code=code or 'No code provided'
    )

    user_prompt = f"Please solve the following problem by generating code using {language}:\n{problem}"

    message = generator.generate(
        system_prompt=system_prompt,
        user_prompt=user_prompt
    )

    return message


def generate_openai_code(problem, language, files=None, code=None):
    generator = openai_client.Generator()
    files = (files or '')[:500]
    code = (code or '')[:5000] # TODO: use tiktoken to split code into tokens and get token count
    response = generate_code(generator, problem, language, files, code)
    print(f"Response: {response}")
    print("\nParsing code response...\n")
    return parse_code_response(response)


def parse_code_response(response):
    return match_all(CODE_PATTERN, response)


def match_all(pattern, text):
    return [ m.groupdict() for m in re.finditer(pattern, text) ]


def test():
    """
    from codegen.lib.generate import generate_openai_code
    """
    problem = dedent("""
    Write a command-line interface to this Python program:

    Purpose: Call the function `generate_openai_code` with the following arguments:
        - problem: A string that describes the problem to be solved
        - language: A string that specifies the programming language to be used (default: 'python')
        - files: A list of strings that specify the files to be used (optional)
        - code: A string that specifies existing code to reference (optional)
    """)
    code = generate_openai_code(problem, 'python')
    return code


def test_parse():
    with open(os.path.join(THIS_DIR, 'test_file.txt')) as f:
        text = f.read()
        import pdb; pdb.set_trace()
        return parse_code_response(text)
