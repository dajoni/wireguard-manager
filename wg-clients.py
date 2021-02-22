#!/usr/bin/env python3
import yaml
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import configuration


def get_config():
    with open("config.yaml", 'r') as datafile:
        context = yaml.load(datafile, Loader=yaml.FullLoader)
    return context


def write_config_file(config, name, content):
    file_name = f"{config['script']['output_directory']}/{name}"
    print(f"Writing file {file_name}")
    with open(file_name, 'w') as server_config_file:
        server_config_file.write(content)
        server_config_file.write("\n")


def generate_server_config(config, env):
    server_template = env.get_template("templates/server.conf.jinja2")
    rendered_template = server_template.render(**config)
    write_config_file(config, "wg0.conf", rendered_template)


def generate_client_config(config, env):
    client_template = env.get_template("templates/client.conf.jinja2")
    for client in config["clients"]["instances"]:
        rendered_template = client_template.render({**config, "client": client})
        write_config_file(config, f"clients/{client['name']}.conf", rendered_template)


def create_output_directories(config):
    Path(f"{config['script']['output_directory']}/clients").mkdir(parents=True, exist_ok=True)
    Path(f"{config['script']['output_directory']}/keys").mkdir(parents=True, exist_ok=True)


def main():
    config = get_config()
    env = Environment(loader=FileSystemLoader('.'))
    create_output_directories(config)
    generate_server_config(config, env)
    generate_client_config(config, env)


if __name__ == '__main__':
    main()
