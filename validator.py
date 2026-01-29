import json
import jsonschema
from jsonschema import validate

def load_schema(schema_path):
    """
    Load the provided JSON schema file
    :param schema_path: Path to the schema file (We_the_People_Schema_v1.0.json)
    :return: Parsed JSON schema
    """
    with open(schema_path, 'r') as file:
        return json.load(file)

def validate_input(data, schema):
    """
    Validate input data against the given schema
    :param data: JSON input to validate
    :param schema: Parsed JSON schema
    :return: Tuple (is_valid, errors)
    """
    try:
        validate(instance=data, schema=schema)
        return True, []
    except jsonschema.exceptions.ValidationError as ve:
        return False, [ve.message]

def main():
    schema_path = "We_the_People_Schema_v1.0.json"  # Path to schema file
    input_data_path = "input.json"  # Path to the JSON input file for validation

    # Load the schema
    schema = load_schema(schema_path)

    # Load the input data
    with open(input_data_path, 'r') as file:
        input_data = json.load(file)

    # Validate the input data against the schema
    is_valid, errors = validate_input(input_data, schema)

    if is_valid:
        print("Validation successful: Input data adheres to the schema.")
    else:
        print("Validation failed: The input data does not conform to the schema.")
        for error in errors:
            print(f"Error: {error}")

if __name__ == "__main__":
    main()