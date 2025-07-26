"""
Data Synchronization Integration Tests
======================================

Tests for data synchronization between EMSP and CPO systems, including
location discovery, session reporting, CDR submission, and tariff distribution.
"""

import pytest


@pytest.mark.integration
@pytest.mark.asyncio
class TestDataSynchronization:
    """Test data synchronization between EMSP and CPO."""

    async def test_location_discovery_flow(
        self, async_emsp_client, async_mock_cpo_client, emsp_auth_headers, cpo_auth_headers, test_data_factory
    ):
        """Test complete location discovery flow from CPO to EMSP."""
        # Step 1: CPO creates a new location
        new_location = test_data_factory.create_location(id="TEST_LOC_001", name="Test Charging Hub", party_id="CPO")

        # CPO stores the location (simulated)
        cpo_location_response = await async_mock_cpo_client.put(
            "/ocpi/cpo/2.2.1/locations/US/CPO/TEST_LOC_001", headers=cpo_auth_headers, json=new_location
        )
        assert cpo_location_response.status_code in [200, 201]

        # Step 2: EMSP discovers the location
        emsp_location_response = await async_emsp_client.get("/ocpi/emsp/2.2.1/locations", headers=emsp_auth_headers)
        assert emsp_location_response.status_code == 200

        locations_data = emsp_location_response.json()["data"]
        assert isinstance(locations_data, list)

        # Verify location structure
        if locations_data:
            location = locations_data[0]
            assert "id" in location
            assert "name" in location
            assert "address" in location
            assert "coordinates" in location
            assert "evses" in location
            assert isinstance(location["evses"], list)

    async def test_session_reporting_flow(
        self, async_emsp_client, async_mock_cpo_client, emsp_auth_headers, cpo_auth_headers, test_data_factory
    ):
        """Test session reporting from CPO to EMSP."""
        # Step 1: CPO creates a charging session
        new_session = test_data_factory.create_session(
            id="TEST_SES_001", party_id="CPO", location_id="LOC001", status="ACTIVE"
        )

        # CPO reports the session
        cpo_session_response = await async_mock_cpo_client.put(
            "/ocpi/cpo/2.2.1/sessions/US/CPO/TEST_SES_001", headers=cpo_auth_headers, json=new_session
        )
        assert cpo_session_response.status_code in [200, 201]

        # Step 2: EMSP retrieves session information
        emsp_sessions_response = await async_emsp_client.get("/ocpi/emsp/2.2.1/sessions", headers=emsp_auth_headers)
        assert emsp_sessions_response.status_code == 200

        sessions_data = emsp_sessions_response.json()["data"]
        assert isinstance(sessions_data, list)

        # Verify session structure
        if sessions_data:
            session = sessions_data[0]
            assert "id" in session
            assert "start_date_time" in session
            assert "kwh" in session
            assert "cdr_token" in session
            assert "location_id" in session
            assert "status" in session

    async def test_cdr_submission_flow(
        self, async_emsp_client, async_mock_cpo_client, emsp_auth_headers, cpo_auth_headers, test_data_factory
    ):
        """Test CDR submission from CPO to EMSP."""
        # Step 1: CPO creates a CDR for completed session
        new_cdr = test_data_factory.create_cdr(id="TEST_CDR_001", party_id="CPO", session_id="SES001")

        # CPO submits the CDR
        cpo_cdr_response = await async_mock_cpo_client.post(
            "/ocpi/cpo/2.2.1/cdrs", headers=cpo_auth_headers, json=new_cdr
        )
        assert cpo_cdr_response.status_code in [200, 201]

        # Step 2: EMSP retrieves CDR information
        emsp_cdrs_response = await async_emsp_client.get("/ocpi/emsp/2.2.1/cdrs", headers=emsp_auth_headers)
        assert emsp_cdrs_response.status_code == 200

        cdrs_data = emsp_cdrs_response.json()["data"]
        assert isinstance(cdrs_data, list)

        # Verify CDR structure
        if cdrs_data:
            cdr = cdrs_data[0]
            assert "id" in cdr
            assert "start_date_time" in cdr
            assert "end_date_time" in cdr
            assert "session_id" in cdr
            assert "cdr_token" in cdr
            assert "total_cost" in cdr
            assert "total_energy" in cdr

    async def test_tariff_distribution_flow(
        self, async_emsp_client, async_mock_cpo_client, emsp_auth_headers, cpo_auth_headers, test_data_factory
    ):
        """Test tariff distribution from CPO to EMSP."""
        # Step 1: CPO creates a tariff
        new_tariff = test_data_factory.create_tariff(id="TEST_TRF_001", party_id="CPO", currency="USD")

        # CPO publishes the tariff
        cpo_tariff_response = await async_mock_cpo_client.put(
            "/ocpi/cpo/2.2.1/tariffs/US/CPO/TEST_TRF_001", headers=cpo_auth_headers, json=new_tariff
        )
        assert cpo_tariff_response.status_code in [200, 201]

        # Step 2: EMSP retrieves tariff information
        emsp_tariffs_response = await async_emsp_client.get("/ocpi/emsp/2.2.1/tariffs", headers=emsp_auth_headers)
        assert emsp_tariffs_response.status_code == 200

        tariffs_data = emsp_tariffs_response.json()["data"]
        assert isinstance(tariffs_data, list)

        # Verify tariff structure
        if tariffs_data:
            tariff = tariffs_data[0]
            assert "id" in tariff
            assert "currency" in tariff
            assert "elements" in tariff
            assert isinstance(tariff["elements"], list)

            if tariff["elements"]:
                element = tariff["elements"][0]
                assert "price_components" in element
                assert isinstance(element["price_components"], list)

    async def test_token_authorization_flow(
        self, async_emsp_client, async_mock_cpo_client, emsp_auth_headers, cpo_auth_headers, test_data_factory
    ):
        """Test token authorization flow between EMSP and CPO."""
        # Step 1: EMSP provides token information to CPO
        test_token = test_data_factory.create_token(uid="TEST_TOKEN_001", party_id="EMS", contract_id="CONTRACT_001")

        # EMSP sends token to CPO
        emsp_token_response = await async_emsp_client.put(
            "/ocpi/emsp/2.2.1/tokens/US/EMS/TEST_TOKEN_001", headers=emsp_auth_headers, json=test_token
        )
        assert emsp_token_response.status_code in [200, 201]

        # Step 2: CPO requests token authorization
        auth_request = {
            "token": {
                "country_code": "US",
                "party_id": "EMS",
                "uid": "TEST_TOKEN_001",
                "type": "RFID",
                "contract_id": "CONTRACT_001",
            },
            "location_id": "LOC001",
            "evse_uid": "EVSE001",
            "connector_id": "1",
        }

        cpo_auth_response = await async_mock_cpo_client.post(
            "/ocpi/cpo/2.2.1/tokens/US/EMS/TEST_TOKEN_001/authorize", headers=cpo_auth_headers, json=auth_request
        )
        assert cpo_auth_response.status_code == 200

        auth_result = cpo_auth_response.json()["data"]
        assert "allowed" in auth_result
        assert isinstance(auth_result["allowed"], bool)

    async def test_data_pagination(self, async_emsp_client, emsp_auth_headers):
        """Test data pagination for large datasets."""
        # Test locations pagination
        response = await async_emsp_client.get("/ocpi/emsp/2.2.1/locations?limit=2", headers=emsp_auth_headers)
        assert response.status_code == 200

        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)

        # Check pagination headers if present
        if "Link" in response.headers:
            link_header = response.headers["Link"]
            assert "next" in link_header or "prev" in link_header

    async def test_data_filtering(self, async_emsp_client, emsp_auth_headers):
        """Test data filtering capabilities."""
        # Test date filtering for sessions
        date_from = "2023-01-01T00:00:00Z"
        date_to = "2023-12-31T23:59:59Z"

        response = await async_emsp_client.get(
            f"/ocpi/emsp/2.2.1/sessions?date_from={date_from}&date_to={date_to}", headers=emsp_auth_headers
        )
        assert response.status_code == 200

        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)

    @pytest.mark.slow
    async def test_large_dataset_synchronization(
        self, async_emsp_client, async_mock_cpo_client, emsp_auth_headers, cpo_auth_headers, test_data_factory
    ):
        """Test synchronization performance with large datasets."""
        import asyncio
        import time

        # Create multiple locations concurrently
        async def create_location(i):
            location = test_data_factory.create_location(
                id=f"PERF_LOC_{i:03d}", name=f"Performance Test Location {i}", party_id="CPO"
            )
            response = await async_mock_cpo_client.put(
                f"/ocpi/cpo/2.2.1/locations/US/CPO/PERF_LOC_{i:03d}", headers=cpo_auth_headers, json=location
            )
            return response.status_code in [200, 201]

        # Create 10 locations concurrently
        start_time = time.time()
        tasks = [create_location(i) for i in range(10)]
        results = await asyncio.gather(*tasks)
        end_time = time.time()

        # All creations should succeed
        assert all(results), "Some location creations failed"

        # Should complete within reasonable time
        duration = end_time - start_time
        assert duration < 10.0, f"Large dataset sync took too long: {duration}s"
