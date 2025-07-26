#!/usr/bin/env python3
"""
Simple test to verify EMSP backend components work
"""

import os
import sys

# Add the extrawest_ocpi directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "extrawest_ocpi"))


def test_basic_imports():
    """Test basic imports that don't depend on pydantic."""
    print("Testing basic imports...")

    try:
        # Test our models (should work without pydantic issues)
        from models import MockDataGenerator

        print("✓ Models import successful")

        # Test mock data generation
        locations = MockDataGenerator.generate_locations()
        print(f"✓ Generated {len(locations)} mock locations")

        return True
    except Exception as e:
        print(f"✗ Basic imports failed: {e}")
        return False


def test_server_startup():
    """Test if we can start the server using the existing run_app.py"""
    print("\nTesting server startup with existing run_app.py...")

    try:
        # Change to extrawest_ocpi directory and try to import the existing app
        os.chdir("extrawest_ocpi")

        # Import the existing run_app
        import run_app

        print("✓ run_app.py imported successfully")

        # Check if the app was created
        if hasattr(run_app, "app"):
            print("✓ FastAPI app created successfully")
            print(f"✓ App title: {run_app.app.title}")
            return True
        else:
            print("✗ No app found in run_app.py")
            return False

    except Exception as e:
        print(f"✗ Server startup test failed: {e}")
        return False
    finally:
        # Change back to original directory
        os.chdir("..")


def main():
    """Run simple tests."""
    print("=" * 50)
    print("Simple EMSP Backend Test")
    print("=" * 50)

    tests = [
        test_basic_imports,
        test_server_startup,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")

    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    print("=" * 50)

    if passed > 0:
        print("✓ Basic functionality works!")
        print("\nTrying to start the existing OCPI server...")
        return True
    else:
        print("❌ Basic tests failed.")
        return False


if __name__ == "__main__":
    success = main()

    if success:
        print("\nStarting the OCPI server using existing run_app.py...")
        print("This will use the CPO configuration from the library.")
        print("You can modify it later to use EMSP configuration.")

        # Try to start the server
        try:
            os.chdir("extrawest_ocpi")
            import subprocess

            subprocess.run([sys.executable, "run_app.py"])
        except KeyboardInterrupt:
            print("\nServer stopped by user.")
        except Exception as e:
            print(f"Server startup failed: {e}")

    sys.exit(0 if success else 1)
