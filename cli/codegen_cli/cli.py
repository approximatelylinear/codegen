
import argparse
import os
from pathlib import Path

from codegen.lib.generate import generate_openai_code

# Function to color text as red
def color_red(text):
    return f"\033[91m{text}\033[0m"

# Function to color text as cyan
def color_cyan(text):
    return f"\033[96m{text}\033[0m"

def get_language(file):
    if file.endswith('.py'):
        return 'python'
    elif file.endswith('.js'):
        return 'javascript'
    elif file.endswith('.toml'):
        return 'toml'
    elif file.endswith('.jsx'):
        return 'jsx'
    elif file.endswith('.css'):
        return 'css'
    elif file.endswith('.html'):
        return 'html'
    else:
        return 'plaintext'

def read_code(file):
    try:
        if os.path.isdir(file):
            file_contents = ''
            p = Path(file)
            print(f"{color_cyan('Reading directory')} {file}...")
            for child in p.rglob('*'):
                if 'pycache' in str(child):
                    continue
                if not (child.name.endswith('.py') or child.name.endswith('.js') or child.name.endswith('.toml')):
                    continue
                if child.is_file():
                    print(f"{color_cyan('Adding contents of')} {child}...")
                    with open(child) as f:
                        contents = f.read()[:3000]
                        if contents.strip():
                            file_contents += f"\n\n<file>{child}</file>\n```{get_language(file)}\n{contents}\n```\n"
            return file_contents
        else:
            with open(file) as f:
                print(f"{color_cyan('Adding contents of')}{file}...")
                contents = f.read()[:3000]
                return f"\n\n<file>{file}</file>\n```{get_language(file)}\n{contents}\n```\n"
    except Exception as e:
        print(f"Error reading file {file}: {e}")
        return ''


def main():
    parser = argparse.ArgumentParser(description='Call the function generate_openai_code with specified arguments')
    parser.add_argument('--problem', type=str, default=None, help='A string that describes the problem to be solved')
    parser.add_argument('--language', type=str, default='python', help='A string that specifies the programming language to be used (default: python)')
    parser.add_argument('--files', nargs='+', type=str, help='A list of strings that specify the files to be used')
    parser.add_argument('--code', type=str, help='A string that specifies existing code to reference')
    parser.add_argument('--output-dir', type=str, help='Output directory for generated code files')
    parser.add_argument('--problem-file', type=str, help='A file containing the problem statement. Can be used in place of providing a problem on the command-line.')

    args = parser.parse_args()

    code = args.code or ''

    problem = args.problem
    if args.problem_file:
        if problem:
            print(color_red("Both problem and problem-file provided. Using the problem provided on the command-line."))
        else:
            with open(args.problem_file) as f:
                print(f"{color_cyan('Reading problem statement from')} {args.problem_file}...")
                problem = f.read()
    if problem is None:
        print(color_red("Problem statement is required."))
        return

    if args.files:
        for file in args.files:
            code += read_code(file)

    result = generate_openai_code(problem=problem, language=args.language, files=args.files, code=code)
    print(color_red("\nGenerating code...\n"))

    if args.output_dir and not os.path.exists(args.output_dir):
        print(f"Directory '{args.output_dir}' does not exist.")
        create_dir = input("Do you want to create this directory? (y/N): ")
        if create_dir.lower().strip() in ('y'):
            os.makedirs(args.output_dir)
            print(f"Directory '{args.output_dir}' created.")
        else:
            print(color_red('Skipping directory creation...'))

    for item in result:
        print(color_red("Generated Code block:\n"))
        if item.get('filename'):
            print(f"{color_red('Filename')}: {item['filename']}")
        if item.get('language'):
            print(f"{color_red('Language')}: {color_red(item['language'])}")
        if item.get('code'):
            print(f"{color_red('Code')}:\n{item['code']}\n")
        if item.get('filename'):
            output_file = os.path.join(args.output_dir, item['filename'])
            save_file = input(f"Do you want to save the content to  {color_red(output_file)}? (y/N): ")
            if save_file.strip().lower() == 'y':
                with open(output_file, 'w') as f:
                    f.write(item['code'].strip() + '\n')
                    print(f"Code saved to {color_red(output_file)}")
            else:
                print(color_red(f"Did not save {color_red(item.get('filename'))}"))

if __name__ == "__main__":
    main()
