"""
Test for QookFast template generation
"""

import os
import subprocess

import pytest
import requests
import yaml


@pytest.fixture
def project_name():
    return "Test Project-CI/CD"


@pytest.fixture
def essential_files():
    return [
        ".gitignore",
        "get_versions.sh",
        "Makefile",
        "README.md",
        "run_pipeline.sh",
        "align/.gitkeep",
        "counts/.gitkeep",
        "genome/.gitkeep",
        "genome/star_index/.gitkeep",
        "qc/.gitkeep",
        "raw_data/.gitkeep",
    ]


def minimal_tests(
    result,
    fixture_project_name,
    fixture_essential_files,
    expected_species="Homo_sapiens",
):
    print("===== #1. Checking exit code =====")
    assert (
        result.exit_code == 0
    ), f"FAILED in #1! Invalid exit_code; expected 0, got {result.exit_code}"

    print("===== #2. Checking exception status =====")
    assert (
        result.exception is None
    ), f"FAILED in #2! Invalid exception; expected None, got {result.exception}"

    print("===== #3. Checking project path name =====")
    path = result.project_path.name
    expected_path = (
        fixture_project_name.replace(" ", "_").replace("-", "_").replace("/", "_")
    )
    assert (
        path == expected_path
    ), f"FAILED in #3! Invalid path; expected `{expected_path}`, got {path}"

    print("===== #4. Checking project path is a directory =====")
    assert result.project_path.is_dir(), f"FAILED in #4! {path} is not a directory"

    print("===== #5. Checking essential files =====")
    for i, file in enumerate(
        fixture_essential_files + [f"{expected_path.lower()}.def"]
    ):
        file_path = result.project_path / file
        assert (
            file_path.exists()
        ), f"FAILED in #5-{i + 1}! {file} is not found in {path}"

    print("===== #6. Checking apptainer container (Mocked) =====")
    fake_sudo = result.project_path / "sudo"
    fake_sudo.write_text('#!/bin/bash\n"$@"\n')
    fake_sudo.chmod(0o755)
    fake_apptainer = result.project_path / "apptainer"
    fake_apptainer.write_text("#!/bin/bash\nexit 0\n")
    fake_apptainer.chmod(0o755)

    env = os.environ.copy()
    env["PATH"] = f"{result.project_path}:{env['PATH']}"

    subprocess.run(["make", "build_env"], cwd=result.project_path, env=env, check=True)
    recipe_file = result.project_path / "recipe.yaml"
    assert recipe_file.exists(), f"FAILED in #6! recipe.yaml is not found in {path}"

    print("===== #7–17. Checking genome URLs in recipe.yaml =====")
    recipe_file = result.project_path / "recipe.yaml"
    with open(recipe_file, "r") as f:
        recipe = yaml.safe_load(f)

    fa_url = recipe.get("fa_file_source")
    gtf_url = recipe.get("gtf_file_source")

    assert fa_url is not None, "FAILED in #7! fa_file_source not found in recipe.yaml"
    assert gtf_url is not None, "FAILED in #8! gtf_file_source not found in recipe.yaml"

    for i, sp in enumerate([expected_species, expected_species.lower()]):
        assert (
            sp in fa_url
        ), f"FAILED in #9-{i + 1}! {sp} missing in FASTA URL, got {fa_url}"
        assert (
            sp in gtf_url
        ), f"FAILED in #10-{i + 1}! {sp} missing in GTF URL, got {gtf_url}"

    unexpected_species = {
        "Homo_sapiens": ["Mus_musculus", "mus_musculus"],
        "Mus_musculus": ["Homo_sapiens", "homo_sapiens"],
    }[expected_species]

    for i, sp in enumerate(unexpected_species):
        assert (
            sp not in fa_url
        ), f"FAILED in #11-{i + 1}! {sp} contained in FASTA URL, got {fa_url}"
        assert (
            sp not in gtf_url
        ), f"FAILED in #12-{i + 1}! {sp} contained in GTF URL, got {gtf_url}"

    reference_id = {"Homo_sapiens": "GRCh38", "Mus_musculus": "GRCm39"}[
        expected_species
    ]

    assert (
        reference_id in fa_url
    ), f"FAILED in #13! {reference_id} missing in FASTA URL, got {fa_url}"
    assert (
        reference_id in gtf_url
    ), f"FAILED in #14! {reference_id} missing in GTF URL, got {gtf_url}"

    try:
        fa_response = requests.head(fa_url, allow_redirects=True)
        assert (
            fa_response.status_code == 200
        ), f"FAILED in #16! FASTA URL returned {fa_response.status_code}"

        gtf_response = requests.head(gtf_url, allow_redirects=True)
        assert (
            gtf_response.status_code == 200
        ), f"FAILED in #17! GTF URL returned {gtf_response.status_code}"
    except requests.RequestException as e:
        pytest.fail(f"FAILED in #15! Network request failed: {e}")


def test_correct_template_human(cookies, project_name, essential_files):
    result = cookies.bake(extra_context={"project_name": project_name})
    minimal_tests(result, project_name, essential_files)


def test_correct_template_mouse(cookies, project_name, essential_files):
    expected_species = "Mus_musculus"
    result = cookies.bake(
        extra_context={"project_name": project_name, "species": expected_species}
    )
    minimal_tests(
        result, project_name, essential_files, expected_species=expected_species
    )
