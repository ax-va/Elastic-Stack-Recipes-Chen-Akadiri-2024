import os
import subprocess
import yaml
from pathlib import Path

with open('../secret.yml', 'r') as file:
    secret = yaml.safe_load(file)

ELASTICSEARCH_DIRS = {
    "main": Path("/bin/elasticsearch"),
    "cold": Path("/bin/elasticsearch-node-cold"),
    "frozen": Path("/bin/elasticsearch-node-frozen"),
    "master": Path("/bin/elasticsearch-node-master"),
    "ml": Path("/bin/elasticsearch-node-ml"),
}
KIBANA_DIR = Path("/bin/kibana")
ELASTICSEARCH_PACKAGE = "elasticsearch-8.15.1"
KIBANA_PACKAGE = "kibana-8.15.1"
PACKAGE_SPECIFICATION = "-linux-x86_64.tar.gz"
PATHS_TO_INSTALLED_PACKAGES = [dir_ / ELASTICSEARCH_PACKAGE for dir_ in ELASTICSEARCH_DIRS.values()]
PATHS_TO_INSTALLED_PACKAGES.extend([KIBANA_DIR / KIBANA_PACKAGE])


def execute_command_with_sudo(command: str):
    # Use `subprocess.Popen` to run the command with sudo
    process = subprocess.Popen(
        ['sudo', '-S'] + command.split(), # '-S' reads the password from stdin
        stdin=subprocess.PIPE, # Connect stdin for password input
        stdout=subprocess.PIPE, # Capture standard output
        stderr=subprocess.PIPE, # Capture standard error
        text=True # Return output as text
    )
    # Pass the password to the process via stdin
    stdout, stderr = process.communicate(input=secret["sudo_password"] + '\n')
    print("Output:", stdout)
    print("Error:", stderr)


def remove_directory_with_content(path: str | Path):
    execute_command_with_sudo(f'rm -r {path}')


def extract_from_tar_gz(file_dir: str | Path, filename: str | Path):
    os.chdir(file_dir)
    execute_command_with_sudo(f'tar -xzf {filename}')


def delete_all_elastic_stack_elements():
    for path in PATHS_TO_INSTALLED_PACKAGES:
        remove_directory_with_content(path)


def extract_all_elastic_stack_elements_from_tar_gz():
    for dir_ in ELASTICSEARCH_DIRS.values():
        filename = ELASTICSEARCH_PACKAGE + PACKAGE_SPECIFICATION
        print("Extracting:", str(dir_ / filename))
        extract_from_tar_gz(dir_, filename)
    dir_ = KIBANA_DIR
    filename = KIBANA_PACKAGE + PACKAGE_SPECIFICATION
    print("Extracting:", str(dir_ / filename))
    extract_from_tar_gz(dir_, filename)


if __name__ == "__main__":
    # delete_all_elastic_stack_elements()
    extract_all_elastic_stack_elements_from_tar_gz()
