#!/usr/bin/env python3
"""
OCPI EMSP-CPO Demo Startup Script
=================================

This script provides an educational demonstration of OCPI (Open Charge Point Interface)
interactions between an EMSP (E-Mobility Service Provider) and CPO (Charge Point Operator).

🎯 What is OCPI?
OCPI is a protocol that enables communication between different actors in the EV charging
ecosystem. It allows EMSPs (like charging apps) to communicate with CPOs (charging station
operators) to provide seamless charging experiences for EV drivers.

🏗️ Architecture:
- EMSP Backend (Port 8000): Represents a charging app/service provider
- Mock CPO Server (Port 8001): Simulates a charging station operator
- Both systems communicate using OCPI 2.2.1 protocol

🔄 Key OCPI Flows Demonstrated:
1. Authentication & Credential Exchange
2. Location Discovery (CPO shares charging station info)
3. Token Authorization (EMSP user wants to charge)
4. Session Management (start/stop charging)
5. CDR Processing (billing information)

Usage:
    python start_ocpi_demo.py [options]

Options:
    --emsp-only     Start only EMSP backend
    --cpo-only      Start only Mock CPO server
    --no-tests      Skip running demo tests
    --port-emsp     EMSP port (default: 8000)
    --port-cpo      Mock CPO port (default: 8001)
    --help          Show this help message
"""

import argparse
import asyncio
import logging
import os
import signal
import subprocess
import sys
import time
from typing import Optional

import httpx

# Configure logging for educational output
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("ocpi_demo.log")],
)
logger = logging.getLogger(__name__)


