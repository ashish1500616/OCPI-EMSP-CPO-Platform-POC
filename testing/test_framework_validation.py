#!/usr/bin/env python3
"""
Testing Framework Validation Script
===================================

This script validates that the OCPI EMSP testing framework is properly
set up and all components can be imported and initialized correctly.
"""

import sys
import os
import traceback

def test_imports():
    """Test that all framework components can be imported."""
    print("🔍 Testing framework imports...")
    
    try:
        # Test main application imports
        from main import create_emsp_application
        from auth import ClientAuthenticator
        from crud import EMSPCrud
        from config import settings
        print("✅ Main application components imported successfully")
        
        # Test framework imports
        from tests.mock_cpo_server import create_mock_cpo_application, MockCPOCrud, MockCPOAuthenticator
        from tests.test_data_factory import TestDataFactory
        print("✅ Testing framework components imported successfully")
        
        # Test pytest and testing dependencies
        import pytest
        import httpx
        from fastapi.testclient import TestClient
        print("✅ Testing dependencies imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure to install dependencies: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during imports: {e}")
        traceback.print_exc()
        return False

def test_applications():
    """Test that applications can be created."""
    print("\n🏗️  Testing application creation...")
    
    try:
        # Test EMSP application creation
        from main import create_emsp_application
        emsp_app = create_emsp_application()
        print("✅ EMSP application created successfully")
        
        # Test Mock CPO application creation
        from tests.mock_cpo_server import create_mock_cpo_application
        mock_cpo_app = create_mock_cpo_application()
        print("✅ Mock CPO application created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Application creation error: {e}")
        traceback.print_exc()
        return False

def test_data_factory():
    """Test that test data factory works."""
    print("\n🏭 Testing data factory...")
    
    try:
        from tests.test_data_factory import TestDataFactory
        
        factory = TestDataFactory()
        
        # Test data generation
        location = factory.create_location()
        session = factory.create_session()
        token = factory.create_token()
        command = factory.create_command()
        
        # Validate generated data
        assert "id" in location
        assert "name" in location
        assert "evses" in location
        
        assert "id" in session
        assert "status" in session
        assert "kwh" in session
        
        assert "uid" in token
        assert "type" in token
        assert "valid" in token
        
        assert "response_url" in command
        assert "token" in command
        
        print("✅ Test data factory working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Data factory error: {e}")
        traceback.print_exc()
        return False

def test_authentication():
    """Test authentication components."""
    print("\n🔐 Testing authentication...")
    
    try:
        from auth import ClientAuthenticator
        from tests.mock_cpo_server import MockCPOAuthenticator
        
        # Test EMSP authenticator
        import asyncio
        
        async def test_auth():
            # Test token validation
            valid_token = "emsp_token_a_12345"
            is_valid = await ClientAuthenticator.is_token_valid(valid_token)
            assert is_valid is True
            
            invalid_token = "invalid_token"
            is_valid = await ClientAuthenticator.is_token_valid(invalid_token)
            assert is_valid is False
            
            # Test Mock CPO authenticator
            cpo_token = "cpo_token_a_12345"
            is_valid = await MockCPOAuthenticator.is_token_valid(cpo_token)
            assert is_valid is True
        
        asyncio.run(test_auth())
        print("✅ Authentication components working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        traceback.print_exc()
        return False

def test_crud_operations():
    """Test CRUD operations."""
    print("\n💾 Testing CRUD operations...")
    
    try:
        from crud import EMSPCrud
        from tests.mock_cpo_server import MockCPOCrud
        from py_ocpi.core.enums import RoleEnum, ModuleID
        
        import asyncio
        
        async def test_crud():
            # Test EMSP CRUD
            test_data = {"id": "test_123", "name": "Test Location"}
            created = await EMSPCrud.create(ModuleID.locations, RoleEnum.emsp, test_data)
            assert created["id"] == "test_123"
            
            # Test Mock CPO CRUD
            mock_crud = MockCPOCrud()
            locations = await MockCPOCrud.list(ModuleID.locations, RoleEnum.cpo, {})
            assert isinstance(locations, list)
        
        asyncio.run(test_crud())
        print("✅ CRUD operations working correctly")
        return True
        
    except Exception as e:
        print(f"❌ CRUD operations error: {e}")
        traceback.print_exc()
        return False

def test_configuration():
    """Test configuration."""
    print("\n⚙️  Testing configuration...")
    
    try:
        from config import settings
        
        # Test configuration access
        assert hasattr(settings, 'PROJECT_NAME')
        assert hasattr(settings, 'OCPI_HOST')
        assert hasattr(settings, 'COUNTRY_CODE')
        assert hasattr(settings, 'PARTY_ID')
        
        print(f"✅ Configuration loaded: {settings.PROJECT_NAME}")
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        traceback.print_exc()
        return False

def test_pytest_setup():
    """Test pytest configuration."""
    print("\n🧪 Testing pytest setup...")
    
    try:
        # Check if pytest.ini exists
        if os.path.exists("pytest.ini"):
            print("✅ pytest.ini configuration found")
        else:
            print("⚠️  pytest.ini not found (optional)")
        
        # Check if conftest.py exists
        if os.path.exists("tests/conftest.py"):
            print("✅ tests/conftest.py found")
        else:
            print("❌ tests/conftest.py not found")
            return False
        
        # Test that pytest can discover tests
        import subprocess
        result = subprocess.run(
            ["python", "-m", "pytest", "--collect-only", "-q", "tests/"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ pytest can discover tests")
            return True
        else:
            print(f"❌ pytest test discovery failed: {result.stderr}")
            return False
        
    except Exception as e:
        print(f"❌ pytest setup error: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all validation tests."""
    print("🚀 OCPI EMSP Testing Framework Validation")
    print("=" * 60)
    
    tests = [
        ("Import Tests", test_imports),
        ("Application Creation", test_applications),
        ("Data Factory", test_data_factory),
        ("Authentication", test_authentication),
        ("CRUD Operations", test_crud_operations),
        ("Configuration", test_configuration),
        ("Pytest Setup", test_pytest_setup),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        print("-" * 40)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Validation Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All validation tests passed! Framework is ready to use.")
        print("\n💡 Next steps:")
        print("   1. Run tests: python run_tests.py")
        print("   2. Run specific test types: python run_tests.py unit")
        print("   3. View reports in tests/reports/")
        return True
    else:
        print("💥 Some validation tests failed. Please fix the issues above.")
        print("\n💡 Common fixes:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Check Python path and working directory")
        print("   3. Ensure all files are in correct locations")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
