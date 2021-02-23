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
    with pytest.raises(configuration.YamlValidationError, match="No script section found in configuration file"):
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
    with pytest.raises(configuration.YamlValidationError,
                       match="script.output_directory not found in configuration file"):
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


def test_validate_context_has_correct_server_section_no_server_section(empty_configuration):
    yaml_contents = """
    foo:
      bar
        """
    context = configuration.yaml_from_stream(yaml_contents)
    assert context
    with pytest.raises(configuration.YamlValidationError, match="No server section found in configuration file"):
        configuration.validate_context_has_correct_server_section(context, empty_configuration)


def test_validate_context_has_correct_server_section_empty_server_section(empty_configuration):
    yaml_contents = """
    server:
        """
    context = configuration.yaml_from_stream(yaml_contents)
    assert context
    with pytest.raises(configuration.YamlValidationError, match="Server section is empty"):
        configuration.validate_context_has_correct_server_section(context, empty_configuration)


def test_validate_context_has_correct_server_section_server_section_not_a_dict(empty_configuration):
    yaml_contents = """
    server:
        foo
        """
    context = configuration.yaml_from_stream(yaml_contents)
    assert context
    with pytest.raises(configuration.YamlValidationError, match="Server section is not a dictionary"):
        configuration.validate_context_has_correct_server_section(context, empty_configuration)


def test_validate_context_has_correct_server_section_contains_address(empty_configuration):
    yaml_contents = """
    server:
        foo: bar
        """
    context = configuration.yaml_from_stream(yaml_contents)
    assert context
    with pytest.raises(configuration.YamlValidationError, match="server.address not found in configuration file"):
        configuration.validate_context_has_correct_server_section(context, empty_configuration)


def test_validate_context_has_correct_server_section_contains_listen_port(empty_configuration):
    yaml_contents = """
    server:
        address: bar
        """
    context = configuration.yaml_from_stream(yaml_contents)
    assert context
    with pytest.raises(configuration.YamlValidationError, match="server.listen_port not found in configuration file"):
        configuration.validate_context_has_correct_server_section(context, empty_configuration)


server_parameters = ["address", "listen_port", "endpoint_ip", "public_key", "private_key"]


@pytest.mark.parametrize("field_name", server_parameters)
def test_validate_context_has_correct_server_section_contains_field(field_name, empty_configuration):
    yaml_contents = """
    server:
      address: 10.0.0.1/24
      listen_port: 51820
      endpoint_ip: 127.0.0.1
      public_key: somepublickey=
      private_key: someprivatekey=
        """
    context = configuration.yaml_from_stream(yaml_contents)
    assert context
    del context['server'][field_name]
    with pytest.raises(configuration.YamlValidationError, match=f"server.{field_name} not found in configuration file"):
        configuration.validate_context_has_correct_server_section(context, empty_configuration)


def test_validate_context_has_correct_server_section(empty_configuration):
    yaml_contents = """
    server:
      address: 10.0.0.1/24
      listen_port: 51820
      endpoint_ip: 127.0.0.1
      public_key: somepublickey=
      private_key: someprivatekey=
        """
    context = configuration.yaml_from_stream(yaml_contents)
    assert context
    configuration.validate_context_has_correct_server_section(context, empty_configuration)
    assert empty_configuration.server.address == "10.0.0.1/24"
    assert empty_configuration.server.listen_port == 51820
    assert empty_configuration.server.endpoint_ip == "127.0.0.1"
    assert empty_configuration.server.public_key == "somepublickey="
    assert empty_configuration.server.private_key == "someprivatekey="