class OCPIDemoManager:
    """Manages the OCPI demonstration environment."""

    def __init__(self, emsp_port: int = 8000, cpo_port: int = 8001):
        self.emsp_port = emsp_port
        self.cpo_port = cpo_port
        self.emsp_process: Optional[subprocess.Popen] = None
        self.cpo_process: Optional[subprocess.Popen] = None
        self.running = False

    def print_banner(self):
        """Print educational banner about OCPI."""
        print("\n" + "=" * 80)
        print("🚗⚡ OCPI EMSP-CPO Educational Demo")
        print("=" * 80)
        print("📚 OCPI (Open Charge Point Interface) Protocol Demonstration")
        print()
        print("🎯 Learning Objectives:")
        print("   • Understand EMSP-CPO communication patterns")
        print("   • See OCPI 2.2.1 protocol in action")
        print("   • Learn about EV charging ecosystem interactions")
        print()
        print("🏗️  System Architecture:")
        print(f"   📱 EMSP Backend    → http://localhost:{self.emsp_port}")
        print(f"   🔌 Mock CPO Server → http://localhost:{self.cpo_port}")
        print()
        print("🔄 OCPI Flows Available:")
        print("   1. Authentication & Credential Exchange")
        print("   2. Location Discovery (charging stations)")
        print("   3. Token Authorization (user authentication)")
        print("   4. Session Management (start/stop charging)")
        print("   5. CDR Processing (billing records)")
        print("=" * 80)

    def check_ports(self) -> bool:
        """Check if required ports are available."""
        import socket

        ports_to_check = [self.emsp_port, self.cpo_port]
        for port in ports_to_check:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                result = sock.connect_ex(("localhost", port))
                if result == 0:
                    print(f"❌ Port {port} is already in use!")
                    print(f"💡 Try: lsof -ti:{port} | xargs kill -9")
                    return False
        return True

    def start_emsp_backend(self):
        """Start the EMSP backend server."""
        print(f"\n🚀 Starting EMSP Backend on port {self.emsp_port}...")
        print("📱 EMSP = E-Mobility Service Provider (like a charging app)")

        try:
            # Use pipenv if available, otherwise use python directly
            if os.path.exists("Pipfile"):
                cmd = [
                    "pipenv",
                    "run",
                    "python",
                    "-m",
                    "uvicorn",
                    "main:app",
                    "--host",
                    "0.0.0.0",
                    "--port",
                    str(self.emsp_port),
                ]
            else:
                cmd = ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", str(self.emsp_port)]

            self.emsp_process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1
            )

            # Wait for startup
            time.sleep(3)

            if self.emsp_process.poll() is None:
                print("✅ EMSP Backend started successfully!")
                print(f"🌐 API Documentation: http://localhost:{self.emsp_port}/docs")
                print(f"📊 OCPI Endpoints: http://localhost:{self.emsp_port}/ocpi/emsp/2.2.1/versions")
                return True
            else:
                print("❌ EMSP Backend failed to start")
                return False

        except Exception as e:
            print(f"❌ Error starting EMSP Backend: {e}")
            return False

    def start_mock_cpo(self):
        """Start the Mock CPO server."""
        print(f"\n🚀 Starting Mock CPO Server on port {self.cpo_port}...")
        print("🔌 CPO = Charge Point Operator (manages charging stations)")

        try:
            # Create a script to run the mock CPO server
            mock_cpo_script = f"""
import uvicorn
from tests.mock_cpo_server import mock_cpo_app

if __name__ == "__main__":
    uvicorn.run(mock_cpo_app, host="0.0.0.0", port={self.cpo_port})
"""

            with open("run_mock_cpo.py", "w") as f:
                f.write(mock_cpo_script)

            if os.path.exists("Pipfile"):
                cmd = ["pipenv", "run", "python", "run_mock_cpo.py"]
            else:
                cmd = ["python", "run_mock_cpo.py"]

            self.cpo_process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1
            )

            # Wait for startup
            time.sleep(3)

            if self.cpo_process.poll() is None:
                print("✅ Mock CPO Server started successfully!")
                print(f"🌐 API Documentation: http://localhost:{self.cpo_port}/docs")
                print(f"📊 OCPI Endpoints: http://localhost:{self.cpo_port}/ocpi/cpo/2.2.1/versions")
                return True
            else:
                print("❌ Mock CPO Server failed to start")
                return False

        except Exception as e:
            print(f"❌ Error starting Mock CPO Server: {e}")
            return False

    async def health_check(self) -> bool:
        """Perform health checks on both services."""
        print("\n🔍 Performing health checks...")

        async with httpx.AsyncClient() as client:
            # Check EMSP Backend
            try:
                response = await client.get(f"http://localhost:{self.emsp_port}/")
                if response.status_code == 200:
                    print("✅ EMSP Backend is healthy")
                    emsp_healthy = True
                else:
                    print(f"⚠️  EMSP Backend returned status {response.status_code}")
                    emsp_healthy = False
            except Exception as e:
                print(f"❌ EMSP Backend health check failed: {e}")
                emsp_healthy = False

            # Check Mock CPO Server
            try:
                response = await client.get(f"http://localhost:{self.cpo_port}/")
                if response.status_code == 200:
                    print("✅ Mock CPO Server is healthy")
                    cpo_healthy = True
                else:
                    print(f"⚠️  Mock CPO Server returned status {response.status_code}")
                    cpo_healthy = False
            except Exception as e:
                print(f"❌ Mock CPO Server health check failed: {e}")
                cpo_healthy = False

        return emsp_healthy and cpo_healthy

    async def run_demo_tests(self):
        """Run educational demo tests."""
        print("\n🧪 Running Educational OCPI Demo Tests...")
        print("📚 These tests demonstrate key OCPI interactions:")

        # Run authentication tests
        print("\n1️⃣  Testing Authentication & Credential Exchange...")
        result = subprocess.run(
            [
                "pipenv",
                "run",
                "python",
                "-m",
                "pytest",
                "tests/integration/test_authentication.py::TestOCPIAuthentication::test_emsp_token_validation",
                "-v",
                "--tb=short",
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            print("✅ Authentication test passed!")
        else:
            print("❌ Authentication test failed")
            print(result.stdout)

        # Add more demo tests here
        print("\n📊 Demo tests completed!")

    def cleanup(self):
        """Clean up processes and temporary files."""
        print("\n🧹 Cleaning up...")

        if self.emsp_process:
            self.emsp_process.terminate()
            self.emsp_process.wait()
            print("✅ EMSP Backend stopped")

        if self.cpo_process:
            self.cpo_process.terminate()
            self.cpo_process.wait()
            print("✅ Mock CPO Server stopped")

        # Clean up temporary files
        if os.path.exists("run_mock_cpo.py"):
            os.remove("run_mock_cpo.py")

        print("🎉 Cleanup completed!")

    def signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        print(f"\n🛑 Received signal {signum}, shutting down...")
        self.running = False
        self.cleanup()
        sys.exit(0)

    async def start_demo(self, start_emsp: bool = True, start_cpo: bool = True, run_tests: bool = True):
        """Start the complete OCPI demo environment."""
        self.print_banner()

        # Set up signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        # Check ports
        if not self.check_ports():
            return False

        self.running = True

        try:
            # Start services
            if start_emsp and not self.start_emsp_backend():
                return False

            if start_cpo and not self.start_mock_cpo():
                return False

            # Health checks
            if not await self.health_check():
                print("⚠️  Some services are not healthy, but continuing...")

            # Run demo tests
            if run_tests:
                await self.run_demo_tests()

            # Keep running
            print("\n🎉 OCPI Demo Environment is ready!")
            print("\n💡 What you can do now:")
            print(f"   • Visit EMSP API docs: http://localhost:{self.emsp_port}/docs")
            print(f"   • Visit CPO API docs: http://localhost:{self.cpo_port}/docs")
            print("   • Run tests: python run_tests.py integration")
            print("   • Press Ctrl+C to stop")

            # Keep the demo running
            while self.running:
                await asyncio.sleep(1)

        except KeyboardInterrupt:
            print("\n🛑 Demo stopped by user")
        except Exception as e:
            print(f"❌ Demo error: {e}")
        finally:
            self.cleanup()

        return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="OCPI EMSP-CPO Educational Demo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument("--emsp-only", action="store_true", help="Start only EMSP backend")
    parser.add_argument("--cpo-only", action="store_true", help="Start only Mock CPO server")
    parser.add_argument("--no-tests", action="store_true", help="Skip running demo tests")
    parser.add_argument("--port-emsp", type=int, default=8000, help="EMSP port (default: 8000)")
    parser.add_argument("--port-cpo", type=int, default=8001, help="Mock CPO port (default: 8001)")

    args = parser.parse_args()

    # Determine what to start
    start_emsp = not args.cpo_only
    start_cpo = not args.emsp_only
    run_tests = not args.no_tests

    # Create and run demo
    demo = OCPIDemoManager(args.port_emsp, args.port_cpo)

    try:
        asyncio.run(demo.start_demo(start_emsp, start_cpo, run_tests))
    except KeyboardInterrupt:
        print("\n👋 Demo stopped by user")
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
