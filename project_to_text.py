# this script will create a text file that contain all your oroject codes.
import os
from pathlib import Path

# Configuration
ALLOWED_EXTENSIONS = {'.py', '.md', '.yml', '.yaml', '.toml', '.env', '.gitignore', '.log'}
IGNORED_DIRS = {'.idea', '__pycache__'}
MAX_FILE_SIZE = 200 * 1024  # 200 KB in bytes
SCRIPT_NAME = Path(__file__).name


def is_allowed_file(path: Path) -> bool:
    return path.suffix in ALLOWED_EXTENSIONS


def should_ignore_dir(dir_name: str) -> bool:
    return dir_name in IGNORED_DIRS


def gather_project_info(root_path: Path):
    files = []
    empty_dirs = []
    project_name = root_path.name
    root_path = root_path.resolve()

    for dirpath, dirnames, filenames in os.walk(root_path, topdown=True):
        # Filter ignored directories
        dirnames[:] = [d for d in dirnames if not should_ignore_dir(d)]

        # Process files
        for filename in filenames:
            file_path = Path(dirpath) / filename
            if file_path.name == SCRIPT_NAME:
                continue  # Skip the script itself

            try:
                # Skip files larger than MAX_FILE_SIZE
                if file_path.stat().st_size > MAX_FILE_SIZE:
                    continue
            except Exception as e:
                print(f"⚠️ Error checking size for {file_path}: {str(e)}")
                continue

            # Calculate relative path with project name prefix
            try:
                relative_path = file_path.relative_to(root_path.parent)
                if str(relative_path).startswith(project_name):
                    full_relative = relative_path.as_posix()
                else:
                    full_relative = f"{project_name}/{relative_path.as_posix()}"
            except ValueError:
                full_relative = f"{project_name}/{file_path.name}"

            files.append((full_relative, file_path))

        # Check for empty directories
        if not filenames and not dirnames:
            try:
                dir_rel_path = Path(dirpath).relative_to(root_path.parent)
                formatted_path = dir_rel_path.as_posix()
                if not formatted_path.startswith(project_name):
                    formatted_path = f"{project_name}/{formatted_path}"
            except ValueError:
                formatted_path = f"{project_name}/{Path(dirpath).name}"

            if not any(part in IGNORED_DIRS for part in formatted_path.split('/')):
                empty_dirs.append(formatted_path)

    return files, empty_dirs


def main():
    root_folder = input("Enter project root folder path: ").strip()
    root_path = Path(root_folder)

    if not root_path.exists():
        print("❌ Invalid path!")
        return

    project_name = root_path.name
    files, empty_dirs = gather_project_info(root_path)
    output_file = f"{project_name}.txt"

    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Process files
        for full_relative, full_path in files:
            try:
                header = f"### File: {full_relative}\n"

                if is_allowed_file(full_path):
                    with open(full_path, 'r', encoding='utf-8') as infile:
                        content = infile.read()
                    outfile.write(header + content + "\n\n")
                else:
                    outfile.write(f"# File: {full_relative}\n\n")

            except UnicodeDecodeError:
                outfile.write(f"# File: {full_relative} (binary/non-text file)\n\n")
            except Exception as e:
                print(f"⚠️ Error processing {full_relative}: {str(e)}")

        # Process empty directories
        if empty_dirs:
            outfile.write("\n\n### Empty Directories\n")
            for dir_path in empty_dirs:
                outfile.write(f"# Empty Directory: {dir_path}\n")

    print(f"✅ Successfully created {output_file}!")


if __name__ == "__main__":
    main()
