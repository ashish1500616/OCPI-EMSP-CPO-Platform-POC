"""
Mock CPO Server Implementation
==============================

This module implements a complete mock CPO (Charge Point Operator) server
using the extrawest_ocpi library. It provides all CPO role endpoints required
for testing EMSP-CPO interactions according to OCPI 2.2.1 specification.

The mock CPO server:
- Implements all CPO sender/receiver modules
- Provides realistic CPO behavior simulation
- Supports configurable error scenarios
- Runs on port 8001 to avoid conflicts with EMSP backend
"""

import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from py_ocpi import get_application
from py_ocpi.core.authentication.authenticator import Authenticator
from py_ocpi.core.crud import Crud
from py_ocpi.core.enums import ModuleID, RoleEnum
from py_ocpi.modules.versions.enums import VersionNumber

from tests.test_data_factory import TestDataFactory

# Configure logging
logger = logging.getLogger(__name__)


class MockCPOAuthenticator(Authenticator):
    """Mock CPO Authenticator for testing."""

    # Mock CPO tokens for testing
    _valid_tokens_a: List[str] = [
        "cpo_token_a_12345",
        "cpo_token_a_67890",
        "cpo_development_token_a",
    ]

    _valid_tokens_c: List[str] = [
        "emsp_token_c_abcdef",
        "emsp_token_c_ghijkl",
        "emsp_development_token_c",
        "test_token_c_456",
    ]

    @classmethod
    async def get_valid_token_a(cls) -> List[str]:
        """Get valid Token A list for CPO."""
        return cls._valid_tokens_a

    @classmethod
    async def get_valid_token_c(cls) -> List[str]:
        """Get valid Token C list for CPO."""
        return cls._valid_tokens_c

    @classmethod
    async def is_token_valid(cls, token: str) -> bool:
        """
        Check if a token is valid (either Token A or Token C).

        Args:
            token: The token to validate

        Returns:
            True if token is valid, False otherwise
        """
        tokens_a = await cls.get_valid_token_a()
        tokens_c = await cls.get_valid_token_c()

        is_valid = token in tokens_a or token in tokens_c

        if is_valid:
            logger.debug(f"Mock CPO: Token validation successful: {token[:8]}...")
        else:
            logger.warning(f"Mock CPO: Token validation failed: {token[:8]}...")

        return is_valid


