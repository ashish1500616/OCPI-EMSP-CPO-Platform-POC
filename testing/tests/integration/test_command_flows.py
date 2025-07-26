"""
Command Flow Integration Tests
=============================

Tests for OCPI command execution flows between EMSP and CPO systems,
including start/stop session commands, reservation management, and
charging profile updates with proper response handling.
"""

import asyncio
from datetime import datetime

import pytest


@pytest.mark.integration
@pytest.mark.asyncio
class TestCommandFlows:
    """Test OCPI command execution flows."""

    async def test_start_session_command_flow(
        self, async_emsp_client, async_mock_cpo_client, emsp_auth_headers, cpo_auth_headers, test_data_factory
    ):
        """Test complete start session command flow."""
        # Step 1: EMSP sends START_SESSION command to CPO
        start_command = test_data_factory.create_command(
            command_type="START_SESSION",
            response_url="https://emsp.example.com/ocpi/emsp/2.2.1/commands/START_SESSION/123",
        )

        command_response = await async_emsp_client.post(
            "/ocpi/emsp/2.2.1/commands/START_SESSION", headers=emsp_auth_headers, json=start_command
        )
        assert command_response.status_code in [200, 201]

        command_result = command_response.json()["data"]
        assert "result" in command_result
        assert command_result["result"] in ["ACCEPTED", "REJECTED"]

        # Step 2: If accepted, verify command was processed
        if command_result["result"] == "ACCEPTED":
            # Wait a moment for command processing
            await asyncio.sleep(0.1)

            # Check that a session was created (simulated)
            sessions_response = await async_mock_cpo_client.get("/ocpi/cpo/2.2.1/sessions", headers=cpo_auth_headers)
            assert sessions_response.status_code == 200

    async def test_stop_session_command_flow(
        self, async_emsp_client, async_mock_cpo_client, emsp_auth_headers, cpo_auth_headers, test_data_factory
    ):
        """Test complete stop session command flow."""
        # Step 1: Create an active session first (simulated)

        # Step 2: EMSP sends STOP_SESSION command to CPO
        stop_command = test_data_factory.create_command(
            command_type="STOP_SESSION",
            response_url="https://emsp.example.com/ocpi/emsp/2.2.1/commands/STOP_SESSION/456",
        )
        stop_command["session_id"] = "ACTIVE_SES_001"

        command_response = await async_emsp_client.post(
            "/ocpi/emsp/2.2.1/commands/STOP_SESSION", headers=emsp_auth_headers, json=stop_command
        )
        assert command_response.status_code in [200, 201]

        command_result = command_response.json()["data"]
        assert "result" in command_result
        assert command_result["result"] in ["ACCEPTED", "REJECTED"]

        # Step 3: If accepted, verify session status changed
        if command_result["result"] == "ACCEPTED":
            await asyncio.sleep(0.1)

            # Session should be completed or completing
            session_response = await async_mock_cpo_client.get(
                "/ocpi/cpo/2.2.1/sessions/US/CPO/ACTIVE_SES_001", headers=cpo_auth_headers
            )
            if session_response.status_code == 200:
                session_data = session_response.json()["data"]
                assert session_data["status"] in ["COMPLETED", "INVALID"]

    async def test_reserve_now_command_flow(
        self, async_emsp_client, async_mock_cpo_client, emsp_auth_headers, cpo_auth_headers, test_data_factory
    ):
        """Test reservation command flow."""
        # Step 1: EMSP sends RESERVE_NOW command to CPO
        reserve_command = test_data_factory.create_command(
            command_type="RESERVE_NOW", response_url="https://emsp.example.com/ocpi/emsp/2.2.1/commands/RESERVE_NOW/789"
        )

        command_response = await async_emsp_client.post(
            "/ocpi/emsp/2.2.1/commands/RESERVE_NOW", headers=emsp_auth_headers, json=reserve_command
        )
        assert command_response.status_code in [200, 201]

        command_result = command_response.json()["data"]
        assert "result" in command_result
        assert command_result["result"] in ["ACCEPTED", "REJECTED"]

        # Step 2: If accepted, verify reservation was created
        if command_result["result"] == "ACCEPTED":
            await asyncio.sleep(0.1)

            # Check EVSE status (should be reserved)
            location_response = await async_mock_cpo_client.get("/ocpi/cpo/2.2.1/locations", headers=cpo_auth_headers)
            assert location_response.status_code == 200

    async def test_cancel_reservation_command_flow(
        self, async_emsp_client, async_mock_cpo_client, emsp_auth_headers, cpo_auth_headers, test_data_factory
    ):
        """Test cancel reservation command flow."""
        # Step 1: Create a reservation first (simulated)
        reservation_id = "RES_001"

        # Step 2: EMSP sends CANCEL_RESERVATION command to CPO
        cancel_command = test_data_factory.create_command(
            command_type="CANCEL_RESERVATION",
            response_url="https://emsp.example.com/ocpi/emsp/2.2.1/commands/CANCEL_RESERVATION/012",
        )
        cancel_command["reservation_id"] = reservation_id

        command_response = await async_emsp_client.post(
            "/ocpi/emsp/2.2.1/commands/CANCEL_RESERVATION", headers=emsp_auth_headers, json=cancel_command
        )
        assert command_response.status_code in [200, 201]

        command_result = command_response.json()["data"]
        assert "result" in command_result
        assert command_result["result"] in ["ACCEPTED", "REJECTED"]

    async def test_unlock_connector_command_flow(
        self, async_emsp_client, async_mock_cpo_client, emsp_auth_headers, cpo_auth_headers, test_data_factory
    ):
        """Test unlock connector command flow."""
        # Step 1: EMSP sends UNLOCK_CONNECTOR command to CPO
        unlock_command = test_data_factory.create_command(
            command_type="UNLOCK_CONNECTOR",
            response_url="https://emsp.example.com/ocpi/emsp/2.2.1/commands/UNLOCK_CONNECTOR/345",
        )

        command_response = await async_emsp_client.post(
            "/ocpi/emsp/2.2.1/commands/UNLOCK_CONNECTOR", headers=emsp_auth_headers, json=unlock_command
        )
        assert command_response.status_code in [200, 201]

        command_result = command_response.json()["data"]
        assert "result" in command_result
        assert command_result["result"] in ["ACCEPTED", "REJECTED"]

    async def test_command_timeout_handling(self, async_emsp_client, emsp_auth_headers, test_data_factory):
        """Test command timeout handling."""
        # Send command with short timeout
        command = test_data_factory.create_command(
            command_type="START_SESSION",
            response_url="https://emsp.example.com/ocpi/emsp/2.2.1/commands/START_SESSION/timeout",
        )

        start_time = datetime.now()
        command_response = await async_emsp_client.post(
            "/ocpi/emsp/2.2.1/commands/START_SESSION", headers=emsp_auth_headers, json=command
        )
        end_time = datetime.now()

        # Command should respond within reasonable time
        duration = (end_time - start_time).total_seconds()
        assert duration < 30.0, f"Command took too long: {duration}s"

        assert command_response.status_code in [200, 201]
        command_result = command_response.json()["data"]
        assert "result" in command_result

    async def test_command_error_handling(self, async_emsp_client, emsp_auth_headers, test_data_factory):
        """Test command error handling for invalid requests."""
        # Send command with invalid data
        invalid_command = {
            "response_url": "invalid-url",
            "token": {
                "country_code": "",  # Invalid empty country code
                "party_id": "",  # Invalid empty party ID
                "uid": "",  # Invalid empty UID
                "type": "INVALID",  # Invalid token type
                "contract_id": "",  # Invalid empty contract ID
            },
            "location_id": "",  # Invalid empty location ID
            "evse_uid": "",  # Invalid empty EVSE UID
            "connector_id": "",  # Invalid empty connector ID
        }

        command_response = await async_emsp_client.post(
            "/ocpi/emsp/2.2.1/commands/START_SESSION", headers=emsp_auth_headers, json=invalid_command
        )

        # Should return error status
        assert command_response.status_code in [400, 422]

    async def test_command_result_callback(self, async_emsp_client, emsp_auth_headers, test_data_factory):
        """Test command result callback mechanism."""
        # This test simulates the callback mechanism
        # In real implementation, CPO would call back to EMSP with result

        command = test_data_factory.create_command(
            command_type="START_SESSION",
            response_url="https://emsp.example.com/ocpi/emsp/2.2.1/commands/START_SESSION/callback",
        )

        # Send initial command
        command_response = await async_emsp_client.post(
            "/ocpi/emsp/2.2.1/commands/START_SESSION", headers=emsp_auth_headers, json=command
        )
        assert command_response.status_code in [200, 201]

        # Simulate callback with command result
        callback_result = test_data_factory.create_command_response(result="ACCEPTED")

        # In real scenario, this would be called by CPO
        callback_response = await async_emsp_client.post(
            "/ocpi/emsp/2.2.1/commands/START_SESSION/callback", headers=emsp_auth_headers, json=callback_result
        )

        # Callback should be accepted
        assert callback_response.status_code in [200, 201]

    async def test_concurrent_commands(self, async_emsp_client, emsp_auth_headers, test_data_factory):
        """Test handling of concurrent commands."""

        async def send_command(command_type, index):
            command = test_data_factory.create_command(
                command_type=command_type,
                response_url=f"https://emsp.example.com/ocpi/emsp/2.2.1/commands/{command_type}/{index}",
            )

            response = await async_emsp_client.post(
                f"/ocpi/emsp/2.2.1/commands/{command_type}", headers=emsp_auth_headers, json=command
            )
            return response.status_code in [200, 201]

        # Send multiple commands concurrently
        tasks = [send_command("START_SESSION", i) for i in range(3)] + [
            send_command("RESERVE_NOW", i) for i in range(2)
        ]

        results = await asyncio.gather(*tasks)

        # All commands should be processed successfully
        assert all(results), "Some concurrent commands failed"

    @pytest.mark.slow
    async def test_command_performance(self, async_emsp_client, emsp_auth_headers, test_data_factory):
        """Test command processing performance."""
        import time

        # Measure command processing time
        command = test_data_factory.create_command(
            command_type="START_SESSION",
            response_url="https://emsp.example.com/ocpi/emsp/2.2.1/commands/START_SESSION/perf",
        )

        start_time = time.time()
        command_response = await async_emsp_client.post(
            "/ocpi/emsp/2.2.1/commands/START_SESSION", headers=emsp_auth_headers, json=command
        )
        end_time = time.time()

        # Command should process quickly
        duration = end_time - start_time
        assert duration < 2.0, f"Command processing too slow: {duration}s"

        assert command_response.status_code in [200, 201]
        command_result = command_response.json()["data"]
        assert "result" in command_result
