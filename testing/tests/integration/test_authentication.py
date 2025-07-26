"""
Authentication Integration Tests
===============================

Tests for OCPI authentication flows between EMSP and CPO systems,
including token exchange, credentials registration, and authorization.
"""

import pytest


@pytest.mark.integration
@pytest.mark.asyncio
class TestOCPIAuthentication:
    """Test OCPI authentication flows."""

    async def test_emsp_token_validation(self, async_emsp_client, emsp_auth_headers):
        """Test EMSP token validation."""
        response = await async_emsp_client.get("/ocpi/emsp/2.2.1/versions", headers=emsp_auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert len(data["data"]) > 0

    async def test_cpo_token_validation(self, async_mock_cpo_client, cpo_auth_headers):
        """Test CPO token validation."""
        response = await async_mock_cpo_client.get("/ocpi/cpo/2.2.1/versions", headers=cpo_auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert len(data["data"]) > 0

    async def test_invalid_token_rejection(self, async_emsp_client):
        """Test that invalid tokens are rejected."""
        invalid_headers = {"Authorization": "Token invalid_token_123", "Content-Type": "application/json"}

        response = await async_emsp_client.get("/ocpi/emsp/2.2.1/versions", headers=invalid_headers)
        assert response.status_code == 401

    async def test_missing_token_rejection(self, async_emsp_client):
        """Test that requests without tokens are rejected."""
        headers = {"Content-Type": "application/json"}

        response = await async_emsp_client.get("/ocpi/emsp/2.2.1/versions", headers=headers)
        assert response.status_code == 401

    async def test_credentials_exchange_flow(
        self, async_emsp_client, async_mock_cpo_client, emsp_auth_headers, cpo_auth_headers
    ):
        """Test the complete credentials exchange flow between EMSP and CPO."""
        # Step 1: EMSP gets credentials from CPO
        cpo_credentials_response = await async_mock_cpo_client.get(
            "/ocpi/cpo/2.2.1/credentials", headers=cpo_auth_headers
        )
        assert cpo_credentials_response.status_code == 200
        cpo_credentials = cpo_credentials_response.json()["data"]

        # Step 2: CPO gets credentials from EMSP
        emsp_credentials_response = await async_emsp_client.get(
            "/ocpi/emsp/2.2.1/credentials", headers=emsp_auth_headers
        )
        assert emsp_credentials_response.status_code == 200
        emsp_credentials = emsp_credentials_response.json()["data"]

        # Verify credentials structure
        assert "token" in cpo_credentials
        assert "url" in cpo_credentials
        assert "business_details" in cpo_credentials
        assert "party_id" in cpo_credentials
        assert "country_code" in cpo_credentials

        assert "token" in emsp_credentials
        assert "url" in emsp_credentials
        assert "business_details" in emsp_credentials
        assert "party_id" in emsp_credentials
        assert "country_code" in emsp_credentials

    async def test_version_information_exchange(
        self, async_emsp_client, async_mock_cpo_client, emsp_auth_headers, cpo_auth_headers
    ):
        """Test version information exchange between EMSP and CPO."""
        # Test EMSP version endpoint
        emsp_versions_response = await async_emsp_client.get("/ocpi/emsp/2.2.1/versions", headers=emsp_auth_headers)
        assert emsp_versions_response.status_code == 200
        emsp_versions = emsp_versions_response.json()["data"]

        # Test CPO version endpoint
        cpo_versions_response = await async_mock_cpo_client.get("/ocpi/cpo/2.2.1/versions", headers=cpo_auth_headers)
        assert cpo_versions_response.status_code == 200
        cpo_versions = cpo_versions_response.json()["data"]

        # Verify version information structure
        assert isinstance(emsp_versions, list)
        assert len(emsp_versions) > 0
        assert "version" in emsp_versions[0]
        assert "url" in emsp_versions[0]

        assert isinstance(cpo_versions, list)
        assert len(cpo_versions) > 0
        assert "version" in cpo_versions[0]
        assert "url" in cpo_versions[0]

    async def test_version_details_exchange(
        self, async_emsp_client, async_mock_cpo_client, emsp_auth_headers, cpo_auth_headers
    ):
        """Test version details exchange between EMSP and CPO."""
        # Test EMSP version details
        emsp_details_response = await async_emsp_client.get(
            "/ocpi/emsp/2.2.1/versions/2.2.1", headers=emsp_auth_headers
        )
        assert emsp_details_response.status_code == 200
        emsp_details = emsp_details_response.json()["data"]

        # Test CPO version details
        cpo_details_response = await async_mock_cpo_client.get(
            "/ocpi/cpo/2.2.1/versions/2.2.1", headers=cpo_auth_headers
        )
        assert cpo_details_response.status_code == 200
        cpo_details = cpo_details_response.json()["data"]

        # Verify version details structure
        assert "version" in emsp_details
        assert "endpoints" in emsp_details
        assert isinstance(emsp_details["endpoints"], list)

        assert "version" in cpo_details
        assert "endpoints" in cpo_details
        assert isinstance(cpo_details["endpoints"], list)

        # Verify that both systems support required modules
        emsp_modules = [ep["identifier"] for ep in emsp_details["endpoints"]]
        cpo_modules = [ep["identifier"] for ep in cpo_details["endpoints"]]

        # EMSP should support these modules
        expected_emsp_modules = ["locations", "sessions", "cdrs", "tariffs", "commands", "tokens"]
        for module in expected_emsp_modules:
            assert module in emsp_modules, f"EMSP missing required module: {module}"

        # CPO should support these modules
        expected_cpo_modules = ["locations", "sessions", "cdrs", "tariffs", "commands", "tokens"]
        for module in expected_cpo_modules:
            assert module in cpo_modules, f"CPO missing required module: {module}"

    @pytest.mark.slow
    async def test_authentication_performance(self, async_emsp_client, emsp_auth_headers):
        """Test authentication performance under load."""
        import asyncio
        import time

        async def make_auth_request():
            response = await async_emsp_client.get("/ocpi/emsp/2.2.1/versions", headers=emsp_auth_headers)
            return response.status_code == 200

        # Test concurrent authentication requests
        start_time = time.time()
        tasks = [make_auth_request() for _ in range(10)]
        results = await asyncio.gather(*tasks)
        end_time = time.time()

        # All requests should succeed
        assert all(results), "Some authentication requests failed"

        # Should complete within reasonable time (adjust threshold as needed)
        duration = end_time - start_time
        assert duration < 5.0, f"Authentication took too long: {duration}s"
