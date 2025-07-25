"""
OCPI 2.2.1 Specification Compliance Tests
=========================================

Tests that validate strict adherence to OCPI 2.2.1 specification requirements,
including message formats, required fields, data types, and protocol behavior.
"""

import pytest
import httpx
from datetime import datetime
import re


@pytest.mark.compliance
@pytest.mark.asyncio
class TestOCPICompliance:
    """Test OCPI 2.2.1 specification compliance."""
    
    async def test_response_format_compliance(self, async_emsp_client, emsp_auth_headers):
        """Test that all responses follow OCPI response format."""
        endpoints = [
            "/ocpi/emsp/2.2.1/versions",
            "/ocpi/emsp/2.2.1/versions/2.2.1",
            "/ocpi/emsp/2.2.1/locations",
            "/ocpi/emsp/2.2.1/sessions",
            "/ocpi/emsp/2.2.1/cdrs",
            "/ocpi/emsp/2.2.1/tariffs"
        ]
        
        for endpoint in endpoints:
            response = await async_emsp_client.get(endpoint, headers=emsp_auth_headers)
            
            # Should return 200 for successful requests
            assert response.status_code == 200, f"Endpoint {endpoint} returned {response.status_code}"
            
            data = response.json()
            
            # OCPI response format compliance
            assert "data" in data, f"Response missing 'data' field for {endpoint}"
            assert "status_code" in data, f"Response missing 'status_code' field for {endpoint}"
            assert "status_message" in data, f"Response missing 'status_message' field for {endpoint}"
            assert "timestamp" in data, f"Response missing 'timestamp' field for {endpoint}"
            
            # Status code should be 1000 for success
            assert data["status_code"] == 1000, f"Invalid status_code for {endpoint}: {data['status_code']}"
            
            # Timestamp should be valid ISO format
            timestamp = data["timestamp"]
            assert self._is_valid_iso_timestamp(timestamp), f"Invalid timestamp format for {endpoint}: {timestamp}"
    
    async def test_version_information_compliance(self, async_emsp_client, emsp_auth_headers):
        """Test version information endpoint compliance."""
        response = await async_emsp_client.get(
            "/ocpi/emsp/2.2.1/versions",
            headers=emsp_auth_headers
        )
        assert response.status_code == 200
        
        data = response.json()["data"]
        assert isinstance(data, list), "Versions data should be a list"
        assert len(data) > 0, "Should have at least one version"
        
        for version in data:
            # Required fields for version information
            assert "version" in version, "Version missing 'version' field"
            assert "url" in version, "Version missing 'url' field"
            
            # Version should be valid format (e.g., "2.2.1")
            version_pattern = r'^\d+\.\d+(\.\d+)?$'
            assert re.match(version_pattern, version["version"]), f"Invalid version format: {version['version']}"
            
            # URL should be valid HTTP(S) URL
            url_pattern = r'^https?://.+'
            assert re.match(url_pattern, version["url"]), f"Invalid URL format: {version['url']}"
    
    async def test_version_details_compliance(self, async_emsp_client, emsp_auth_headers):
        """Test version details endpoint compliance."""
        response = await async_emsp_client.get(
            "/ocpi/emsp/2.2.1/versions/2.2.1",
            headers=emsp_auth_headers
        )
        assert response.status_code == 200
        
        data = response.json()["data"]
        
        # Required fields for version details
        assert "version" in data, "Version details missing 'version' field"
        assert "endpoints" in data, "Version details missing 'endpoints' field"
        
        assert data["version"] == "2.2.1", f"Expected version 2.2.1, got {data['version']}"
        assert isinstance(data["endpoints"], list), "Endpoints should be a list"
        
        # Validate endpoint information
        for endpoint in data["endpoints"]:
            assert "identifier" in endpoint, "Endpoint missing 'identifier' field"
            assert "role" in endpoint, "Endpoint missing 'role' field"
            assert "url" in endpoint, "Endpoint missing 'url' field"
            
            # Role should be valid OCPI role
            valid_roles = ["SENDER", "RECEIVER"]
            assert endpoint["role"] in valid_roles, f"Invalid role: {endpoint['role']}"
            
            # URL should be valid
            url_pattern = r'^https?://.+'
            assert re.match(url_pattern, endpoint["url"]), f"Invalid endpoint URL: {endpoint['url']}"
    
    async def test_location_object_compliance(self, async_emsp_client, emsp_auth_headers):
        """Test Location object compliance with OCPI specification."""
        response = await async_emsp_client.get(
            "/ocpi/emsp/2.2.1/locations",
            headers=emsp_auth_headers
        )
        assert response.status_code == 200
        
        locations = response.json()["data"]
        if not locations:
            pytest.skip("No locations available for compliance testing")
        
        for location in locations:
            # Required fields for Location
            required_fields = [
                "country_code", "party_id", "id", "publish", "name", 
                "address", "city", "postal_code", "country", "coordinates", 
                "evses", "last_updated"
            ]
            
            for field in required_fields:
                assert field in location, f"Location missing required field: {field}"
            
            # Validate field formats
            assert len(location["country_code"]) == 2, "Country code should be 2 characters"
            assert len(location["party_id"]) == 3, "Party ID should be 3 characters"
            assert isinstance(location["publish"], bool), "Publish should be boolean"
            assert isinstance(location["evses"], list), "EVSEs should be a list"
            
            # Validate coordinates
            coords = location["coordinates"]
            assert "latitude" in coords, "Coordinates missing latitude"
            assert "longitude" in coords, "Coordinates missing longitude"
            
            # Validate timestamp format
            assert self._is_valid_iso_timestamp(location["last_updated"]), \
                f"Invalid last_updated timestamp: {location['last_updated']}"
    
    async def test_session_object_compliance(self, async_emsp_client, emsp_auth_headers):
        """Test Session object compliance with OCPI specification."""
        response = await async_emsp_client.get(
            "/ocpi/emsp/2.2.1/sessions",
            headers=emsp_auth_headers
        )
        assert response.status_code == 200
        
        sessions = response.json()["data"]
        if not sessions:
            pytest.skip("No sessions available for compliance testing")
        
        for session in sessions:
            # Required fields for Session
            required_fields = [
                "country_code", "party_id", "id", "start_date_time", "kwh",
                "cdr_token", "auth_method", "location_id", "evse_uid",
                "connector_id", "currency", "status", "last_updated"
            ]
            
            for field in required_fields:
                assert field in session, f"Session missing required field: {field}"
            
            # Validate field formats
            assert len(session["country_code"]) == 2, "Country code should be 2 characters"
            assert len(session["party_id"]) == 3, "Party ID should be 3 characters"
            assert isinstance(session["kwh"], (int, float)), "kWh should be numeric"
            assert len(session["currency"]) == 3, "Currency should be 3 characters"
            
            # Validate status
            valid_statuses = ["ACTIVE", "COMPLETED", "INVALID", "PENDING", "RESERVATION"]
            assert session["status"] in valid_statuses, f"Invalid session status: {session['status']}"
            
            # Validate timestamps
            assert self._is_valid_iso_timestamp(session["start_date_time"]), \
                f"Invalid start_date_time: {session['start_date_time']}"
            assert self._is_valid_iso_timestamp(session["last_updated"]), \
                f"Invalid last_updated: {session['last_updated']}"
    
    async def test_cdr_object_compliance(self, async_emsp_client, emsp_auth_headers):
        """Test CDR object compliance with OCPI specification."""
        response = await async_emsp_client.get(
            "/ocpi/emsp/2.2.1/cdrs",
            headers=emsp_auth_headers
        )
        assert response.status_code == 200
        
        cdrs = response.json()["data"]
        if not cdrs:
            pytest.skip("No CDRs available for compliance testing")
        
        for cdr in cdrs:
            # Required fields for CDR
            required_fields = [
                "country_code", "party_id", "id", "start_date_time", "end_date_time",
                "session_id", "cdr_token", "auth_method", "cdr_location", "currency",
                "charging_periods", "total_cost", "total_energy", "last_updated"
            ]
            
            for field in required_fields:
                assert field in cdr, f"CDR missing required field: {field}"
            
            # Validate field formats
            assert len(cdr["country_code"]) == 2, "Country code should be 2 characters"
            assert len(cdr["party_id"]) == 3, "Party ID should be 3 characters"
            assert len(cdr["currency"]) == 3, "Currency should be 3 characters"
            assert isinstance(cdr["charging_periods"], list), "Charging periods should be a list"
            assert isinstance(cdr["total_energy"], (int, float)), "Total energy should be numeric"
            
            # Validate timestamps
            assert self._is_valid_iso_timestamp(cdr["start_date_time"]), \
                f"Invalid start_date_time: {cdr['start_date_time']}"
            assert self._is_valid_iso_timestamp(cdr["end_date_time"]), \
                f"Invalid end_date_time: {cdr['end_date_time']}"
            assert self._is_valid_iso_timestamp(cdr["last_updated"]), \
                f"Invalid last_updated: {cdr['last_updated']}"
    
    async def test_error_response_compliance(self, async_emsp_client):
        """Test error response format compliance."""
        # Test with invalid authentication
        invalid_headers = {
            "Authorization": "Token invalid_token",
            "Content-Type": "application/json"
        }
        
        response = await async_emsp_client.get(
            "/ocpi/emsp/2.2.1/versions",
            headers=invalid_headers
        )
        
        assert response.status_code == 401
        
        # Error responses should still follow OCPI format
        data = response.json()
        assert "status_code" in data, "Error response missing status_code"
        assert "status_message" in data, "Error response missing status_message"
        assert "timestamp" in data, "Error response missing timestamp"
        
        # Status code should be appropriate error code
        assert data["status_code"] >= 2000, f"Error status_code should be >= 2000, got {data['status_code']}"
    
    async def test_pagination_compliance(self, async_emsp_client, emsp_auth_headers):
        """Test pagination compliance with OCPI specification."""
        # Test with limit parameter
        response = await async_emsp_client.get(
            "/ocpi/emsp/2.2.1/locations?limit=1",
            headers=emsp_auth_headers
        )
        assert response.status_code == 200
        
        data = response.json()["data"]
        
        # Should respect limit parameter
        assert len(data) <= 1, "Should respect limit parameter"
        
        # Check for pagination headers
        headers = response.headers
        if len(data) == 1:  # If there might be more data
            # Link header should be present for pagination
            # Note: This depends on implementation - some may use different pagination methods
            pass  # Implementation-specific pagination validation
    
    async def test_http_methods_compliance(self, async_emsp_client, emsp_auth_headers):
        """Test HTTP methods compliance for different endpoints."""
        # GET methods should work for list endpoints
        get_endpoints = [
            "/ocpi/emsp/2.2.1/locations",
            "/ocpi/emsp/2.2.1/sessions",
            "/ocpi/emsp/2.2.1/cdrs",
            "/ocpi/emsp/2.2.1/tariffs"
        ]
        
        for endpoint in get_endpoints:
            response = await async_emsp_client.get(endpoint, headers=emsp_auth_headers)
            assert response.status_code == 200, f"GET {endpoint} should return 200"
        
        # HEAD methods should work for the same endpoints
        for endpoint in get_endpoints:
            response = await async_emsp_client.head(endpoint, headers=emsp_auth_headers)
            assert response.status_code in [200, 405], f"HEAD {endpoint} should return 200 or 405"
    
    def _is_valid_iso_timestamp(self, timestamp_str: str) -> bool:
        """Validate ISO 8601 timestamp format."""
        try:
            # Try to parse the timestamp
            datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            return True
        except ValueError:
            return False
