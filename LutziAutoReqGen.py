import ast
import os
import time
from tkinter import Tk, filedialog as fd
from tkinter.filedialog import askopenfilename, asksaveasfilename
import re
from tkinter import filedialog
from tkinter import messagebox
import subprocess
import sys
try:
    from colorama import Fore
    from prettytable import PrettyTable
except Exception as e:
    os.system("pip install colorama==0.4.4")
    os.system("pip install prettytable==3.11.0")
    time.sleep(5)
def get_imports_from_file(file_path):
    """Extract all imported module names from a Python file."""
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read(), filename=file_path)

    imports = set()

    # Iterate through all nodes in the AST
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split('.')[0])  # Get the module name
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split('.')[0])  # Get the module name

    imports.discard('')  # Remove empty strings (in case of invalid imports)
    return imports

def parse_requirements_file(req_file_path):
    """Parse the requirements.txt file and return a dictionary of package names and versions."""
    package_dict = {}
    with open(req_file_path, 'r') as req_file:
        for line in req_file:
            line = line.strip()
            if line and not line.startswith('#'):  # Skip empty lines and comments
                match = re.match(r'([^=]+)==(.+)', line)
                if match:
                    package_name = match.group(1).lower()  # Normalize to lowercase
                    package_version = match.group(2)
                    package_dict[package_name] = package_version

    return package_dict

def generate_filtered_requirements(imports, installed_packages):
    """Generate the filtered requirements.txt content based on detected imports."""
    requirements = []
    matched_imports = []

    for module in imports:
        package_name = module.lower()  # Normalize the import name to lowercase for comparison
        if package_name in installed_packages:
            version = installed_packages[package_name]
            requirements.append(f"{package_name}=={version}")
        else:
            matched_imports.append(module)  # Note the unmatched imports

    return requirements, matched_imports

def install_requirements():
    """Install the filtered requirements.txt using pip."""
    try:
        subprocess.check_call([os.sys.executable, "-m", "pip", "install", "-r", "filtered_requirements.txt"])
        print("Requirements successfully installed.")
    except subprocess.CalledProcessError as e:
        print("Failed to install requirements:", e)

def main():
    # Step 1: Ask the user to select the main Python project file
    window = Tk()
    window.withdraw()
    file_path = askopenfilename(filetypes=[("Python files", "*.py")])

    if file_path and os.path.isfile(file_path):
        # Step 2: Extract the imports from the selected Python file
        imports = get_imports_from_file(file_path)
        print(f"Detected imports: {imports}")

        # Step 3: Ask for the pre-generated requirements.txt file
        req_file_path = askopenfilename(title="Select requirements.txt", filetypes=[("Text files", "*.txt")])

        if req_file_path and os.path.isfile(req_file_path):
            # Step 4: Parse the pre-generated requirements.txt to get all installed packages
            installed_packages = parse_requirements_file(req_file_path)
            print(f"Installed packages: {installed_packages}")

            # Step 5: Compare imports with installed packages and generate a filtered requirements.txt
            requirements, matched_imports = generate_filtered_requirements(imports, installed_packages)
            print(f"Filtered requirements: {requirements}")

            # List of Python's built-in modules (for Python 3.x)
            builtin_modules = set(sys.builtin_module_names)

            # Step 6: Write the filtered requirements and unmatched imports to a new file
            with open("filtered_requirements.txt", "w") as f:
                # Write the matched requirements with versions
                for req in requirements:
                    f.write(req + "\n")

                # Write the unmatched imports, along with their versions if found in the original requirements.txt
                for imp in matched_imports:
                    imp_lower = imp.lower()  # Normalize to lowercase

                    # Ignore built-in modules
                    if imp_lower in builtin_modules:
                        continue

                    # Check if the package is in the installed_packages (parsed from requirements.txt)
                    if imp_lower in installed_packages:
                        version = installed_packages[imp_lower]
                        f.write(f"{imp}=={version}\n")  # Write the unmatched import with its version if available
                    else:
                        # In case the import was not found at all in requirements.txt
                        f.write(f"{imp}\n")

            # Step 7: Warn about any unmatched imports
            if matched_imports:
                print("\nWarning: The following imports were not matched to any packages in requirements.txt:")
                table = PrettyTable(["Unmatched Imports"])
                for imp in matched_imports:
                    table.add_row([imp])
                print(table)
            else:
                print("\nAll imports were matched successfully!")

            # Step 8: Ask the user if they want to install the requirements
            install_choice = input("Would you like to install the filtered requirements now? (y/n): ").lower()
            if install_choice == 'y':
                install_requirements()
            else:
                print("You chose not to install the requirements now.")
        else:
            print("No valid requirements.txt file selected.")
    else:
        print("No valid Python file selected.")


