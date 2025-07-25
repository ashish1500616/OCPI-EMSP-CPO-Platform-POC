#!/usr/bin/env python3
"""
Test script for EMSP backend implementation
==========================================

This script tests the EMSP backend components without running the full server.
It validates that all components are properly implemented and can be imported.
"""

import sys
import os

# Add the extrawest_ocpi directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'extrawest_ocpi'))

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        # Test py_ocpi imports
        from py_ocpi import get_application
        from py_ocpi.core.enums import RoleEnum, ModuleID
        from py_ocpi.modules.versions.enums import VersionNumber
        print("✓ py_ocpi imports successful")
        
        # Test our custom modules
        from auth import ClientAuthenticator
        from crud import EMSPCrud
        from config import settings
        from models import MockDataGenerator
        print("✓ Custom module imports successful")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_authenticator():
    """Test the ClientAuthenticator implementation."""
    print("\nTesting ClientAuthenticator...")
    
    try:
        from auth import ClientAuthenticator
        
        # Test token methods
        import asyncio
        
        async def test_auth():
            tokens_a = await ClientAuthenticator.get_valid_token_a()
            tokens_c = await ClientAuthenticator.get_valid_token_c()
            
            print(f"✓ Token A count: {len(tokens_a)}")
            print(f"✓ Token C count: {len(tokens_c)}")
            
            # Test token validation
            if tokens_c:
                is_valid = await ClientAuthenticator.is_token_valid(tokens_c[0])
                print(f"✓ Token validation works: {is_valid}")
            
            return True
        
        return asyncio.run(test_auth())
        
    except Exception as e:
        print(f"✗ Authenticator test failed: {e}")
        return False

def test_crud():
    """Test the EMSPCrud implementation."""
    print("\nTesting EMSPCrud...")
    
    try:
        from crud import EMSPCrud
        from py_ocpi.core.enums import ModuleID, RoleEnum
        import asyncio
        
        async def test_crud_ops():
            # Test creating a location
            test_data = {
                "id": "TEST001",
                "name": "Test Location",
                "address": "123 Test St"
            }
            
            created = await EMSPCrud.create(
                ModuleID.locations, 
                RoleEnum.emsp, 
                test_data
            )
            print(f"✓ Create operation successful: {created['id']}")
            
            # Test getting the location
            retrieved = await EMSPCrud.get(
                ModuleID.locations,
                RoleEnum.emsp,
                created['id']
            )
            print(f"✓ Get operation successful: {retrieved['name']}")
            
            # Test listing locations
            locations, total, is_last = await EMSPCrud.list(
                ModuleID.locations,
                RoleEnum.emsp,
                {"offset": 0, "limit": 10}
            )
            print(f"✓ List operation successful: {total} total locations")
            
            return True
        
        return asyncio.run(test_crud_ops())
        
    except Exception as e:
        print(f"✗ CRUD test failed: {e}")
        return False

def test_config():
    """Test the configuration."""
    print("\nTesting Configuration...")
    
    try:
        from config import settings
        
        print(f"✓ Project Name: {settings.PROJECT_NAME}")
        print(f"✓ OCPI Host: {settings.OCPI_HOST}")
        print(f"✓ Country Code: {settings.COUNTRY_CODE}")
        print(f"✓ Party ID: {settings.PARTY_ID}")
        print(f"✓ Base URL: {settings.base_url}")
        print(f"✓ OCPI Base URL: {settings.ocpi_base_url}")
        
        return True
        
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def test_mock_data():
    """Test the mock data generation."""
    print("\nTesting Mock Data...")
    
    try:
        from models import MockDataGenerator, get_mock_data
        
        locations = MockDataGenerator.generate_locations()
        sessions = MockDataGenerator.generate_sessions()
        cdrs = MockDataGenerator.generate_cdrs()
        tariffs = MockDataGenerator.generate_tariffs()
        tokens = MockDataGenerator.generate_tokens()
        
        print(f"✓ Generated {len(locations)} mock locations")
        print(f"✓ Generated {len(sessions)} mock sessions")
        print(f"✓ Generated {len(cdrs)} mock CDRs")
        print(f"✓ Generated {len(tariffs)} mock tariffs")
        print(f"✓ Generated {len(tokens)} mock tokens")
        
        # Test get_mock_data function
        mock_locations = get_mock_data("locations")
        print(f"✓ Mock data retrieval works: {len(mock_locations)} locations")
        
        return True
        
    except Exception as e:
        print(f"✗ Mock data test failed: {e}")
        return False

def test_application_creation():
    """Test creating the FastAPI application."""
    print("\nTesting Application Creation...")
    
    try:
        from py_ocpi import get_application
        from py_ocpi.core.enums import RoleEnum, ModuleID
        from py_ocpi.modules.versions.enums import VersionNumber
        from auth import ClientAuthenticator
        from crud import EMSPCrud
        
        # Define EMSP modules
        emsp_modules = [
            ModuleID.locations,
            ModuleID.sessions,
            ModuleID.cdrs,
            ModuleID.tariffs,
            ModuleID.commands,
            ModuleID.tokens,
            ModuleID.hub_client_info,
            ModuleID.charging_profile,
            ModuleID.credentials_and_registration,
        ]
        
        # Create the application
        app = get_application(
            version_numbers=[VersionNumber.v_2_2_1],
            roles=[RoleEnum.emsp],
            crud=EMSPCrud,
            modules=emsp_modules,
            authenticator=ClientAuthenticator,
            http_push=True,
            websocket_push=False,
        )
        
        print(f"✓ FastAPI application created successfully")
        print(f"✓ Application title: {app.title}")
        print(f"✓ Number of routes: {len(app.routes)}")
        
        return True
        
    except Exception as e:
        print(f"✗ Application creation failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("EMSP Backend Implementation Test")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_config,
        test_mock_data,
        test_authenticator,
        test_crud,
        test_application_creation,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("🎉 All tests passed! The EMSP backend is ready to use.")
        print("\nTo start the server, run:")
        print("  python main.py")
        print("\nOr with uvicorn directly:")
        print("  uvicorn main:app --reload --host 0.0.0.0 --port 8000")
        return True
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