class MockCPOCrud(Crud):
    """Mock CPO CRUD implementation with test data."""

    def __init__(self):
        """Initialize mock CPO with test data."""
        self.data_factory = TestDataFactory()
        self._storage: Dict[str, Dict[str, Any]] = {
            "locations": {},
            "sessions": {},
            "cdrs": {},
            "tariffs": {},
            "commands": {},
            "tokens": {},
            "hub_client_info": {},
            "charging_profiles": {},
            "credentials": {},
        }
        self._populate_test_data()

    async def do(self, *args, **kwargs):
        """Required abstract method implementation."""
        # This method is required by the base Crud class but not used in our mock
        pass

    def _populate_test_data(self):
        """Populate mock CPO with realistic test data."""
        # Create test locations
        for i in range(3):
            location = self.data_factory.create_location(
                id=f"LOC{i+1:03d}", name=f"Mock CPO Station {i+1}", party_id="CPO"
            )
            self._storage["locations"][location["id"]] = location

        # Create test tariffs
        for i in range(2):
            tariff = self.data_factory.create_tariff(id=f"TRF{i+1:03d}", party_id="CPO")
            self._storage["tariffs"][tariff["id"]] = tariff

        # Create test sessions
        for i in range(2):
            session = self.data_factory.create_session(
                id=f"SES{i+1:03d}", party_id="CPO", location_id="LOC001"
            )
            self._storage["sessions"][session["id"]] = session

    def _get_storage_key(self, module: ModuleID) -> str:
        """Get storage key for module."""
        module_mapping = {
            ModuleID.locations: "locations",
            ModuleID.sessions: "sessions",
            ModuleID.cdrs: "cdrs",
            ModuleID.tariffs: "tariffs",
            ModuleID.commands: "commands",
            ModuleID.tokens: "tokens",
            ModuleID.hub_client_info: "hub_client_info",
            ModuleID.charging_profile: "charging_profiles",
            ModuleID.credentials_and_registration: "credentials",
        }
        return module_mapping.get(module, "unknown")

    @classmethod
    async def get(
        cls, module: ModuleID, role: RoleEnum, id: str, *args, **kwargs
    ) -> Any:
        """Get a single object by ID."""
        instance = cls()
        storage_key = instance._get_storage_key(module)

        if id in instance._storage[storage_key]:
            logger.info(f"Mock CPO: Retrieved {module.value} with id: {id}")
            return instance._storage[storage_key][id]

        logger.warning(f"Mock CPO: {module.value} with id {id} not found")
        return None

    @classmethod
    async def list(
        cls, module: ModuleID, role: RoleEnum, filters: dict, *args, **kwargs
    ) -> List[Any]:
        """List objects with optional filtering."""
        instance = cls()
        storage_key = instance._get_storage_key(module)

        objects = list(instance._storage[storage_key].values())

        # Apply basic filtering
        if filters:
            filtered_objects = []
            for obj in objects:
                match = True
                for key, value in filters.items():
                    if key in obj and obj[key] != value:
                        match = False
                        break
                if match:
                    filtered_objects.append(obj)
            objects = filtered_objects

        logger.info(f"Mock CPO: Listed {len(objects)} {module.value} objects")
        return objects

    @classmethod
    async def create(
        cls, module: ModuleID, role: RoleEnum, data: dict, *args, **kwargs
    ) -> Any:
        """Create a new object."""
        instance = cls()
        storage_key = instance._get_storage_key(module)

        # Generate ID if not provided
        object_id = data.get("id") or str(uuid.uuid4())

        # Add metadata
        data["id"] = object_id
        data["last_updated"] = datetime.now(timezone.utc).isoformat()

        # Store the object
        instance._storage[storage_key][object_id] = data

        logger.info(f"Mock CPO: Created {module.value} with id: {object_id}")
        return data

    @classmethod
    async def update(
        cls, module: ModuleID, role: RoleEnum, data: dict, id: str, *args, **kwargs
    ) -> Any:
        """Update an existing object."""
        instance = cls()
        storage_key = instance._get_storage_key(module)

        if id in instance._storage[storage_key]:
            # Update existing object
            instance._storage[storage_key][id].update(data)
            instance._storage[storage_key][id]["last_updated"] = datetime.now(
                timezone.utc
            ).isoformat()

            logger.info(f"Mock CPO: Updated {module.value} with id: {id}")
            return instance._storage[storage_key][id]

        logger.warning(f"Mock CPO: {module.value} with id {id} not found for update")
        return None

    @classmethod
    async def delete(
        cls, module: ModuleID, role: RoleEnum, id: str, *args, **kwargs
    ) -> bool:
        """Delete an object."""
        instance = cls()
        storage_key = instance._get_storage_key(module)

        if id in instance._storage[storage_key]:
            del instance._storage[storage_key][id]
            logger.info(f"Mock CPO: Deleted {module.value} with id: {id}")
            return True

        logger.warning(f"Mock CPO: {module.value} with id {id} not found for deletion")
        return False


def create_mock_cpo_application():
    """
    Create and configure the Mock CPO FastAPI application.

    Returns:
        FastAPI: Configured Mock CPO application
    """
    # Define CPO modules according to OCPI 2.2.1 specification
    cpo_modules = [
        # Sender modules (CPO sends data to EMSP)
        ModuleID.locations,  # Location information to EMSPs
        ModuleID.sessions,  # Charging session information
        ModuleID.cdrs,  # Charge Detail Records
        ModuleID.tariffs,  # Tariff information
        ModuleID.hub_client_info,  # Hub client information
        ModuleID.credentials_and_registration,  # Credentials and registration
        # Receiver modules (CPO receives data from EMSP)
        ModuleID.commands,  # Commands from EMSPs
        ModuleID.tokens,  # Token authorization requests
        ModuleID.charging_profile,  # Charging profile management
    ]

    # Create the Mock CPO application
    app = get_application(
        version_numbers=[VersionNumber.v_2_2_1],
        roles=[RoleEnum.cpo],
        crud=MockCPOCrud,
        modules=cpo_modules,
        authenticator=MockCPOAuthenticator,
        # Enable HTTP push for real-time updates
        http_push=True,
        # Disable WebSocket push for simplicity
        websocket_push=False,
    )

    return app


# Create the Mock CPO application instance
mock_cpo_app = create_mock_cpo_application()


@mock_cpo_app.get("/")
async def mock_cpo_root():
    """
    Root endpoint for Mock CPO server.

    Returns:
        dict: Mock CPO service information
    """
    return {
        "service": "Mock OCPI CPO Server",
        "version": "2.2.1",
        "role": "CPO",
        "status": "operational",
        "purpose": "Testing EMSP-CPO interactions",
        "endpoints": {
            "ocpi": "/ocpi/cpo/2.2.1",
            "docs": "/docs",
            "redoc": "/redoc",
        },
        "supported_modules": [
            "locations",
            "sessions",
            "cdrs",
            "tariffs",
            "commands",
            "tokens",
            "hub_client_info",
            "charging_profile",
            "credentials",
        ],
    }


@mock_cpo_app.get("/health")
async def mock_cpo_health():
    """Health check endpoint for Mock CPO server."""
    return {"status": "healthy", "service": "Mock CPO Server"}