import tkinter as tk
from tkinter import filedialog


def read_file_with_encoding(file_path):
    """Attempt to read a file with multiple encodings."""
    encodings = ['utf-8', 'utf-16', 'latin-1']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return {line.strip() for line in file if line.strip()}
        except UnicodeDecodeError:
            continue
    raise ValueError("Unsupported file encoding")


def extract_base_words(lines):
    """Extract the base words (before '==') from the lines."""
    base_words = {}
    for line in lines:
        if '==' in line:
            base_word = line.split('==')[0].strip()
            base_words[base_word] = line
        else:
            base_word = line.strip()
            base_words[base_word] = None
    return base_words


def find_matching_lines(file1_path, file2_path, file3_path):
    """Find lines in file1 that are also in file2 and save them to file3."""
    try:
        # Read the content of file1 and file2 with proper encoding
        file1_lines = read_file_with_encoding(file1_path)
        file2_lines = read_file_with_encoding(file2_path)

        # Extract base words from file2 lines
        file2_base_lines = extract_base_words(file2_lines)

        # Find matching lines and build the output
        output_lines = []
        for word in file1_lines:
            if word in file2_base_lines:
                # Get the full line from file2
                full_line = file2_base_lines[word]
                if full_line:  # There is a version number
                    output_lines.append(full_line)
                    output_lines.append(file2_base_lines.get(word, word))
                else:  # Just a word, no version number
                    # Ensure to get the longer line if exists
                    output_lines.append(file2_base_lines.get(word, word))

        # Write the matching lines to file3
        with open(file3_path, 'w', encoding='utf-8') as file3:
            for line in output_lines:
                file3.write(line + '\n')

        print(f"Matching lines have been written to {file3_path}")

    except Exception as e:
        print(f"An error occurred: {e}")


def select_files():
    """Open file dialogs to select the files and perform the comparison."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Select the source file (file1)
    file1_path = filedialog.askopenfilename(title="Select the first file (filtered_requirements.txt file)", filetypes=[("Text files", "*.txt")])
    if not file1_path:
        print("No first file selected.")
        return

    # Select the second file (file2) for comparison
    file2_path = filedialog.askopenfilename(title="Select the second file (requirements.txt again)", filetypes=[("Text files", "*.txt")])
    if not file2_path:
        print("No second file selected.")
        return

    # Select the destination file (file3) to save matching lines
    file3_path = filedialog.asksaveasfilename(title="Save the matching lines as", defaultextension=".txt",
                                              filetypes=[("Text files", "*.txt")])
    if not file3_path:
        print("No destination file selected.")
        return

    # Find and save matching lines
    find_matching_lines(file1_path, file2_path, file3_path)


if __name__ == "__main__":
    print(Fore.MAGENTA+ "This script author by LutziGoz to Provide ability that calculate and provide specific requirements.txt for project that for share opensource project with others\m\nFirst build environment and i will to handle by requirements.txt are needed."
          "\non main project and main python environment where the project running, use by freeze command to build requirements.txt then entered to python environment folder\n then run the script\n\n")
    print(Fore.LIGHTCYAN_EX+ "1. First Choose python file main project\n2. for this step choose requirements.txt with entire packages\n3. for The Third step choose the filtered_requirements.txt file(Will Generated after chosen Requirements.txt for entire packages)\n4. at this point choose the requirements.txt again\n5. step and last step choose output.txt")
    main()
    select_files()

