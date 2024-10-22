import os
import re
import select
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


def execute_command_with_sudo(command: str, sudo_password: str = None):
    if sudo_password is None:
        sudo_password = secret["sudo_password"]

    try:
        # Use `subprocess.Popen` to run the command with sudo
        process = subprocess.Popen(
            ['sudo', '-S'] + command.split(),  # '-S' reads the password from stdin
            stdin=subprocess.PIPE,  # Connect stdin for password input
            stdout=subprocess.PIPE,  # Capture standard output
            stderr=subprocess.PIPE,  # Capture standard error
            text=True  # Return output as text
        )
        # Pass the password to the process via stdin
        stdout, stderr = process.communicate(input=f"{sudo_password}\n")
        print("Output:", stdout)
        print("Error:", stderr)

    except Exception as e:
        print(f"Error occurred: {e}")


def execute_command_with_sudo_as_user_and_stream_logs(
        command: str,
        sudo_password: str = None,
        username: str = None,
):
    """ ToDo: does not work """

    if sudo_password is None:
        sudo_password = secret["sudo_password"]

    if username is None:
        username = secret["username"]

    try:
        process = subprocess.Popen(
            ['sudo', '-S', '-u', username] + command.split(),  # '-S' reads the password from stdin
            stdin=subprocess.PIPE,  # Connect stdin for password input
            stdout=subprocess.PIPE,  # Capture standard output
            stderr=subprocess.PIPE,  # Capture standard error
            bufsize=1,  # Line-buffered output
            preexec_fn=os.setsid,  # Run command in a new process group
            universal_newlines=True  # Decode stdout/stderr as text instead of bytes
        )

        # Send the password to the process
        process.stdin.write(f"{sudo_password}\n")
        process.stdin.flush()

        # Use select to read both stdout and stderr without blocking
        while True:
            reads = [process.stdout, process.stderr]
            readable, _, _ = select.select(reads, [], [])

            for stream in readable:
                output = stream.readline()
                if output:
                    log = output.strip()
                    print(f"Streaming logs: {log}")
                    yield log
                else:
                    print(f"Streaming logs finished.")
                    return

    except Exception as e:
        print(f"Error occurred: {e}")


def remove_directory_with_content(dir_path: Path):
    execute_command_with_sudo(f'rm -r {dir_path}')


def extract_from_tar_gz(dir_path: Path, filename: str):
    os.chdir(dir_path)
    execute_command_with_sudo(f'tar -xzf {filename}')


def change_owner(dir_path: Path, username: str):
    execute_command_with_sudo(f'chown -R {username}:{username} {dir_path}')


def write_jvm_options(filepath: Path, options: str):
    with open(filepath, "wt") as f:
        f.write(options)


def set_transport_host(filepath: Path, host: str = "0.0.0.0"):
    pattern = re.compile(r"\s*transport.host")
    with open(filepath, "rt") as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            match = pattern.search(line)
            if match:
                lines[index] = f"{match.group()}: {host}\n"
                break
        else:
            lines.append(f"transport.host: {host}\n")

    if lines:
        with open(filepath, "wt") as f:
            f.write("".join(lines))
    else:
        print(f"Nothing to set in: {filepath}")


def run_elasticsearch_node_and_stream_logs(dir_path: Path):
    """ ToDo: does not work """
    for log in execute_command_with_sudo_as_user_and_stream_logs(str(dir_path / "bin/elasticsearch")):
        yield log


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
        username: str = None,
):
    if dir_paths is None:
        dir_paths = ELASTICSEARCH_DIR_PATH_DICT.values()

    if elastcisearch_package is None:
        elastcisearch_package = ELASTICSEARCH_PACKAGE

    if username is None:
        username = secret["username"]

    for dir_path in dir_paths:
        dir_path = dir_path / elastcisearch_package
        print(f"Changing owner of Elasticsearch directory to '{username}':", str(dir_path))
        change_owner(dir_path, username)


def change_owner_of_kibana_dir(
        dir_path: Path = None,
        kibana_package: str = None,
        username: str = None,
):
    if dir_path is None:
        dir_path = KIBANA_DIR_PATH

    if kibana_package is None:
        kibana_package = KIBANA_PACKAGE

    if username is None:
        username = secret["username"]

    dir_path = dir_path / kibana_package
    print(f"Changing owner of Kibana directory to '{username}':", str(dir_path))
    change_owner(dir_path, username)


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


def run_main_elasticsearch_node_and_stream_logs():
    """ ToDo: does not work """
    path_to_main_elasticsearch_node = ELASTICSEARCH_DIR_PATH_DICT["main"] / ELASTICSEARCH_PACKAGE
    for log in run_elasticsearch_node_and_stream_logs(path_to_main_elasticsearch_node):
        yield log


if __name__ == "__main__":
    # delete_elastic_stack_dirs()
    # extract_elasticsearch_dirs_from_tar_gz()
    # extract_kibana_dir_from_tar_gz()
    # change_owner_of_elasticsearch_dirs()
    # change_owner_of_kibana_dir()
    # write_jvm_options_in_elasticsearch_configs()
    # run_main_elasticsearch_node_and_stream_logs()  # ToDo: does not work
    ...