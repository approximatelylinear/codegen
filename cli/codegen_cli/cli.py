
import argparse
import os

from codegen.lib.generate import generate_openai_code

def main():
    parser = argparse.ArgumentParser(description='Call the function generate_openai_code with specified arguments')
    parser.add_argument('problem', type=str, help='A string that describes the problem to be solved')
    parser.add_argument('--language', type=str, default='python', help='A string that specifies the programming language to be used (default: python)')
    parser.add_argument('--files', nargs='+', type=str, help='A list of strings that specify the files to be used')
    parser.add_argument('--code', type=str, help='A string that specifies existing code to reference')

    args = parser.parse_args()

    code = args.code or ''

    if args.files:
        for file in args.files:
            try:
                with open(file) as f:
                    contents = f.read()[:3000]
                    if file.endswith('.py'):
                        file_lang = 'python'
                    elif file.endswith('.js'):
                        file_lang = 'javascript'
                    elif file.endswith('.toml'):
                        file_lang = 'toml'
                    else:
                        file_lang = 'plaintext'
                    code += f"\n\n<file>{file}</file>\n```{file_lang}\n{contents}\n```\n"
                    files += f"\n{file}"
            except Exception as e:
                print(f"Error reading file {file}: {e}")

    result = generate_openai_code(args.problem, args.language, args.files, args.code)
    for item in result:
        print("Code block:")
        if item.get('filename'):
            print(f"Filename: {item['filename']}")
        if item.get('language'):
            print(f"Language: {item['language']}")
        if item.get('code'):
            print(f"Code:\n{item['code']}\n")
        print(item)

if __name__ == "__main__":
    main()
