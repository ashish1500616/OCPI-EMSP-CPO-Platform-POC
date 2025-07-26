"""
EMSP CRUD Operations Implementation
==================================

This module implements all CRUD operations required for an OCPI-compliant EMSP backend.
It extends the py_ocpi.core.crud.Crud base class and provides implementations for all
EMSP modules including locations, sessions, CDRs, tariffs, commands, tokens, and more.

The implementation includes:
- Mock data for development and testing
- Proper OCPI response formatting
- Error handling and validation
- Support for all EMSP modules
"""

import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from py_ocpi.core.crud import Crud
from py_ocpi.core.enums import Action, ModuleID, RoleEnum
from py_ocpi.core.exceptions import NotFoundOCPIError

# Configure logging
logger = logging.getLogger(__name__)


class EMSPCrud(Crud):
    """
    EMSP CRUD implementation with mock data storage.

    This class provides all CRUD operations required for EMSP functionality.
    In a production environment, replace the mock data storage with actual
    database operations.
    """

    # Mock data storage - replace with actual database in production
    _storage: Dict[str, Dict[str, Any]] = {
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

    @classmethod
    async def get(cls, module: ModuleID, role: RoleEnum, id: str, *args, **kwargs) -> Any:
        """
        Get a single object by ID.

        Args:
            module: The OCPI module
            role: The role of the caller
            id: The ID of the object to retrieve
            **kwargs: Additional parameters (auth_token, version, etc.)

        Returns:
            The requested object data

        Raises:
            NotFoundOCPIError: If the object is not found
        """
        logger.info(f"Getting {module.value} with id: {id}")

        storage_key = cls._get_storage_key(module)

        if id not in cls._storage[storage_key]:
            logger.warning(f"Object not found: {module.value} with id {id}")
            raise NotFoundOCPIError

        data = cls._storage[storage_key][id]
        logger.debug(f"Retrieved {module.value}: {data}")

        return data

    @classmethod
    async def list(
        cls, module: ModuleID, role: RoleEnum, filters: dict, *args, **kwargs
    ) -> Tuple[List[Any], int, bool]:
        """
        Get a list of objects with pagination.

        Args:
            module: The OCPI module
            role: The role of the caller
            filters: OCPI pagination filters (offset, limit, date_from, date_to)
            **kwargs: Additional parameters

        Returns:
            Tuple of (objects_list, total_count, is_last_page)
        """
        logger.info(f"Listing {module.value} with filters: {filters}")

        storage_key = cls._get_storage_key(module)
        all_objects = list(cls._storage[storage_key].values())

        # Apply basic filtering (in production, implement proper filtering)
        offset = filters.get("offset", 0)
        limit = filters.get("limit", 50)

        # Simple pagination
        total_count = len(all_objects)
        start_idx = offset
        end_idx = min(offset + limit, total_count)

        objects_list = all_objects[start_idx:end_idx]
        is_last_page = end_idx >= total_count

        logger.debug(f"Returning {len(objects_list)} {module.value} objects")

        return objects_list, total_count, is_last_page

    @classmethod
    async def create(cls, module: ModuleID, role: RoleEnum, data: dict, *args, **kwargs) -> Any:
        """
        Create a new object.

        Args:
            module: The OCPI module
            role: The role of the caller
            data: The object data to create
            **kwargs: Additional parameters

        Returns:
            The created object data
        """
        logger.info(f"Creating {module.value} with data: {data}")

        storage_key = cls._get_storage_key(module)

        # Generate ID if not provided
        object_id = data.get("id") or str(uuid.uuid4())

        # Add metadata
        data["id"] = object_id
        data["last_updated"] = datetime.now(timezone.utc).isoformat()

        # Store the object
        cls._storage[storage_key][object_id] = data

        logger.debug(f"Created {module.value} with id: {object_id}")

        return data

    @classmethod
    async def update(
        cls,
        module: ModuleID,
        role: RoleEnum,
        data: dict,
        id: str,
        *args,
        **kwargs,
    ) -> Any:
        """
        Update an existing object.

        Args:
            module: The OCPI module
            role: The role of the caller
            data: The updated object data
            id: The ID of the object to update
            **kwargs: Additional parameters

        Returns:
            The updated object data

        Raises:
            NotFoundOCPIError: If the object is not found
        """
        logger.info(f"Updating {module.value} with id: {id}")

        storage_key = cls._get_storage_key(module)

        if id not in cls._storage[storage_key]:
            logger.warning(f"Object not found for update: {module.value} with id {id}")
            raise NotFoundOCPIError

        # Update the object
        existing_data = cls._storage[storage_key][id]
        existing_data.update(data)
        existing_data["last_updated"] = datetime.now(timezone.utc).isoformat()

        cls._storage[storage_key][id] = existing_data

        logger.debug(f"Updated {module.value} with id: {id}")

        return existing_data

    @classmethod
    async def delete(cls, module: ModuleID, role: RoleEnum, id: str, *args, **kwargs) -> None:
        """
        Delete an object.

        Args:
            module: The OCPI module
            role: The role of the caller
            id: The ID of the object to delete
            **kwargs: Additional parameters

        Raises:
            NotFoundOCPIError: If the object is not found
        """
        logger.info(f"Deleting {module.value} with id: {id}")

        storage_key = cls._get_storage_key(module)

        if id not in cls._storage[storage_key]:
            logger.warning(f"Object not found for deletion: {module.value} with id {id}")
            raise NotFoundOCPIError

        del cls._storage[storage_key][id]

        logger.debug(f"Deleted {module.value} with id: {id}")

    @classmethod
    async def do(
        cls,
        module: ModuleID,
        role: Optional[RoleEnum],
        action: Action,
        *args,
        data: Optional[dict] = None,
        **kwargs,
    ) -> Any:
        """
        Perform non-CRUD actions.

        Args:
            module: The OCPI module
            role: The role of the caller
            action: The action to perform
            data: Optional data for the action
            **kwargs: Additional parameters

        Returns:
            Action result
        """
        logger.info(f"Performing action {action.value} on {module.value}")

        # Handle different actions
        if action == Action.get_client_token:
            # Return a mock client token
            return "mock_client_token_" + str(uuid.uuid4())[:8]

        elif action == Action.authorize_token:
            # Mock token authorization - always allow for development
            logger.debug("Authorizing token (mock implementation)")
            return {
                "allowed": "ALLOWED",
                "authorization_info": {
                    "allowed": "ALLOWED",
                    "token": kwargs.get("token", "unknown"),
                    "location": kwargs.get("location"),
                },
            }

        elif action == Action.send_command:
            # Mock command sending
            command_id = str(uuid.uuid4())
            logger.debug(f"Sending command with id: {command_id}")
            return {
                "result": "ACCEPTED",
                "timeout": 30,
                "message": "Command accepted for processing",
            }

        elif action in [
            Action.send_get_chargingprofile,
            Action.send_delete_chargingprofile,
            Action.send_update_charging_profile,
        ]:
            # Mock charging profile actions
            logger.debug(f"Performing charging profile action: {action.value}")
            return {
                "result": "ACCEPTED",
                "timeout": 30,
                "message": f"Charging profile {action.value} accepted",
            }

        else:
            logger.warning(f"Unknown action: {action.value}")
            return {"result": "UNKNOWN_ACTION"}

    @classmethod
    def _get_storage_key(cls, module: ModuleID) -> str:
        """
        Get the storage key for a given module.

        Args:
            module: The OCPI module

        Returns:
            Storage key string
        """
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

        return module_mapping.get(module, module.value)

    @classmethod
    def get_mock_data_summary(cls) -> Dict[str, int]:
        """
        Get a summary of mock data for debugging.

        Returns:
            Dictionary with counts of objects in each module
        """
        return {key: len(value) for key, value in cls._storage.items()}
