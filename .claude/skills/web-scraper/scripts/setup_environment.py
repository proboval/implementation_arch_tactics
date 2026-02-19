#!/usr/bin/env python3
"""
Environment Setup for Web Scraper Skill
Manages virtual environment and dependencies automatically
"""

import os
import sys
import subprocess
import venv
from pathlib import Path

# Fix Windows console encoding for emoji support
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')


class SkillEnvironment:
    """Manages skill-specific virtual environment"""

    def __init__(self):
        self.skill_dir = Path(__file__).parent.parent
        self.venv_dir = self.skill_dir / ".venv"
        self.requirements_file = self.skill_dir / "requirements.txt"

        if os.name == 'nt':  # Windows
            self.venv_python = self.venv_dir / "Scripts" / "python.exe"
            self.venv_pip = self.venv_dir / "Scripts" / "pip.exe"
        else:  # Unix/Linux/Mac
            self.venv_python = self.venv_dir / "bin" / "python"
            self.venv_pip = self.venv_dir / "bin" / "pip"

    def ensure_venv(self) -> bool:
        """Ensure virtual environment exists and is set up"""
        if self.is_in_skill_venv():
            print("Already running in skill virtual environment")
            return True

        if not self.venv_dir.exists():
            print(f"Creating virtual environment in {self.venv_dir.name}/")
            try:
                venv.create(self.venv_dir, with_pip=True)
                print("Virtual environment created")
            except Exception as e:
                print(f"Failed to create venv: {e}")
                return False

        if self.requirements_file.exists():
            print("Installing dependencies...")
            try:
                subprocess.run(
                    [str(self.venv_pip), "install", "--upgrade", "pip"],
                    check=True,
                    capture_output=True,
                    text=True
                )

                result = subprocess.run(
                    [str(self.venv_pip), "install", "-r", str(self.requirements_file)],
                    check=True,
                    capture_output=True,
                    text=True
                )
                print("Dependencies installed")

                # Install Chrome for Patchright (not Chromium!)
                print("Installing Google Chrome for Patchright...")
                try:
                    subprocess.run(
                        [str(self.venv_python), "-m", "patchright", "install", "chrome"],
                        check=True,
                        capture_output=True,
                        text=True
                    )
                    print("Chrome installed")
                except subprocess.CalledProcessError as e:
                    print(f"Warning: Failed to install Chrome: {e}")
                    print("   You may need to run manually: python -m patchright install chrome")

                return True
            except subprocess.CalledProcessError as e:
                print(f"Failed to install dependencies: {e}")
                return False
        else:
            print("No requirements.txt found, skipping dependency installation")
            return True

    def is_in_skill_venv(self) -> bool:
        """Check if we're already running in the skill's venv"""
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            venv_path = Path(sys.prefix)
            return venv_path == self.venv_dir
        return False

    def get_python_executable(self) -> str:
        """Get the correct Python executable to use"""
        if self.venv_python.exists():
            return str(self.venv_python)
        return sys.executable

    def run_script(self, script_name: str, args: list = None) -> int:
        """Run a script with the virtual environment"""
        script_path = self.skill_dir / "scripts" / script_name

        if not script_path.exists():
            print(f"Script not found: {script_path}")
            return 1

        if not self.ensure_venv():
            print("Failed to set up environment")
            return 1

        cmd = [str(self.venv_python), str(script_path)]
        if args:
            cmd.extend(args)

        print(f"Running: {script_name} with venv Python")

        try:
            result = subprocess.run(cmd)
            return result.returncode
        except Exception as e:
            print(f"Failed to run script: {e}")
            return 1

    def activate_instructions(self) -> str:
        """Get instructions for manual activation"""
        if os.name == 'nt':
            activate = self.venv_dir / "Scripts" / "activate.bat"
            return f"Run: {activate}"
        else:
            activate = self.venv_dir / "bin" / "activate"
            return f"Run: source {activate}"


def main():
    """Main entry point for environment setup"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Setup Web Scraper skill environment'
    )
    parser.add_argument('--check', action='store_true', help='Check if environment is set up')
    parser.add_argument('--run', help='Run a script with the venv')
    parser.add_argument('args', nargs='*', help='Arguments to pass to the script')

    args = parser.parse_args()
    env = SkillEnvironment()

    if args.check:
        if env.venv_dir.exists():
            print(f"Virtual environment exists: {env.venv_dir}")
            print(f"   Python: {env.get_python_executable()}")
            print(f"   To activate manually: {env.activate_instructions()}")
        else:
            print("No virtual environment found")
            print("   Run setup_environment.py to create it")
        return

    if args.run:
        return env.run_script(args.run, args.args)

    if env.ensure_venv():
        print(f"\nEnvironment ready!")
        print(f"   Virtual env: {env.venv_dir}")
        print(f"   Python: {env.get_python_executable()}")
        print(f"\nTo activate manually: {env.activate_instructions()}")
    else:
        print("\nEnvironment setup failed")
        return 1


if __name__ == "__main__":
    sys.exit(main() or 0)