import pytest
import os
import tempfile
import json
import yaml
from create_genesis_seal import (
    read_file_content,
    read_yaml_content,
    read_json_content,
    create_deterministic_json,
    calculate_sha256
)

def test_read_file_content():
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
        f.write("Hello TrueAlphaSpiral!")
        temp_path = f.name

    try:
        content = read_file_content(temp_path)
        assert content == "Hello TrueAlphaSpiral!"

        # Test non-existent file
        assert read_file_content("non_existent_file_12345.txt") is None
    finally:
        os.unlink(temp_path)

def test_read_yaml_content():
    yaml_data = {"key": "value", "number": 42}
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
        yaml.dump(yaml_data, f)
        temp_path = f.name

    try:
        content = read_yaml_content(temp_path)
        assert content == yaml_data

        # Test invalid YAML
        with open(temp_path, 'w', encoding='utf-8') as f2:
            f2.write("invalid: yaml: :")
        assert read_yaml_content(temp_path) is None

        # Test non-existent file
        assert read_yaml_content("non_existent_yaml.yaml") is None
    finally:
        os.unlink(temp_path)

def test_read_json_content():
    json_data = {"key": "value", "number": 42}
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
        json.dump(json_data, f)
        temp_path = f.name

    try:
        content = read_json_content(temp_path)
        assert content == json_data

        # Test invalid JSON
        with open(temp_path, 'w', encoding='utf-8') as f2:
            f2.write("invalid json")
        assert read_json_content(temp_path) is None

        # Test non-existent file
        assert read_json_content("non_existent_json.json") is None
    finally:
        os.unlink(temp_path)

def test_create_deterministic_json():
    data1 = {"b": 2, "a": 1, "c": 3}
    data2 = {"a": 1, "c": 3, "b": 2}

    json1 = create_deterministic_json(data1)
    json2 = create_deterministic_json(data2)

    assert json1 == json2
    assert json1 == '{"a":1,"b":2,"c":3}'

def test_calculate_sha256():
    data = "Hello World"
    expected_hash = "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e"
    assert calculate_sha256(data) == expected_hash
