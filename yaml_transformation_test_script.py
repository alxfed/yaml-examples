# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
# !/usr/bin/env python3
"""
Test script for yaml_transform.py

This script creates test YAML files with various special characters
and verifies that the transformation preserves all special characters
and successfully converts the format.
"""

import os
import sys
import yaml
import tempfile
import unittest
from yaml_transformation_script import transform_yaml


class TestYAMLTransform(unittest.TestCase):
    """Test cases for YAML transformation"""

    def setUp(self):
        """Set up temporary directories for testing"""
        self.temp_dir = tempfile.mkdtemp()
        self.input_file = os.path.join(self.temp_dir, "input.yaml")
        self.output_file = os.path.join(self.temp_dir, "output.yaml")

    def tearDown(self):
        """Clean up temporary files"""
        if os.path.exists(self.input_file):
            os.remove(self.input_file)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        os.rmdir(self.temp_dir)

    def test_basic_transformation(self):
        """Test basic transformation without special characters"""
        input_data = [
            {
                'parts': [{'text': 'what is it?'}],
                'role': 'user'
            },
            {
                'parts': [{'text': 'this is a response'}],
                'role': 'model'
            }
        ]

        expected_output = [
            {
                'role': 'Human',
                'text': 'what is it?'
            },
            {
                'role': 'machine',
                'text': 'this is a response'
            }
        ]

        with open(self.input_file, 'w') as f:
            yaml.dump(input_data, f)

        self.assertTrue(transform_yaml(self.input_file, self.output_file))

        with open(self.output_file, 'r') as f:
            output_data = yaml.safe_load(f)

        self.assertEqual(output_data, expected_output)

    def test_special_characters(self):
        """Test transformation with special characters"""
        input_data = [
            {
                'parts': [{'text': "Text with 'single quotes' and \"double quotes\""}],
                'role': 'user'
            },
            {
                'parts': [{'text': "Text with special chars: & * % $ # @ !"}],
                'role': 'model'
            },
            {
                'parts': [{'text': "Text with\nnewlines\nand\ttabs"}],
                'role': 'user'
            }
        ]

        with open(self.input_file, 'w') as f:
            yaml.dump(input_data, f)

        self.assertTrue(transform_yaml(self.input_file, self.output_file))

        with open(self.output_file, 'r') as f:
            output_data = yaml.safe_load(f)

        # Verify all texts were preserved
        self.assertEqual(output_data[0]['text'], input_data[0]['parts'][0]['text'])
        self.assertEqual(output_data[1]['text'], input_data[1]['parts'][0]['text'])
        self.assertEqual(output_data[2]['text'], input_data[2]['parts'][0]['text'])

        # Verify roles were transformed
        self.assertEqual(output_data[0]['role'], 'Human')
        self.assertEqual(output_data[1]['role'], 'machine')
        self.assertEqual(output_data[2]['role'], 'Human')

    def test_error_handling(self):
        """Test error handling for invalid input"""
        # Test with non-existent file
        non_existent_file = os.path.join(self.temp_dir, "non_existent.yaml")
        self.assertFalse(transform_yaml(non_existent_file, self.output_file))

        # Test with invalid YAML
        with open(self.input_file, 'w') as f:
            f.write("This is not valid YAML: {unclosed")

        self.assertFalse(transform_yaml(self.input_file, self.output_file))

        # Test with incorrect structure
        with open(self.input_file, 'w') as f:
            yaml.dump({"this": "is not the expected structure"}, f)

        self.assertTrue(transform_yaml(self.input_file, self.output_file))

        with open(self.output_file, 'r') as f:
            output_data = yaml.safe_load(f)

        # The output should be an empty list since no valid items were found
        self.assertEqual(output_data, [])


if __name__ == "__main__":
    unittest.main()