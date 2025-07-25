#!/usr/bin/env python3
"""
OCPI EMSP Backend Test Runner
============================

This script provides a convenient way to run different types of tests
for the OCPI EMSP backend testing framework.

Usage:
    python run_tests.py [test_type] [options]

Test Types:
    all         - Run all tests (default)
    unit        - Run only unit tests
    integration - Run only integration tests
    compliance  - Run only compliance tests
    performance - Run only performance tests
    quick       - Run quick tests (unit + integration, no performance)

Options:
    --parallel  - Run tests in parallel
    --coverage  - Generate coverage report
    --html      - Generate HTML report
    --verbose   - Verbose output
    --help      - Show this help message
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, description=""):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    if description:
        print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print(f"\n✅ {description or 'Command'} completed successfully")
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description or 'Command'} failed with exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"\n❌ Command not found: {cmd[0]}")
        print("Make sure pytest is installed: pip install -r requirements.txt")
        return False


def ensure_directories():
    """Ensure test report directories exist."""
    report_dirs = [
        "tests/reports",
        "tests/reports/coverage",
    ]
    
    for dir_path in report_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"📁 Created directory: {dir_path}")


def run_tests(test_type="all", parallel=False, coverage=True, html=True, verbose=False):
    """Run tests based on specified type and options."""
    
    # Ensure report directories exist
    ensure_directories()
    
    # Base pytest command
    cmd = ["python", "-m", "pytest"]
    
    # Add test type markers
    if test_type == "unit":
        cmd.extend(["-m", "unit"])
    elif test_type == "integration":
        cmd.extend(["-m", "integration"])
    elif test_type == "compliance":
        cmd.extend(["-m", "compliance"])
    elif test_type == "performance":
        cmd.extend(["-m", "performance"])
    elif test_type == "quick":
        cmd.extend(["-m", "unit or integration"])
    elif test_type == "all":
        # Run all tests (no marker filter)
        pass
    else:
        print(f"❌ Unknown test type: {test_type}")
        return False
    
    # Add parallel execution
    if parallel:
        cmd.extend(["-n", "auto"])
    
    # Add coverage
    if coverage:
        cmd.extend([
            "--cov=.",
            "--cov-report=html:tests/reports/coverage",
            "--cov-report=term-missing",
            "--cov-report=xml:tests/reports/coverage.xml"
        ])
    
    # Add HTML report
    if html:
        cmd.extend([
            "--html=tests/reports/report.html",
            "--self-contained-html"
        ])
    
    # Add JUnit XML for CI/CD
    cmd.extend(["--junitxml=tests/reports/junit.xml"])
    
    # Add verbosity
    if verbose:
        cmd.append("-v")
    else:
        cmd.append("-q")
    
    # Add test path
    cmd.append("tests/")
    
    # Run the tests
    description = f"OCPI EMSP Backend Tests ({test_type})"
    success = run_command(cmd, description)
    
    if success:
        print(f"\n🎉 All {test_type} tests passed!")
        print(f"📊 Reports generated in tests/reports/")
        if html:
            print(f"🌐 HTML report: tests/reports/report.html")
        if coverage:
            print(f"📈 Coverage report: tests/reports/coverage/index.html")
    else:
        print(f"\n💥 Some {test_type} tests failed!")
        print(f"📋 Check the reports in tests/reports/ for details")
    
    return success


def install_dependencies():
    """Install test dependencies."""
    print("📦 Installing test dependencies...")
    cmd = ["pip", "install", "-r", "requirements.txt"]
    return run_command(cmd, "Installing dependencies")


def check_environment():
    """Check if the test environment is properly set up."""
    print("🔍 Checking test environment...")
    
    # Check if pytest is available
    try:
        result = subprocess.run(["python", "-m", "pytest", "--version"], 
                              capture_output=True, text=True, check=True)
        print(f"✅ pytest version: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ pytest not found. Installing dependencies...")
        if not install_dependencies():
            return False
    
    # Check if main modules can be imported
    try:
        import main
        import auth
        import crud
        import config
        print("✅ Main modules can be imported")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're in the correct directory and dependencies are installed")
        return False
    
    return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="OCPI EMSP Backend Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        "test_type",
        nargs="?",
        default="all",
        choices=["all", "unit", "integration", "compliance", "performance", "quick"],
        help="Type of tests to run (default: all)"
    )
    
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Run tests in parallel"
    )
    
    parser.add_argument(
        "--no-coverage",
        action="store_true",
        help="Disable coverage reporting"
    )
    
    parser.add_argument(
        "--no-html",
        action="store_true",
        help="Disable HTML report generation"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose output"
    )
    
    parser.add_argument(
        "--install-deps",
        action="store_true",
        help="Install dependencies before running tests"
    )
    
    parser.add_argument(
        "--check-env",
        action="store_true",
        help="Check environment setup"
    )
    
    args = parser.parse_args()
    
    print("🚀 OCPI EMSP Backend Test Runner")
    print("=" * 60)
    
    # Install dependencies if requested
    if args.install_deps:
        if not install_dependencies():
            sys.exit(1)
    
    # Check environment if requested or if running tests
    if args.check_env or not args.install_deps:
        if not check_environment():
            print("\n💡 Try running with --install-deps to install missing dependencies")
            sys.exit(1)
    
    # Run tests
    success = run_tests(
        test_type=args.test_type,
        parallel=args.parallel,
        coverage=not args.no_coverage,
        html=not args.no_html,
        verbose=args.verbose
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
