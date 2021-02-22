import configuration
import pytest


@pytest.fixture()
def empty_configuration() -> configuration.Configuration:
    return configuration.Configuration()


def test_configuration_from_yaml_file_empty_filename():
    with pytest.raises(FileNotFoundError, match='No such file or directory: \'\''):
        configuration.configuration_from_yaml_file("")


def test_configuration_from_yaml_file_invalid_filename():
    name = "foo"
    with pytest.raises(FileNotFoundError, match=f'No such file or directory: \'{name}\''):
        configuration.configuration_from_yaml_file(name)


def test_yaml_from_stream_file_is_empty():
    yaml_contents = """
"""
    context = configuration.yaml_from_stream(yaml_contents)
    assert context is None


def test_validate_yaml_object():
    with pytest.raises(configuration.YamlValidationError, match="No configuration data. Empty file?"):
        configuration.validate_yaml_and_build_configuration(None)


def test_validate_context_has_correct_script_section_no_section(empty_configuration):
    yaml_contents = """
foo:
  bar
    """
    context = configuration.yaml_from_stream(yaml_contents)
    assert context
    with pytest.raises(configuration.YamlValidationError, match="No script section found"):
        configuration.validate_context_has_correct_script_section(context, empty_configuration)


def test_validate_context_has_correct_script_section_empty_script_section(empty_configuration):
    yaml_contents = """
script:
    """
    context = configuration.yaml_from_stream(yaml_contents)
    assert context
    with pytest.raises(configuration.YamlValidationError, match="Script section is empty"):
        configuration.validate_context_has_correct_script_section(context, empty_configuration)


def test_validate_context_has_correct_script_section_with_output_dir(empty_configuration):
    yaml_contents = """
script:
  eirectory: foobar
    """
    context = configuration.yaml_from_stream(yaml_contents)
    assert context
    with pytest.raises(configuration.YamlValidationError, match="Key script.output_directory not found"):
        configuration.validate_context_has_correct_script_section(context, empty_configuration)


def test_validate_context_has_correct_script_section(empty_configuration):
    yaml_contents = """
script:
  output_directory: foobar
    """
    context = configuration.yaml_from_stream(yaml_contents)
    assert context
    configuration.validate_context_has_correct_script_section(context, empty_configuration)
    assert empty_configuration.output_directory == "foobar"
