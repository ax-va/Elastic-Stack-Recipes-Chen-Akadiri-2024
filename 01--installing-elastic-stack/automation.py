import os
import subprocess
import yaml
from pathlib import Path

with open('../secret.yml', 'r') as file:
    secret = yaml.safe_load(file)

ELASTICSEARCH_DIR_PATH_DICT = {
    "main": Path("/bin/elasticsearch"),
    "cold": Path("/bin/elasticsearch-node-cold"),
    "frozen": Path("/bin/elasticsearch-node-frozen"),
    "master": Path("/bin/elasticsearch-node-master"),
    "ml": Path("/bin/elasticsearch-node-ml"),
}
KIBANA_DIR_PATH = Path("/bin/kibana")
ELASTICSEARCH_PACKAGE = "elasticsearch-8.15.1"
KIBANA_PACKAGE = "kibana-8.15.1"
PACKAGE_SPECIFICATION = "-linux-x86_64.tar.gz"
PATHS_TO_INSTALLED_PACKAGES = [dir_path / ELASTICSEARCH_PACKAGE for dir_path in ELASTICSEARCH_DIR_PATH_DICT.values()]
PATHS_TO_INSTALLED_PACKAGES.extend([KIBANA_DIR_PATH / KIBANA_PACKAGE])
JVM_OPTIONS_DICT = {
    "main": "-Xms4g\n-Xmx4g",
    "cold": "-Xms2g\n-Xmx2g",
    "frozen": "-Xms2g\n-Xmx2g",
    "master": "-Xms4g\n-Xmx4g",
    "ml": "-Xms4g\n-Xmx4g",
}


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


def remove_directory_with_content(dir_path: Path):
    execute_command_with_sudo(f'rm -r {dir_path}')


def extract_from_tar_gz(dir_path: Path, filename: str):
    os.chdir(dir_path)
    execute_command_with_sudo(f'tar -xzf {filename}')


def change_owner(dir_path: Path, owner: str):
    execute_command_with_sudo(f'chown -R {owner}:{owner} {dir_path}')


def write_jvm_options(filepath: Path, options: str):
    with open(filepath, "wt") as f:
        f.write(options)


def delete_all_elastic_stack_dirs():
    for path in PATHS_TO_INSTALLED_PACKAGES:
        remove_directory_with_content(path)


def extract_all_elastic_stack_dirs_from_tar_gz():
    for dir_path in ELASTICSEARCH_DIR_PATH_DICT.values():
        filename = ELASTICSEARCH_PACKAGE + PACKAGE_SPECIFICATION
        print("Extracting:", str(dir_path / filename))
        extract_from_tar_gz(dir_path, filename)
    dir_path = KIBANA_DIR_PATH
    filename = KIBANA_PACKAGE + PACKAGE_SPECIFICATION
    print("Extracting:", str(dir_path / filename))
    extract_from_tar_gz(dir_path, filename)


def change_owner_of_all_elastic_stack_dirs():
    for dir_path in ELASTICSEARCH_DIR_PATH_DICT.values():
        dir_path = dir_path / ELASTICSEARCH_PACKAGE
        print("Changing owner of:", str(dir_path))
        change_owner(dir_path, secret["owner"])
    dir_path = KIBANA_DIR_PATH / KIBANA_PACKAGE
    print("Changing owner of:", str(dir_path))
    change_owner(dir_path, secret["owner"])


def write_jvm_options_in_all_elasticsearch_configs():
    for node_name, dir_path in ELASTICSEARCH_DIR_PATH_DICT.items():
        filepath = dir_path / ELASTICSEARCH_PACKAGE / "config/jvm.options.d/jvm.options"
        print("Writing JVM options:", str(filepath))
        write_jvm_options(filepath, JVM_OPTIONS_DICT[node_name])

if __name__ == "__main__":
    # delete_all_elastic_stack_dirs()
    # extract_all_elastic_stack_dirs_from_tar_gz()
    # change_owner_of_all_elastic_stack_dirs()
    write_jvm_options_in_all_elasticsearch_configs()
