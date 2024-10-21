import os
import subprocess
from typing import Iterable, Dict

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


def set_transport_host(filepath: Path, host: str = "0.0.0.0"):
    with open(filepath, "rt") as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            if "transport.host" in line:
                lines[index] = f"transport.host: {host}\n"
                break
        else:
            lines.append(f"transport.host: {host}\n")

    if lines:
        with open(filepath, "wt") as f:
            f.write("".join(lines))
    else:
        print(f"Nothing set in: {filepath}")


def delete_elastic_stack_dirs(dir_paths: Iterable[Path] = None):
    if dir_paths is None:
        dir_paths = PATHS_TO_INSTALLED_PACKAGES

    for dir_path in dir_paths:
        remove_directory_with_content(dir_path)


def extract_elasticsearch_dirs_from_tar_gz(
        dir_paths: Iterable[Path] = None,
        elasticsearch_package: str = None,
        package_specification: str = None,
):
    if dir_paths is None:
        dir_paths = ELASTICSEARCH_DIR_PATH_DICT.values()

    if elasticsearch_package is None:
        elasticsearch_package = ELASTICSEARCH_PACKAGE

    if package_specification is None:
        package_specification = PACKAGE_SPECIFICATION

    for dir_path in dir_paths:
        filename = elasticsearch_package + package_specification
        print("Extracting Elasticsearch:", str(dir_path / filename))
        extract_from_tar_gz(dir_path, filename)


def extract_kibana_dir_from_tar_gz(
        dir_path: Path = None,
        kibana_package: str = None,
        package_specification: str = None,
):
    if dir_path is None:
        dir_path = KIBANA_DIR_PATH

    if kibana_package is None:
        kibana_package = KIBANA_PACKAGE

    if package_specification is None:
        package_specification = PACKAGE_SPECIFICATION

    filename = kibana_package + package_specification
    print("Extracting Kibana:", str(dir_path / filename))
    extract_from_tar_gz(dir_path, filename)


def change_owner_of_elasticsearch_dirs(
        dir_paths: Iterable[Path] = None,
        elastcisearch_package: str = None,
):
    if dir_paths is None:
        dir_paths = ELASTICSEARCH_DIR_PATH_DICT.values()

    for dir_path in dir_paths:
        dir_path = dir_path / elastcisearch_package
        print("Changing owner of Elasticsearch directory:", str(dir_path))
        change_owner(dir_path, secret["owner"])


def change_owner_of_kibana_dir(
        dir_path: Path = None,
        kibana_package: str = None,
):
    if dir_path is None:
        dir_path = KIBANA_DIR_PATH

    if kibana_package is None:
        kibana_package = KIBANA_PACKAGE

    dir_path = dir_path / kibana_package
    print("Changing owner of Kibana directory:", str(dir_path))
    change_owner(dir_path, secret["owner"])


def write_jvm_options_in_elasticsearch_configs(
        dir_path_dict: Dict[str, Path] = None,
        jvm_options_dict: Dict[str, str] = None,
        elasticsearch_package: str = None,
):
    if dir_path_dict is None:
        dir_path_dict = ELASTICSEARCH_DIR_PATH_DICT

    if jvm_options_dict is None:
        jvm_options_dict = JVM_OPTIONS_DICT

    if elasticsearch_package is None:
        elasticsearch_package = ELASTICSEARCH_PACKAGE

    for node_name, dir_path in dir_path_dict.items():
        filepath = dir_path / elasticsearch_package / "config/jvm.options.d/jvm.options"
        print("Writing JVM options:", str(filepath))
        write_jvm_options(filepath, jvm_options_dict[node_name])


def set_transport_host_for_main_elasticsearch_node():
    set_transport_host(ELASTICSEARCH_DIR_PATH_DICT["main"] / ELASTICSEARCH_PACKAGE / "config/elasticsearch.yml")


if __name__ == "__main__":
    # delete_elastic_stack_dirs()
    # extract_elasticsearch_dirs_from_tar_gz()
    # extract_kibana_dir_from_tar_gz()
    # change_owner_of_elasticsearch_dirs()
    # change_owner_of_kibana_dir()
    # write_jvm_options_in_elasticsearch_configs()
    ...