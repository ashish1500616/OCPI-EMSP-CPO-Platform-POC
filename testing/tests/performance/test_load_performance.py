"""
Load and Performance Tests
==========================

Tests that validate system performance under load, including concurrent
requests, high-frequency operations, and resource usage validation.
"""

import asyncio
import time

import pytest


@pytest.mark.performance
@pytest.mark.slow
@pytest.mark.asyncio
class TestLoadPerformance:
    """Test system performance under load."""

    async def test_concurrent_authentication_requests(self, async_emsp_client, emsp_auth_headers):
        """Test concurrent authentication request performance."""

        async def make_auth_request():
            start_time = time.time()
            response = await async_emsp_client.get("/ocpi/emsp/2.2.1/versions", headers=emsp_auth_headers)
            end_time = time.time()
            return {
                "success": response.status_code == 200,
                "duration": end_time - start_time,
                "status_code": response.status_code,
            }

        # Test with 50 concurrent requests
        num_requests = 50
        start_time = time.time()

        tasks = [make_auth_request() for _ in range(num_requests)]
        results = await asyncio.gather(*tasks)

        end_time = time.time()
        total_duration = end_time - start_time

        # Analyze results
        successful_requests = sum(1 for r in results if r["success"])
        average_duration = sum(r["duration"] for r in results) / len(results)
        max_duration = max(r["duration"] for r in results)
        min_duration = min(r["duration"] for r in results)

        # Performance assertions
        assert successful_requests == num_requests, f"Only {successful_requests}/{num_requests} requests succeeded"
        assert total_duration < 10.0, f"Total time too long: {total_duration}s"
        assert average_duration < 1.0, f"Average request time too long: {average_duration}s"
        assert max_duration < 2.0, f"Max request time too long: {max_duration}s"

        # Calculate requests per second
        rps = num_requests / total_duration
        assert rps > 10, f"Requests per second too low: {rps}"

        print("Performance metrics:")
        print(f"  Total requests: {num_requests}")
        print(f"  Successful requests: {successful_requests}")
        print(f"  Total duration: {total_duration:.2f}s")
        print(f"  Average request duration: {average_duration:.3f}s")
        print(f"  Min request duration: {min_duration:.3f}s")
        print(f"  Max request duration: {max_duration:.3f}s")
        print(f"  Requests per second: {rps:.2f}")

    async def test_location_endpoint_performance(self, async_emsp_client, emsp_auth_headers):
        """Test location endpoint performance under load."""

        async def fetch_locations():
            start_time = time.time()
            response = await async_emsp_client.get("/ocpi/emsp/2.2.1/locations", headers=emsp_auth_headers)
            end_time = time.time()
            return {
                "success": response.status_code == 200,
                "duration": end_time - start_time,
                "data_size": len(response.content) if response.status_code == 200 else 0,
            }

        # Test with 30 concurrent requests
        num_requests = 30
        tasks = [fetch_locations() for _ in range(num_requests)]
        results = await asyncio.gather(*tasks)

        # Analyze results
        successful_requests = sum(1 for r in results if r["success"])
        average_duration = sum(r["duration"] for r in results) / len(results)
        average_data_size = sum(r["data_size"] for r in results) / len(results)

        # Performance assertions
        assert successful_requests == num_requests, f"Only {successful_requests}/{num_requests} requests succeeded"
        assert average_duration < 2.0, f"Average location fetch time too long: {average_duration}s"

        print("Location endpoint performance:")
        print(f"  Successful requests: {successful_requests}/{num_requests}")
        print(f"  Average duration: {average_duration:.3f}s")
        print(f"  Average response size: {average_data_size:.0f} bytes")

    async def test_session_endpoint_performance(self, async_emsp_client, emsp_auth_headers):
        """Test session endpoint performance under load."""

        async def fetch_sessions():
            start_time = time.time()
            response = await async_emsp_client.get("/ocpi/emsp/2.2.1/sessions", headers=emsp_auth_headers)
            end_time = time.time()
            return {"success": response.status_code == 200, "duration": end_time - start_time}

        # Test with 25 concurrent requests
        num_requests = 25
        tasks = [fetch_sessions() for _ in range(num_requests)]
        results = await asyncio.gather(*tasks)

        # Analyze results
        successful_requests = sum(1 for r in results if r["success"])
        average_duration = sum(r["duration"] for r in results) / len(results)

        # Performance assertions
        assert successful_requests == num_requests, f"Only {successful_requests}/{num_requests} requests succeeded"
        assert average_duration < 2.0, f"Average session fetch time too long: {average_duration}s"

        print("Session endpoint performance:")
        print(f"  Successful requests: {successful_requests}/{num_requests}")
        print(f"  Average duration: {average_duration:.3f}s")

    async def test_command_processing_performance(self, async_emsp_client, emsp_auth_headers, test_data_factory):
        """Test command processing performance."""

        async def send_command():
            command = test_data_factory.create_command(
                command_type="START_SESSION",
                response_url="https://emsp.example.com/ocpi/emsp/2.2.1/commands/START_SESSION/perf",
            )

            start_time = time.time()
            response = await async_emsp_client.post(
                "/ocpi/emsp/2.2.1/commands/START_SESSION", headers=emsp_auth_headers, json=command
            )
            end_time = time.time()

            return {
                "success": response.status_code in [200, 201],
                "duration": end_time - start_time,
                "status_code": response.status_code,
            }

        # Test with 20 concurrent commands
        num_commands = 20
        tasks = [send_command() for _ in range(num_commands)]
        results = await asyncio.gather(*tasks)

        # Analyze results
        successful_commands = sum(1 for r in results if r["success"])
        average_duration = sum(r["duration"] for r in results) / len(results)
        max_duration = max(r["duration"] for r in results)

        # Performance assertions
        assert (
            successful_commands >= num_commands * 0.8
        ), f"Too many failed commands: {successful_commands}/{num_commands}"
        assert average_duration < 3.0, f"Average command processing too slow: {average_duration}s"
        assert max_duration < 5.0, f"Max command processing too slow: {max_duration}s"

        print("Command processing performance:")
        print(f"  Successful commands: {successful_commands}/{num_commands}")
        print(f"  Average duration: {average_duration:.3f}s")
        print(f"  Max duration: {max_duration:.3f}s")

    async def test_mixed_workload_performance(self, async_emsp_client, emsp_auth_headers, test_data_factory):
        """Test performance with mixed workload (different endpoint types)."""

        async def mixed_request(request_type, index):
            start_time = time.time()

            if request_type == "versions":
                response = await async_emsp_client.get("/ocpi/emsp/2.2.1/versions", headers=emsp_auth_headers)
            elif request_type == "locations":
                response = await async_emsp_client.get("/ocpi/emsp/2.2.1/locations", headers=emsp_auth_headers)
            elif request_type == "sessions":
                response = await async_emsp_client.get("/ocpi/emsp/2.2.1/sessions", headers=emsp_auth_headers)
            elif request_type == "command":
                command = test_data_factory.create_command(
                    command_type="START_SESSION",
                    response_url=f"https://emsp.example.com/ocpi/emsp/2.2.1/commands/START_SESSION/mixed_{index}",
                )
                response = await async_emsp_client.post(
                    "/ocpi/emsp/2.2.1/commands/START_SESSION", headers=emsp_auth_headers, json=command
                )
            else:
                raise ValueError(f"Unknown request type: {request_type}")

            end_time = time.time()

            return {
                "type": request_type,
                "success": response.status_code in [200, 201],
                "duration": end_time - start_time,
                "status_code": response.status_code,
            }

        # Create mixed workload
        tasks = []
        request_types = ["versions", "locations", "sessions", "command"]

        for i in range(40):  # 40 total requests
            request_type = request_types[i % len(request_types)]
            tasks.append(mixed_request(request_type, i))

        # Execute mixed workload
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        end_time = time.time()

        total_duration = end_time - start_time

        # Analyze results by type
        by_type = {}
        for result in results:
            req_type = result["type"]
            if req_type not in by_type:
                by_type[req_type] = []
            by_type[req_type].append(result)

        # Performance assertions
        total_successful = sum(1 for r in results if r["success"])
        assert total_successful >= len(results) * 0.8, f"Too many failed requests: {total_successful}/{len(results)}"
        assert total_duration < 15.0, f"Mixed workload took too long: {total_duration}s"

        print("Mixed workload performance:")
        print(f"  Total requests: {len(results)}")
        print(f"  Successful requests: {total_successful}")
        print(f"  Total duration: {total_duration:.2f}s")
        print(f"  Overall RPS: {len(results) / total_duration:.2f}")

        for req_type, type_results in by_type.items():
            successful = sum(1 for r in type_results if r["success"])
            avg_duration = sum(r["duration"] for r in type_results) / len(type_results)
            print(f"  {req_type}: {successful}/{len(type_results)} successful, avg {avg_duration:.3f}s")

    @pytest.mark.benchmark
    async def test_endpoint_benchmarks(self, async_emsp_client, emsp_auth_headers):
        """Benchmark critical endpoints."""
        endpoints = [
            "/ocpi/emsp/2.2.1/versions",
            "/ocpi/emsp/2.2.1/versions/2.2.1",
            "/ocpi/emsp/2.2.1/locations",
            "/ocpi/emsp/2.2.1/sessions",
        ]

        benchmark_results = {}

        for endpoint in endpoints:
            # Warm up
            for _ in range(3):
                await async_emsp_client.get(endpoint, headers=emsp_auth_headers)

            # Benchmark
            durations = []
            for _ in range(10):
                start_time = time.time()
                response = await async_emsp_client.get(endpoint, headers=emsp_auth_headers)
                end_time = time.time()

                if response.status_code == 200:
                    durations.append(end_time - start_time)

            if durations:
                avg_duration = sum(durations) / len(durations)
                min_duration = min(durations)
                max_duration = max(durations)

                benchmark_results[endpoint] = {
                    "avg": avg_duration,
                    "min": min_duration,
                    "max": max_duration,
                    "samples": len(durations),
                }

        # Print benchmark results
        print("\nEndpoint Benchmarks:")
        for endpoint, metrics in benchmark_results.items():
            print(f"  {endpoint}:")
            print(f"    Average: {metrics['avg']:.3f}s")
            print(f"    Min: {metrics['min']:.3f}s")
            print(f"    Max: {metrics['max']:.3f}s")
            print(f"    Samples: {metrics['samples']}")

        # Performance assertions
        for endpoint, metrics in benchmark_results.items():
            assert metrics["avg"] < 1.0, f"Average response time too slow for {endpoint}: {metrics['avg']}s"
            assert metrics["max"] < 2.0, f"Max response time too slow for {endpoint}: {metrics['max']}s"
