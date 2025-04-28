# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
# !/usr/bin/env python3
import sys
import yaml
import os
import argparse
from typing import List, Dict, Any, Optional


def transform_yaml(input_file: str, output_file: str, verbose: bool = False) -> bool:
    """
    Transform YAML file from the first format to the second format.

    Args:
        input_file (str): Path to the input YAML file
        output_file (str): Path to the output YAML file
        verbose (bool): Whether to print verbose messages

    Returns:
        bool: True if transformation was successful, False otherwise
    """
    # Read the input YAML file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            try:
                data = yaml.safe_load(f)
                if not isinstance(data, list):
                    print(f"Error: Expected a list in {input_file}, but got {type(data)}")
                    return False
            except yaml.YAMLError as e:
                print(f"Error parsing YAML in {input_file}: {e}")
                return False
    except Exception as e:
        print(f"Error reading file {input_file}: {e}")
        return False

    if verbose:
        print(f"Successfully read {len(data)} items from {input_file}")

    # Transform the data
    transformed_data = []
    warnings = 0

    for i, item in enumerate(data):
        # Check if the item has the expected structure
        if not isinstance(item, dict) or 'parts' not in item or 'role' not in item:
            warnings += 1
            if verbose:
                print(f"Warning: Item {i} has unexpected format: {item}")
            continue

        # Extract the text from the first part
        if not item['parts'] or not isinstance(item['parts'], list) or len(item['parts']) == 0 or 'text' not in \
                item['parts'][0]:
            warnings += 1
            if verbose:
                print(f"Warning: Item {i} has missing or invalid 'parts': {item}")
            continue

        text = item['parts'][0]['text']

        # Transform the role
        if item['role'] == 'user':
            role = 'Human'
        else:
            role = 'machine'

        # Add to transformed data
        transformed_data.append({
            'role': role,
            'text': text
        })

    if warnings > 0 and verbose:
        print(f"Encountered {warnings} warnings during transformation")

    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
        except Exception as e:
            print(f"Error creating output directory {output_dir}: {e}")
            return False

    # Write the transformed data to the output file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            # Use safe_dump with appropriate settings for special characters
            yaml.safe_dump(
                transformed_data,
                f,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False
            )
    except Exception as e:
        print(f"Error writing to {output_file}: {e}")
        return False

    if verbose:
        print(f"Successfully wrote {len(transformed_data)} items to {output_file}")

    return True


def process_directory(input_dir: str, output_dir: str, verbose: bool = False) -> bool:
    """
    Process all YAML files in a directory

    Args:
        input_dir (str): Directory containing input YAML files
        output_dir (str): Directory to write output YAML files
        verbose (bool): Whether to print verbose messages

    Returns:
        bool: True if all files were processed successfully, False otherwise
    """
    if not os.path.exists(input_dir):
        print(f"Error: Input directory '{input_dir}' does not exist")
        return False

    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
        except Exception as e:
            print(f"Error creating output directory '{output_dir}': {e}")
            return False

    success = True
    files_processed = 0

    for filename in os.listdir(input_dir):
        if filename.endswith('.yaml') or filename.endswith('.yml'):
            input_file = os.path.join(input_dir, filename)
            output_file = os.path.join(output_dir, filename)

            if verbose:
                print(f"Processing {input_file} -> {output_file}")

            if transform_yaml(input_file, output_file, verbose):
                files_processed += 1
            else:
                success = False

    if verbose:
        print(f"Successfully processed {files_processed} files")

    return success


def main():
    """Main function to handle command line arguments"""
    parser = argparse.ArgumentParser(description='Transform YAML files from one format to another')

    # Define command line arguments
    parser.add_argument('input', help='Input YAML file or directory')
    parser.add_argument('output', help='Output YAML file or directory')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print verbose output')
    parser.add_argument('-r', '--recursive', action='store_true', help='Process directories recursively')

    args = parser.parse_args()

    # Check if input is a file or directory
    if os.path.isfile(args.input):
        # Process a single file
        if os.path.isdir(args.output):
            # If output is a directory, use the input filename
            output_file = os.path.join(args.output, os.path.basename(args.input))
        else:
            output_file = args.output

        if not os.path.exists(args.input):
            print(f"Error: Input file '{args.input}' does not exist")
            return 1

        if transform_yaml(args.input, output_file, args.verbose):
            if args.verbose:
                print(f"Successfully transformed '{args.input}' to '{output_file}'")
            return 0
        else:
            print(f"Failed to transform '{args.input}'")
            return 1

    elif os.path.isdir(args.input):
        # Process a directory
        if not os.path.isdir(args.output):
            print(f"Error: When input is a directory, output must also be a directory")
            return 1

        if process_directory(args.input, args.output, args.verbose):
            return 0
        else:
            return 1

    else:
        print(f"Error: Input '{args.input}' does not exist")
        return 1


if __name__ == "__main__":
    sys.exit(main())