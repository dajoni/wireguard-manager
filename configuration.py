import yaml


class YamlValidationError(Exception):
    pass


class ServerConfiguration:
    def __init__(self) -> None:
        super().__init__()
        self.address = None


class Configuration:
    def __init__(self) -> None:
        super().__init__()
        self.output_directory = None
        self.server = ServerConfiguration()


def configuration_from_yaml_file(file_name) -> Configuration:
    with open(file_name, 'rt') as datafile:
        context = yaml_from_stream(datafile)
    configuration = validate_yaml_and_build_configuration(context)
    return configuration


def yaml_from_stream(stream) -> dict:
    return yaml.load(stream, Loader=yaml.FullLoader)


def validate_context_has_data(context, configuration):
    if context is None:
        raise YamlValidationError("No configuration data. Empty file?")


def validate_context_has_correct_script_section(context, configuration: Configuration):
    if "script" not in context.keys():
        raise YamlValidationError("No script section found in configuration file")
    script_section = context['script']
    if script_section is None:
        raise YamlValidationError("Script section is empty")
    validate_field_exists("script", "output_directory", script_section)
    configuration.output_directory = script_section['output_directory']


def validate_context_has_correct_server_section(context, configuration: Configuration):
    if "server" not in context.keys():
        raise YamlValidationError("No server section found in configuration file")
    server_section = context['server']
    if server_section is None:
        raise YamlValidationError("Server section is empty")
    if not isinstance(server_section, dict):
        raise YamlValidationError("Server section is not a dictionary")
    validate_field_exists("server", "address", server_section)
    validate_field_exists("server", "listen_port", server_section)
    validate_field_exists("server", "endpoint_ip", server_section)
    validate_field_exists("server", "public_key", server_section)
    validate_field_exists("server", "private_key", server_section)
    configuration.server.address = server_section['address']
    configuration.server.listen_port = server_section['listen_port']
    configuration.server.endpoint_ip = server_section['endpoint_ip']
    configuration.server.public_key = server_section['public_key']
    configuration.server.private_key = server_section['private_key']


def validate_field_exists(section_name, field_name, section):
    if field_name not in section.keys():
        raise YamlValidationError(f"{section_name}.{field_name} not found in configuration file")


def validate_yaml_and_build_configuration(context) -> Configuration:
    configuration = Configuration()
    validate_context_has_data(context, configuration)
    validate_context_has_correct_script_section(context, configuration)
    validate_context_has_correct_server_section(context, configuration)
    return configuration
