import os
import re


def create_project_from_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split content using section delimiter
    sections = re.split(r'^-{10,}$', content, flags=re.MULTILINE)

    for section in sections:
        if not section.strip():
            continue

        # Split into header and code
        parts = section.strip().split('\n', 1)
        if len(parts) < 2:
            continue

        header, code = parts

        # Extract file path from header
        match = re.match(r'^\d+\.\s+(`?)(.*?)\1$', header.strip())
        if not match:
            continue

        file_path = match.group(2).strip()

        # Remove code block markers (e.g., ```)
        code = re.sub(r'^```\w*\n|```$', '', code.strip(), flags=re.MULTILINE)

        # Create directory structure
        dir_path = os.path.dirname(file_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

        # Write file content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)
        print(f"Created: {file_path}")

    print("\nProject structure created successfully!")


if __name__ == "__main__":
    input_file = input("Enter path to project structure text file: ")
    if os.path.exists(input_file):
        create_project_from_text(input_file)
    else:
        print("File not found. Please check the path and try again.")
