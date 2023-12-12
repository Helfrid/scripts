#!/usr/bin/env python3

"""Create a Python project directory.
Script generates a new Python project directory with the following structure:
    project_name/
    ├── data/
    ├── docs/
    ├── notebooks/
    ├── src/
    │   ├── __init__.py
    │   └── main.py
    ├── tests/
    ├── scratch/
    ├── README.md
    ├── .gitignore
    └── LICENSE
Usage:  python new-project.py <project_name> [--python-version <version>]
        python new-project.py --help
Defaukt Python version is 3.11
if conda is selected as python version, no environment will be created and conda env needs
to be created manually. (alias create_cenv)
Example:
    $ new-project.py my_project
    $ new-project.py my_project --python-version 3.11
    $ new-project.py my_project --python-version conda
    $ new-project.py --help
"""

from pathlib import Path
import argparse
import shutil
import subprocess
import sys

# Parse the project name from command-line arguments
parser = argparse.ArgumentParser(description='Create a Python project directory.')
parser.add_argument('project_name', type=str, help='Name of the project')
parser.add_argument('--python-version', type=str, default='3.11',
                    help='Specify the Python version or Conda environment (e.g., "3.11", "conda"), default="3.11"')
args = parser.parse_args()

# Define the path for the new project directory
# It will be a subdirectory of the current working directory
project_path = Path.cwd() / args.project_name
print(project_path)

if project_path.exists():
    # Ask the user whether to override the existing directory
    response = input(f"The directory '{project_path}' already exists. Do you want to override it? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("Operation cancelled by the user.")
        exit()

# Create the project directory
project_path.mkdir(parents=True, exist_ok=True)

def generate_dir(dir_name):
    dir = project_path / dir_name
    dir.mkdir(exist_ok=True)

for dir in ['data', 'docs', 'notebooks', 'src', 'tests', 'scratch']:
    generate_dir(dir) 

# Define the path of your templates directory
templates_path = Path.home() / 'templates'

# Copy template files to the project directory
for template in ['README.md', '.gitignore', 'LICENSE']:
    shutil.copy(templates_path / template, project_path)

# Create __init__.py with version in src folder
init_file = project_path / 'src' / '__init__.py'
with init_file.open('w') as file:
    file.write("__version__ = '0.1.0'")

# Create main.py in src folder
main_file = project_path / 'src' / 'main.py'
with main_file.open('w') as file:
    file.write('#!/usr/bin/env python3')

print("Project setup complete.")

# Set up pyproject.toml
def setup_pyproject_toml():
    pyproject_template_path = templates_path / 'pyproject.toml'
    pyproject_target_path = project_path / 'pyproject.toml'

    # Check if the template pyproject.toml exists
    if not pyproject_template_path.exists():
        print("pyproject.toml template not found.")
        return

    # Read template and replace placeholder with actual project name
    with pyproject_template_path.open('r') as file:
        content = file.read().replace("PROJECT_NAME_PLACEHOLDER", args.project_name)

    # Write the modified content to the new project directory
    with pyproject_target_path.open('w') as file:
        file.write(content)

    print("pyproject.toml set up with project name.")

setup_pyproject_toml()

# Set up environment

# Check if the user wants a Conda environment
is_conda_env = args.python_version.startswith("conda")
env_version = args.python_version

if is_conda_env:
    # Create Conda environment
    subprocess.run(["conda", "create", "-y", "-n", args.project_name, f"python={env_version}"])
    print(f"Created conda env '{args.project_name}' with Python {env_version}")
    print(f"Cd into project and activate with: conda activate {args.project_name}")
else:
    # Determine the path to the specified Python executable
    python_executable = f"/usr/local/bin/python{args.python_version}"
    venv_path = project_path / 'venv'
    subprocess.run([python_executable, "-m", "venv", str(venv_path)])
    print(f"Created virtual environment with Python {args.python_version}")
    print("cd into project and activate with alias vrun")

# init git repo

subprocess.run(["git", "init", str(project_path)])
