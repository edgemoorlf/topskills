#!/usr/bin/env python3
"""
Python Virtual Environment Setup Helper

Usage:
    python pyenv_setup.py --create
    python pyenv_setup.py --create --python 3.11
    python pyenv_setup.py --activate
    python pyenv_setup.py --install requests beautifulsoup4
    python pyenv_setup.py --install -r requirements.txt
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd: list, cwd: str = None) -> tuple:
    """Run a shell command and return (success, output)."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=cwd,
            check=False
        )
        return result.returncode == 0, result.stdout + result.stderr
    except FileNotFoundError as e:
        return False, str(e)


def check_uv_installed() -> bool:
    """Check if uv is installed."""
    success, _ = run_command(["uv", "--version"])
    return success


def create_venv(python_version: str = None) -> bool:
    """Create a virtual environment using uv."""
    if not check_uv_installed():
        print("❌ uv is not installed.")
        print("   Install with: curl -LsSf https://astral.sh/uv/install.sh | sh")
        return False

    cmd = ["uv", "venv"]
    if python_version:
        cmd.extend(["--python", python_version])

    print(f"🐍 Creating virtual environment{' with Python ' + python_version if python_version else ''}...")
    success, output = run_command(cmd)

    if success:
        print("   ✓ Virtual environment created at .venv/")
        print("\n   Activate with:")
        print("     source .venv/bin/activate  # Unix/Mac")
        print("     .venv\\Scripts\\activate     # Windows")
        return True
    else:
        print(f"   ❌ Failed: {output}")
        return False


def get_activate_command() -> str:
    """Get the activate command for the current platform."""
    venv_path = Path(".venv")

    if not venv_path.exists():
        return None

    if sys.platform == "win32":
        activate_script = venv_path / "Scripts" / "activate"
        if activate_script.exists():
            return f".venv\\Scripts\\activate"
    else:
        activate_script = venv_path / "bin" / "activate"
        if activate_script.exists():
            return "source .venv/bin/activate"

    return None


def show_activate_info():
    """Show how to activate the virtual environment."""
    activate_cmd = get_activate_command()

    if not activate_cmd:
        print("❌ No virtual environment found at .venv/")
        print("   Create one with: uv venv")
        return False

    print("📋 To activate the virtual environment, run:")
    print(f"   {activate_cmd}")
    return True


def install_packages(packages: list, from_requirements: str = None) -> bool:
    """Install packages using uv pip."""
    if not check_uv_installed():
        print("❌ uv is not installed.")
        return False

    # Check if venv exists
    if not Path(".venv").exists():
        print("❌ No virtual environment found.")
        print("   Create one first: uv venv")
        return False

    if from_requirements:
        print(f"📦 Installing from {from_requirements}...")
        cmd = ["uv", "pip", "install", "-r", from_requirements]
    else:
        print(f"📦 Installing packages: {', '.join(packages)}...")
        cmd = ["uv", "pip", "install"] + packages

    # Try with venv Python first
    venv_python = Path(".venv/bin/python")
    if venv_python.exists():
        cmd.extend(["--python", str(venv_python)])

    success, output = run_command(cmd)

    if success:
        print("   ✓ Packages installed successfully")
        return True
    else:
        print(f"   ❌ Failed: {output}")
        return False


def install_uv():
    """Show instructions for installing uv."""
    print("🔧 Installing uv...")
    print()
    print("   macOS/Linux:")
    print("     curl -LsSf https://astral.sh/uv/install.sh | sh")
    print()
    print("   Windows:")
    print("     powershell -c \"irm https://astral.sh/uv/install.ps1 | iex\"")
    print()
    print("   Or with pip:")
    print("     pip install uv")
    print()
    print("   After installation, restart your terminal or run:")
    print("     source $HOME/.cargo/env  # macOS/Linux")


def show_status():
    """Show current environment status."""
    print("📊 Environment Status")
    print("=" * 40)

    # Check uv
    success, version = run_command(["uv", "--version"])
    if success:
        print(f"✓ uv installed: {version.strip()}")
    else:
        print("✗ uv not installed")

    # Check venv
    venv_path = Path(".venv")
    if venv_path.exists():
        print(f"✓ Virtual environment exists at {venv_path.absolute()}")
        activate_cmd = get_activate_command()
        if activate_cmd:
            print(f"  Activate: {activate_cmd}")
    else:
        print("✗ No virtual environment found")

    # Check if activated
    if os.environ.get("VIRTUAL_ENV"):
        print(f"✓ Virtual environment is ACTIVE: {os.environ.get('VIRTUAL_ENV')}")
    else:
        print("✗ No virtual environment is currently active")


def main():
    parser = argparse.ArgumentParser(
        description="Python Virtual Environment Setup Helper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Create a new virtual environment
    python pyenv_setup.py --create

    # Create with specific Python version
    python pyenv_setup.py --create --python 3.11

    # Show activation command
    python pyenv_setup.py --activate

    # Install packages
    python pyenv_setup.py --install requests beautifulsoup4

    # Install from requirements.txt
    python pyenv_setup.py --install -r requirements.txt

    # Show environment status
    python pyenv_setup.py --status

    # Show uv installation instructions
    python pyenv_setup.py --install-uv
        """
    )

    parser.add_argument("--create", action="store_true",
                       help="Create a new virtual environment")
    parser.add_argument("--python", type=str, metavar="VERSION",
                       help="Python version to use (e.g., 3.11)")
    parser.add_argument("--activate", action="store_true",
                       help="Show activation command")
    parser.add_argument("--install", nargs="+", metavar="PACKAGE",
                       help="Install packages")
    parser.add_argument("-r", "--requirements", type=str, metavar="FILE",
                       help="Install from requirements file")
    parser.add_argument("--install-uv", action="store_true",
                       help="Show uv installation instructions")
    parser.add_argument("--status", action="store_true",
                       help="Show environment status")

    args = parser.parse_args()

    # Default to status if no args
    if len(sys.argv) == 1:
        args.status = True

    success = True

    if args.install_uv:
        install_uv()
    elif args.create:
        success = create_venv(args.python)
    elif args.activate:
        success = show_activate_info()
    elif args.install:
        success = install_packages(args.install, args.requirements)
    elif args.status:
        show_status()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
