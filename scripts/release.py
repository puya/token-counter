#!/usr/bin/env python3
"""
Release automation script for token-counter-cli.
Usage: python scripts/release.py [patch|minor|major]
"""

import re
import subprocess
import sys
from pathlib import Path

def get_current_version():
    """Get current version from pyproject.toml"""
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()
    match = re.search(r'version = "([^"]+)"', content)
    if not match:
        raise ValueError("Could not find version in pyproject.toml")
    return match.group(1)

def bump_version(current_version, bump_type):
    """Bump version based on type (patch, minor, major)"""
    major, minor, patch = map(int, current_version.split('.'))
    
    if bump_type == "patch":
        patch += 1
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    else:
        raise ValueError("bump_type must be 'patch', 'minor', or 'major'")
    
    return f"{major}.{minor}.{patch}"

def update_version_in_file(new_version):
    """Update version in pyproject.toml"""
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()
    updated_content = re.sub(
        r'version = "[^"]+"',
        f'version = "{new_version}"',
        content
    )
    pyproject_path.write_text(updated_content)

def run_command(cmd, check=True):
    """Run a shell command"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ['patch', 'minor', 'major']:
        print("Usage: python scripts/release.py [patch|minor|major]")
        sys.exit(1)
    
    bump_type = sys.argv[1]
    
    # Ensure we're on main branch and clean
    branch_result = run_command("git branch --show-current")
    if branch_result.stdout.strip() != "main":
        print("Error: Must be on main branch")
        sys.exit(1)
    
    status_result = run_command("git status --porcelain")
    if status_result.stdout.strip():
        print("Error: Working directory must be clean")
        sys.exit(1)
    
    # Get current version and bump it
    current_version = get_current_version()
    new_version = bump_version(current_version, bump_type)
    
    print(f"Bumping version from {current_version} to {new_version}")
    
    # Update version in pyproject.toml
    update_version_in_file(new_version)
    
    # Commit, tag, and push
    run_command(f"git add pyproject.toml")
    run_command(f'git commit -m "Bump version to {new_version}"')
    run_command(f"git tag v{new_version}")
    run_command("git push origin main --tags")
    
    print(f"✅ Release v{new_version} initiated!")
    print(f"🚀 GitHub Actions will automatically:")
    print(f"   - Build and publish to PyPI")
    print(f"   - Create GitHub release")
    print(f"📦 View release: https://github.com/puya/token-counter-cli/releases/tag/v{new_version}")

if __name__ == "__main__":
    main() 