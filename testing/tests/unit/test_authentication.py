"""
Unit Tests for Authentication Module
====================================

Tests for the EMSP authentication implementation, including token validation,
authentication flows, and security features.
"""

from unittest.mock import patch

import pytest
from auth import ClientAuthenticator


@pytest.mark.unit
@pytest.mark.asyncio
class TestClientAuthenticator:
    """Test ClientAuthenticator class."""

    async def test_get_valid_token_a(self):
        """Test getting valid Token A list."""
        tokens = await ClientAuthenticator.get_valid_token_a()

        assert isinstance(tokens, list)
        assert len(tokens) > 0
        assert "emsp_token_a_12345" in tokens
        assert "emsp_token_a_67890" in tokens
        assert "emsp_development_token_a" in tokens

    async def test_get_valid_token_c(self):
        """Test getting valid Token C list."""
        tokens = await ClientAuthenticator.get_valid_token_c()

        assert isinstance(tokens, list)
        assert len(tokens) > 0
        assert "cpo_token_c_abcdef" in tokens
        assert "cpo_token_c_ghijkl" in tokens
        assert "cpo_development_token_c" in tokens
        assert "test_token_c_123" in tokens

    async def test_is_token_valid_with_valid_token_a(self):
        """Test token validation with valid Token A."""
        valid_token = "emsp_token_a_12345"
        is_valid = await ClientAuthenticator.is_token_valid(valid_token)

        assert is_valid is True

    async def test_is_token_valid_with_valid_token_c(self):
        """Test token validation with valid Token C."""
        valid_token = "cpo_token_c_abcdef"
        is_valid = await ClientAuthenticator.is_token_valid(valid_token)

        assert is_valid is True

    async def test_is_token_valid_with_invalid_token(self):
        """Test token validation with invalid token."""
        invalid_token = "invalid_token_xyz"
        is_valid = await ClientAuthenticator.is_token_valid(invalid_token)

        assert is_valid is False

    async def test_is_token_valid_with_empty_token(self):
        """Test token validation with empty token."""
        empty_token = ""
        is_valid = await ClientAuthenticator.is_token_valid(empty_token)

        assert is_valid is False

    async def test_is_token_valid_with_none_token(self):
        """Test token validation with None token."""
        none_token = None
        is_valid = await ClientAuthenticator.is_token_valid(none_token)

        assert is_valid is False

    async def test_get_token_info_with_token_a(self):
        """Test getting token info for Token A."""
        token = "emsp_token_a_12345"
        token_info = await ClientAuthenticator.get_token_info(token)

        assert isinstance(token_info, dict)
        assert token_info["type"] == "TOKEN_A"
        assert token_info["valid"] is True
        assert "EMSP authentication token" in token_info["description"]

    async def test_get_token_info_with_token_c(self):
        """Test getting token info for Token C."""
        token = "cpo_token_c_abcdef"
        token_info = await ClientAuthenticator.get_token_info(token)

        assert isinstance(token_info, dict)
        assert token_info["type"] == "TOKEN_C"
        assert token_info["valid"] is True
        assert "CPO authentication token" in token_info["description"]

    async def test_get_token_info_with_invalid_token(self):
        """Test getting token info for invalid token."""
        token = "invalid_token_xyz"
        token_info = await ClientAuthenticator.get_token_info(token)

        assert isinstance(token_info, dict)
        assert token_info["type"] == "UNKNOWN"
        assert token_info["valid"] is False
        assert "Invalid or unknown token" in token_info["description"]

    async def test_add_token_a(self):
        """Test adding a new Token A."""
        new_token = "new_emsp_token_a_test"

        # Add the token
        await ClientAuthenticator.add_token_a(new_token)

        # Verify it was added
        tokens = await ClientAuthenticator.get_valid_token_a()
        assert new_token in tokens

        # Verify it's valid
        is_valid = await ClientAuthenticator.is_token_valid(new_token)
        assert is_valid is True

    async def test_add_token_c(self):
        """Test adding a new Token C."""
        new_token = "new_cpo_token_c_test"

        # Add the token
        await ClientAuthenticator.add_token_c(new_token)

        # Verify it was added
        tokens = await ClientAuthenticator.get_valid_token_c()
        assert new_token in tokens

        # Verify it's valid
        is_valid = await ClientAuthenticator.is_token_valid(new_token)
        assert is_valid is True

    async def test_remove_token_a(self):
        """Test removing a Token A."""
        token_to_remove = "emsp_token_a_67890"

        # Verify token exists initially
        tokens_before = await ClientAuthenticator.get_valid_token_a()
        assert token_to_remove in tokens_before

        # Remove the token
        await ClientAuthenticator.remove_token_a(token_to_remove)

        # Verify it was removed
        tokens_after = await ClientAuthenticator.get_valid_token_a()
        assert token_to_remove not in tokens_after

        # Verify it's no longer valid
        is_valid = await ClientAuthenticator.is_token_valid(token_to_remove)
        assert is_valid is False

    async def test_remove_token_c(self):
        """Test removing a Token C."""
        token_to_remove = "cpo_token_c_ghijkl"

        # Verify token exists initially
        tokens_before = await ClientAuthenticator.get_valid_token_c()
        assert token_to_remove in tokens_before

        # Remove the token
        await ClientAuthenticator.remove_token_c(token_to_remove)

        # Verify it was removed
        tokens_after = await ClientAuthenticator.get_valid_token_c()
        assert token_to_remove not in tokens_after

        # Verify it's no longer valid
        is_valid = await ClientAuthenticator.is_token_valid(token_to_remove)
        assert is_valid is False

    async def test_token_validation_case_sensitivity(self):
        """Test that token validation is case sensitive."""
        original_token = "emsp_token_a_12345"
        uppercase_token = original_token.upper()
        lowercase_token = original_token.lower()

        # Original should be valid
        assert await ClientAuthenticator.is_token_valid(original_token) is True

        # Case variations should be invalid (assuming original is not all caps/lowercase)
        if original_token != uppercase_token:
            assert await ClientAuthenticator.is_token_valid(uppercase_token) is False
        if original_token != lowercase_token:
            assert await ClientAuthenticator.is_token_valid(lowercase_token) is False

    async def test_token_validation_with_whitespace(self):
        """Test token validation with whitespace."""
        valid_token = "emsp_token_a_12345"
        token_with_spaces = f" {valid_token} "
        token_with_newlines = f"\n{valid_token}\n"

        # Tokens with whitespace should be invalid
        assert await ClientAuthenticator.is_token_valid(token_with_spaces) is False
        assert await ClientAuthenticator.is_token_valid(token_with_newlines) is False

    @patch("auth.logger")
    async def test_logging_on_successful_validation(self, mock_logger):
        """Test that successful token validation is logged."""
        valid_token = "emsp_token_a_12345"

        await ClientAuthenticator.is_token_valid(valid_token)

        # Should log debug message for successful validation
        # Note: There may be multiple debug calls (for token retrieval and validation)
        debug_calls = [call for call in mock_logger.debug.call_args_list]
        assert len(debug_calls) >= 1

        # Check that at least one call contains the validation success message
        validation_calls = [call for call in debug_calls if "Token validation successful" in str(call)]
        assert len(validation_calls) >= 1

    @patch("auth.logger")
    async def test_logging_on_failed_validation(self, mock_logger):
        """Test that failed token validation is logged."""
        invalid_token = "invalid_token_xyz"

        await ClientAuthenticator.is_token_valid(invalid_token)

        # Should log warning message for failed validation
        mock_logger.warning.assert_called_once()
        call_args = mock_logger.warning.call_args[0][0]
        assert "Token validation failed" in call_args
