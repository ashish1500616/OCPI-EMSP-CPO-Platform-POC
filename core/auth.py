"""
EMSP Authentication Implementation
=================================

This module implements OCPI-compliant authentication for the EMSP backend.
It extends the py_ocpi.core.authentication.authenticator.Authenticator base class
and provides token-based authentication following OCPI standards.

The implementation includes:
- Token A and Token C management
- OCPI-compliant authentication flow
- Mock token storage for development
- Proper error handling and logging
"""

import logging
from typing import List

from py_ocpi.core.authentication.authenticator import Authenticator

logger = logging.getLogger(__name__)
"""
Logger for the authentication module.
Configured to provide detailed insights into token management and validation.
"""


class ClientAuthenticator(Authenticator):
    """
    EMSP Client Authenticator implementing OCPI token-based authentication.

    This class manages authentication tokens according to OCPI specifications:
    - Token A: Used by the EMSP to authenticate with CPO systems
    - Token C: Used by CPO systems to authenticate with the EMSP

    In production, replace the mock token storage with a secure database
    or token management system.
    """

    # NOTE: This is mock token storage for educational and development purposes.
    # In a production environment, replace this with a secure, persistent storage
    # solution (e.g., a database, a dedicated token management service).
    _valid_tokens_a: List[str] = [
        "emsp_token_a_12345",
        "emsp_token_a_67890",
        "emsp_development_token_a",  # For local development and testing
    ]

    _valid_tokens_c: List[str] = [
        "cpo_token_c_abcdef",
        "cpo_token_c_ghijkl",
        "cpo_development_token_c",  # For local development and testing
        "test_token_c_123",         # Used specifically in integration tests
    ]

    @classmethod
    async def get_valid_token_a(cls) -> List[str]:
        """
        Return valid Token A list.

        Token A is used by the EMSP to authenticate with CPO systems.
        These tokens are generated and managed by the EMSP.

        Returns:
            List of valid Token A strings
        """
        logger.debug(f"Auth: Returning {len(cls._valid_tokens_a)} valid Token A entries.")
        return cls._valid_tokens_a.copy()

    @classmethod
    async def get_valid_token_c(cls) -> List[str]:
        """
        Return valid Token C list.

        Token C is used by CPO systems to authenticate with the EMSP.
        These tokens are provided by CPO systems during registration.

        Returns:
            List of valid Token C strings
        """
        logger.debug(f"Auth: Returning {len(cls._valid_tokens_c)} valid Token C entries.")
        return cls._valid_tokens_c.copy()

    @classmethod
    async def add_token_a(cls, token: str) -> None:
        """
        Add a new Token A to the valid tokens list.

        Args:
            token: The Token A to add
        """
        if token not in cls._valid_tokens_a:
            cls._valid_tokens_a.append(token)
            logger.info(f"Auth: Added new Token A: {token[:8]}...")
        else:
            logger.warning(f"Auth: Token A already exists, not adding: {token[:8]}...")

    @classmethod
    async def add_token_c(cls, token: str) -> None:
        """
        Add a new Token C to the valid tokens list.

        Args:
            token: The Token C to add
        """
        if token not in cls._valid_tokens_c:
            cls._valid_tokens_c.append(token)
            logger.info(f"Auth: Added new Token C: {token[:8]}...")
        else:
            logger.warning(f"Auth: Token C already exists, not adding: {token[:8]}...")

    @classmethod
    async def remove_token_a(cls, token: str) -> bool:
        """
        Remove a Token A from the valid tokens list.

        Args:
            token: The Token A to remove

        Returns:
            True if token was removed, False if not found
        """
        if token in cls._valid_tokens_a:
            cls._valid_tokens_a.remove(token)
            logger.info(f"Auth: Removed Token A: {token[:8]}... .")
            return True
        else:
            logger.warning(f"Auth: Token A not found for removal: {token[:8]}... .")
            return False

    @classmethod
    async def remove_token_c(cls, token: str) -> bool:
        """
        Remove a Token C from the valid tokens list.

        Args:
            token: The Token C to remove

        Returns:
            True if token was removed, False if not found
        """
        if token in cls._valid_tokens_c:
            cls._valid_tokens_c.remove(token)
            logger.info(f"Auth: Removed Token C: {token[:8]}... .")
            return True
        else:
            logger.warning(f"Auth: Token C not found for removal: {token[:8]}... .")
            return False

    @classmethod
    async def is_token_valid(cls, token: str) -> bool:
        """
        Check if a token is valid (either Token A or Token C).

        Args:
            token: The token to validate

        Returns:
            True if token is valid, False otherwise
        """
        if token is None:
            logger.warning("Auth: Token validation failed: None token provided.")
            return False

        tokens_a = await cls.get_valid_token_a()
        tokens_c = await cls.get_valid_token_c()

        is_valid = token in tokens_a or token in tokens_c

        if is_valid:
            logger.debug(f"Auth: Token validation successful for: {token[:8]}... .")
        else:
            logger.warning(
                f"Auth: Token validation failed for: {token[:8] if token else 'None'}... . Invalid or unknown token."
            )

        return is_valid

    @classmethod
    async def get_token_info(cls, token: str) -> dict:
        """
        Get information about a token.

        Args:
            token: The token to get information about

        Returns:
            Dictionary with token information
        """
        tokens_a = await cls.get_valid_token_a()
        tokens_c = await cls.get_valid_token_c()

        if token in tokens_a:
            return {
                "type": "TOKEN_A",
                "valid": True,
                "description": "EMSP authentication token for CPO systems",
            }
        elif token in tokens_c:
            return {
                "type": "TOKEN_C",
                "valid": True,
                "description": "CPO authentication token for EMSP system",
            }
        else:
            return {
                "type": "UNKNOWN",
                "valid": False,
                "description": "Invalid or unknown token",
            }

    @classmethod
    def get_token_summary(cls) -> dict:
        """
        Get a summary of all tokens for debugging.

        Returns:
            Dictionary with token counts and sample tokens
        """
        return {
            "tokens_a": {
                "count": len(cls._valid_tokens_a),
                "samples": [f"{token[:8]}..." for token in cls._valid_tokens_a[:3]],
            },
            "tokens_c": {
                "count": len(cls._valid_tokens_c),
                "samples": [f"{token[:8]}..." for token in cls._valid_tokens_c[:3]],
            },
        }
