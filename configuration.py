import yaml


class YamlValidationError(Exception):
    pass


class Configuration:
    def __init__(self) -> None:
        super().__init__()
        self.output_directory = None


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


def validate_context_has_correct_script_section(context, configuration):
    if "script" not in context.keys():
        raise YamlValidationError("No script section found")
    script_section = context['script']
    if script_section is None:
        raise YamlValidationError("Script section is empty")
    if "output_directory" not in script_section.keys():
        raise YamlValidationError("Key script.output_directory not found")
    else:
        configuration.output_directory = script_section['output_directory']

def validate_yaml_and_build_configuration(context) -> Configuration:
    configuration = Configuration()
    validate_context_has_data(context, configuration)
    validate_context_has_correct_script_section(context, configuration)
    return configuration
