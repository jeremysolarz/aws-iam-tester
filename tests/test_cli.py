"""
Tests for the command module
"""
import os
import subprocess
import pytest
import pathlib

from pyassert import assert_that
# from aws-iam-tester import cli

script_path = pathlib.Path(__file__).parent.absolute()

def run_command(command_list):
    process = subprocess.Popen(
        command_list,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    # print(f"Return code: {process.returncode}")
    # print(f"Stdout: {stdout}")
    # print(f"Stderr: {stderr}")

    assert_that(process.returncode).is_less_than(2)
    assert_that(stderr).is_not_none()

    return str(stdout), str(stderr)

def test_runas_module():
    exit_status = os.system(f'python -m aws_iam_tester --help')
    assert exit_status == 0

def test_help():
    stdout, stderr = run_command(
        ['aws-iam-tester', '--help']
    )
    assert_that(stdout).contains('Usage')

def test_version():
    stdout, stderr = run_command(
        ['aws-iam-tester', '--version'],
    )
    assert_that(stdout).contains('version')

def test_test_runs():
    stdout, stderr = run_command(
        ['aws-iam-tester', '--config-file', f'{script_path}/config.yml', '--number-of-runs', '10'],
    )

def test_dry_run():
    stdout, stderr = run_command(
        ['aws-iam-tester', '--config-file', f'{script_path}/config.yml', '--dry-run'],
    )

def test_no_system_roles():
    stdout, stderr = run_command(
        ['aws-iam-tester', '--config-file', f'{script_path}/config.yml', '--no-system-roles'],
    )

def test_full_run():
    output_dir = '/tmp/iam_tester_results'
    stdout, stderr = run_command(
        ['aws-iam-tester', '--config-file', f'{script_path}/config.yml', '--write-to-file', '--output-location', output_dir],
    )
    assert_that(stdout).contains("are written to")
    assert_that(output_dir).is_a_directory()

def test_full_run_with_global_limit():
    output_dir = '/tmp/iam_tester_results'
    stdout, stderr = run_command(
        ['aws-iam-tester', '--config-file', f'{script_path}/config_with_global_limit_to.yml', '--write-to-file', '--output-location', output_dir],
    )
    assert_that(stdout).matches(r"(^(.)*are written to(.)*$)|(^(.)*No findings found(.)*$)")
    
    assert_that(output_dir).is_a_directory()
