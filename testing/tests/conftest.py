"""
Pytest Configuration and Shared Fixtures
=========================================

This module provides pytest configuration and shared fixtures for the OCPI EMSP
testing framework. It includes fixtures for mock CPO server, test clients,
and common test data.
"""

import asyncio
import os
import sys
from typing import AsyncGenerator, Generator
import pytest
import pytest_asyncio
import httpx
from fastapi.testclient import TestClient

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import create_emsp_application
from tests.mock_cpo_server import create_mock_cpo_application
from tests.test_data_factory import TestDataFactory


@pytest_asyncio.fixture(scope="session")
async def emsp_app():
    """Create EMSP FastAPI application for testing."""
    return create_emsp_application()


@pytest_asyncio.fixture(scope="session")
async def mock_cpo_app():
    """Create Mock CPO FastAPI application for testing."""
    return create_mock_cpo_application()


@pytest_asyncio.fixture(scope="session")
async def emsp_client(emsp_app) -> TestClient:
    """Create test client for EMSP application."""
    return TestClient(await emsp_app)


@pytest_asyncio.fixture(scope="session")
async def mock_cpo_client(mock_cpo_app) -> TestClient:
    """Create test client for Mock CPO application."""
    return TestClient(await mock_cpo_app)


@pytest_asyncio.fixture(scope="session")
async def async_emsp_client(emsp_app) -> AsyncGenerator[httpx.AsyncClient, None]:
    """Create async test client for EMSP application."""
    async with httpx.AsyncClient(
        app=emsp_app, 
        base_url="http://testserver"
    ) as client:
        yield client


@pytest_asyncio.fixture(scope="session")
async def async_mock_cpo_client(mock_cpo_app) -> AsyncGenerator[httpx.AsyncClient, None]:
    """Create async test client for Mock CPO application."""
    async with httpx.AsyncClient(
        app=mock_cpo_app, 
        base_url="http://testserver:8001"
    ) as client:
        yield client


@pytest.fixture
def test_data_factory() -> TestDataFactory:
    """Create test data factory instance."""
    return TestDataFactory()


@pytest.fixture
def emsp_auth_headers() -> dict:
    """Standard EMSP authentication headers for testing."""
    return {
        "Authorization": "Token emsp_token_a_12345",
        "Content-Type": "application/json",
        "X-Request-ID": "test-request-123",
        "X-Correlation-ID": "test-correlation-456"
    }


@pytest.fixture
def cpo_auth_headers() -> dict:
    """Standard CPO authentication headers for testing."""
    return {
        "Authorization": "Token cpo_token_c_abcdef",
        "Content-Type": "application/json",
        "X-Request-ID": "test-cpo-request-789",
        "X-Correlation-ID": "test-cpo-correlation-012"
    }


@pytest.fixture
def ocpi_headers() -> dict:
    """Standard OCPI headers for testing."""
    return {
        "OCPI-from-country-code": "US",
        "OCPI-from-party-id": "EMS",
        "OCPI-to-country-code": "US", 
        "OCPI-to-party-id": "CPO"
    }


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "compliance: marks tests as OCPI compliance tests"
    )
    config.addinivalue_line(
        "markers", "performance: marks tests as performance tests"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow running"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test location."""
    for item in items:
        # Add markers based on test file location
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "compliance" in str(item.fspath):
            item.add_marker(pytest.mark.compliance)
        elif "performance" in str(item.fspath):
            item.add_marker(pytest.mark.performance)
            item.add_marker(pytest.mark.slow)