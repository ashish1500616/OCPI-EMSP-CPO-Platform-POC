#!/usr/bin/env python3
"""
OCPI Educational Demo Runner
===========================

This script provides step-by-step educational demonstrations of OCPI concepts
with detailed explanations of what's happening in each interaction.

🎓 Educational Goals:
- Understand OCPI protocol fundamentals
- Learn EMSP-CPO communication patterns
- See real OCPI message flows
- Understand EV charging ecosystem roles

Usage:
    python ocpi_educational_demo.py [demo_type]

Demo Types:
    all             - Run all educational demos
    authentication  - Authentication and credential exchange
    locations       - Location discovery workflow
    tokens          - Token authorization flow
    sessions        - Session management (start/stop charging)
    cdrs            - Charge Detail Record processing
    interactive     - Interactive menu-driven demo
"""

import asyncio
import json
from typing import Dict, Optional

import httpx


class OCPIEducationalDemo:
    """Educational demonstration of OCPI concepts."""

    def __init__(self, emsp_port: int = 8000, cpo_port: int = 8001):
        self.emsp_base_url = f"http://localhost:{emsp_port}"
        self.cpo_base_url = f"http://localhost:{cpo_port}"

        # Educational authentication tokens
        self.emsp_headers = {
            "Authorization": "Token emsp_token_a_12345",
            "Content-Type": "application/json",
            "X-Request-ID": "demo-request-001",
            "X-Correlation-ID": "demo-correlation-001",
        }

        self.cpo_headers = {
            "Authorization": "Token cpo_token_c_abcdef",
            "Content-Type": "application/json",
            "X-Request-ID": "demo-cpo-request-001",
            "X-Correlation-ID": "demo-cpo-correlation-001",
        }

    def print_section_header(self, title: str, description: str):
        """Print a formatted section header."""
        print("\n" + "=" * 80)
        print(f"📚 {title}")
        print("=" * 80)
        print(f"💡 {description}")
        print("-" * 80)

    def print_step(self, step_num: int, title: str, description: str):
        """Print a formatted step."""
        print(f"\n🔸 Step {step_num}: {title}")
        print(f"   {description}")

    def print_ocpi_message(self, direction: str, endpoint: str, data: Optional[Dict] = None):
        """Print OCPI message details."""
        print(f"\n📡 OCPI Message: {direction}")
        print(f"   Endpoint: {endpoint}")
        if data:
            print(f"   Data: {json.dumps(data, indent=2)}")

    def wait_for_user(self, message: str = "Press Enter to continue..."):
        """Wait for user input."""
        input(f"\n⏸️  {message}")

    async def demo_authentication(self):
        """Demonstrate OCPI authentication and credential exchange."""
        self.print_section_header(
            "OCPI Authentication & Credential Exchange",
            "Learn how EMSP and CPO systems establish trust and exchange credentials",
        )

        print("\n🎯 What you'll learn:")
        print("   • OCPI Token A and Token C authentication")
        print("   • Credential exchange process")
        print("   • Version negotiation")
        print("   • Endpoint discovery")

        self.wait_for_user()

        async with httpx.AsyncClient() as client:
            # Step 1: Version Discovery
            self.print_step(1, "Version Discovery", "EMSP discovers what OCPI versions the CPO supports")

            try:
                response = await client.get(f"{self.emsp_base_url}/ocpi/emsp/2.2.1/versions", headers=self.emsp_headers)

                self.print_ocpi_message("EMSP → CPO", "/ocpi/emsp/2.2.1/versions")

                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Response: {response.status_code}")
                    print(f"📋 Available versions: {len(data.get('data', []))}")

                    for version in data.get("data", []):
                        print(f"   • Version {version.get('version')}: {version.get('url')}")
                else:
                    print(f"❌ Error: {response.status_code}")

            except Exception as e:
                print(f"❌ Connection error: {e}")

            self.wait_for_user()

            # Step 2: Endpoint Discovery
            self.print_step(2, "Endpoint Discovery", "Discover available OCPI modules and their endpoints")

            try:
                response = await client.get(
                    f"{self.emsp_base_url}/ocpi/emsp/2.2.1/versions/2.2.1", headers=self.emsp_headers
                )

                self.print_ocpi_message("EMSP → CPO", "/ocpi/emsp/2.2.1/versions/2.2.1")

                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Response: {response.status_code}")
                    print("📋 Available endpoints:")

                    for endpoint in data.get("data", {}).get("endpoints", []):
                        role = endpoint.get("role", "UNKNOWN")
                        identifier = endpoint.get("identifier", "unknown")
                        url = endpoint.get("url", "")
                        print(f"   • {identifier} ({role}): {url}")

                else:
                    print(f"❌ Error: {response.status_code}")

            except Exception as e:
                print(f"❌ Connection error: {e}")

            self.wait_for_user()

            # Step 3: Credential Exchange
            self.print_step(3, "Credential Exchange", "Exchange credentials to establish secure communication")

            print("\n📝 In a real scenario:")
            print("   1. EMSP and CPO exchange credentials containing:")
            print("      • Authentication tokens")
            print("      • Business details (company info)")
            print("      • Supported OCPI modules")
            print("      • Endpoint URLs")
            print("   2. Both parties validate and store credentials")
            print("   3. Future API calls use exchanged tokens")

        print("\n🎉 Authentication demo completed!")
        print("💡 Key takeaway: OCPI uses token-based authentication with credential exchange")

    async def demo_location_discovery(self):
        """Demonstrate location discovery workflow."""
        self.print_section_header("Location Discovery Workflow", "Learn how EMSPs discover charging stations from CPOs")

        print("\n🎯 What you'll learn:")
        print("   • How CPOs share charging station information")
        print("   • Location, EVSE, and Connector data structures")
        print("   • Real-time status updates")
        print("   • Geographic and capability-based filtering")

        self.wait_for_user()

        async with httpx.AsyncClient() as client:
            # Step 1: Discover Locations
            self.print_step(1, "Location Discovery", "EMSP requests list of available charging locations from CPO")

            try:
                response = await client.get(
                    f"{self.emsp_base_url}/ocpi/emsp/2.2.1/locations", headers=self.emsp_headers
                )

                self.print_ocpi_message("EMSP → CPO", "/ocpi/emsp/2.2.1/locations")

                if response.status_code == 200:
                    data = response.json()
                    locations = data.get("data", [])
                    print(f"✅ Response: {response.status_code}")
                    print(f"📍 Found {len(locations)} charging locations")

                    for i, location in enumerate(locations[:2]):  # Show first 2
                        print(f"\n   Location {i+1}:")
                        print(f"   • ID: {location.get('id')}")
                        print(f"   • Name: {location.get('name')}")
                        print(f"   • Address: {location.get('address')}")
                        print(f"   • EVSEs: {len(location.get('evses', []))}")

                        # Show EVSE details
                        for evse in location.get("evses", [])[:1]:  # Show first EVSE
                            print(f"     EVSE {evse.get('uid')}:")
                            print(f"     • Status: {evse.get('status')}")
                            print(f"     • Connectors: {len(evse.get('connectors', []))}")

                            for connector in evse.get("connectors", [])[:1]:  # Show first connector
                                print(f"       Connector {connector.get('id')}:")
                                print(f"       • Standard: {connector.get('standard')}")
                                print(f"       • Power: {connector.get('max_electric_power')}W")

                else:
                    print(f"❌ Error: {response.status_code}")

            except Exception as e:
                print(f"❌ Connection error: {e}")

            self.wait_for_user()

        print("\n🎉 Location discovery demo completed!")
        print("💡 Key takeaway: CPOs share detailed charging infrastructure data with EMSPs")

    async def demo_token_authorization(self):
        """Demonstrate token authorization flow."""
        self.print_section_header(
            "Token Authorization Flow", "Learn how EMSP users get authorized to charge at CPO stations"
        )

        print("\n🎯 What you'll learn:")
        print("   • RFID/App token validation")
        print("   • Real-time authorization requests")
        print("   • Authorization responses and restrictions")
        print("   • User account validation")

        self.wait_for_user()

        print("\n📝 Token Authorization Process:")
        print("   1. EV driver approaches charging station")
        print("   2. Driver presents RFID card or uses mobile app")
        print("   3. CPO sends authorization request to EMSP")
        print("   4. EMSP validates user account and responds")
        print("   5. CPO allows or denies charging based on response")

        # Simulate authorization request
        self.print_step(1, "Authorization Request", "CPO requests authorization for user token")

        token_data = {
            "country_code": "US",
            "party_id": "EMS",
            "uid": "DEMO_TOKEN_001",
            "type": "RFID",
            "contract_id": "CONTRACT_12345",
        }

        auth_request = {"token": token_data, "location_id": "LOC001", "evse_uid": "EVSE001", "connector_id": "1"}

        self.print_ocpi_message("CPO → EMSP", "/tokens/authorize", auth_request)

        print("\n✅ Simulated Authorization Response:")
        print("   • Allowed: True")
        print("   • Authorization Reference: AUTH_REF_789")
        print("   • User Info: John Doe (Premium Account)")
        print("   • Restrictions: Max 50kWh per session")

        self.wait_for_user()

        print("\n🎉 Token authorization demo completed!")
        print("💡 Key takeaway: Real-time authorization ensures only valid users can charge")

    async def demo_session_management(self):
        """Demonstrate session management workflow."""
        self.print_section_header(
            "Session Management Workflow", "Learn how charging sessions are started, monitored, and stopped"
        )

        print("\n🎯 What you'll learn:")
        print("   • START_SESSION and STOP_SESSION commands")
        print("   • Session status monitoring")
        print("   • Real-time energy consumption tracking")
        print("   • Session completion and billing preparation")

        self.wait_for_user()

        # Step 1: Start Session Command
        self.print_step(1, "Start Session Command", "EMSP sends command to CPO to start charging session")

        start_command = {
            "response_url": f"{self.emsp_base_url}/ocpi/emsp/2.2.1/commands/START_SESSION/demo123",
            "token": {
                "country_code": "US",
                "party_id": "EMS",
                "uid": "DEMO_TOKEN_001",
                "type": "RFID",
                "contract_id": "CONTRACT_12345",
            },
            "location_id": "LOC001",
            "evse_uid": "EVSE001",
            "connector_id": "1",
        }

        self.print_ocpi_message("EMSP → CPO", "/commands/START_SESSION", start_command)

        print("\n✅ Command Response:")
        print("   • Result: ACCEPTED")
        print("   • Timeout: 30 seconds")
        print("   • Message: Session will start shortly")

        self.wait_for_user()

        # Step 2: Session Monitoring
        self.print_step(2, "Session Monitoring", "Monitor active charging session progress")

        session_data = {
            "id": "SESSION_DEMO_001",
            "start_date_time": "2024-01-15T10:30:00Z",
            "kwh": 15.5,
            "status": "ACTIVE",
            "location_id": "LOC001",
            "evse_uid": "EVSE001",
            "connector_id": "1",
            "currency": "USD",
        }

        self.print_ocpi_message("CPO → EMSP", "/sessions/SESSION_DEMO_001", session_data)

        print("\n📊 Session Progress:")
        print("   • Duration: 45 minutes")
        print("   • Energy Consumed: 15.5 kWh")
        print("   • Current Power: 22 kW")
        print("   • Estimated Cost: $4.65")

        self.wait_for_user()

        # Step 3: Stop Session
        self.print_step(3, "Stop Session Command", "User or system initiates session termination")

        stop_command = {
            "response_url": f"{self.emsp_base_url}/ocpi/emsp/2.2.1/commands/STOP_SESSION/demo456",
            "session_id": "SESSION_DEMO_001",
        }

        self.print_ocpi_message("EMSP → CPO", "/commands/STOP_SESSION", stop_command)

        print("\n✅ Session Completed:")
        print("   • Final Energy: 18.2 kWh")
        print("   • Duration: 52 minutes")
        print("   • Status: COMPLETED")
        print("   • CDR will be generated for billing")

        self.wait_for_user()

        print("\n🎉 Session management demo completed!")
        print("💡 Key takeaway: OCPI enables real-time session control and monitoring")

    async def demo_cdr_processing(self):
        """Demonstrate CDR (Charge Detail Record) processing."""
        self.print_section_header(
            "CDR Processing Workflow", "Learn how billing information is exchanged after charging sessions"
        )

        print("\n🎯 What you'll learn:")
        print("   • CDR structure and required fields")
        print("   • Tariff application and cost calculation")
        print("   • Billing data exchange")
        print("   • Invoice generation preparation")

        self.wait_for_user()

        # Step 1: CDR Generation
        self.print_step(1, "CDR Generation", "CPO generates detailed billing record after session completion")

        cdr_data = {
            "id": "CDR_DEMO_001",
            "start_date_time": "2024-01-15T10:30:00Z",
            "end_date_time": "2024-01-15T11:22:00Z",
            "session_id": "SESSION_DEMO_001",
            "cdr_token": {
                "country_code": "US",
                "party_id": "EMS",
                "uid": "DEMO_TOKEN_001",
                "type": "RFID",
                "contract_id": "CONTRACT_12345",
            },
            "auth_method": "AUTH_REQUEST",
            "currency": "USD",
            "total_cost": {"excl_vat": 5.46, "incl_vat": 6.01},
            "total_energy": 18.2,
            "total_time": 52.0,
            "charging_periods": [
                {
                    "start_date_time": "2024-01-15T10:30:00Z",
                    "dimensions": [{"type": "ENERGY", "volume": 18.2}, {"type": "TIME", "volume": 52.0}],
                }
            ],
        }

        self.print_ocpi_message("CPO → EMSP", "/cdrs", cdr_data)

        print("\n📋 CDR Details:")
        print("   • Session Duration: 52 minutes")
        print("   • Energy Consumed: 18.2 kWh")
        print("   • Cost (excl. VAT): $5.46")
        print("   • Cost (incl. VAT): $6.01")
        print("   • Average Rate: $0.30/kWh")

        self.wait_for_user()

        # Step 2: Billing Integration
        self.print_step(2, "Billing Integration", "EMSP processes CDR for customer billing")

        print("\n💳 Billing Process:")
        print("   1. EMSP receives and validates CDR")
        print("   2. Cost calculation verified against tariffs")
        print("   3. Customer account charged")
        print("   4. Invoice generated and sent to customer")
        print("   5. Payment processed")
        print("   6. Settlement with CPO initiated")

        self.wait_for_user()

        print("\n🎉 CDR processing demo completed!")
        print("💡 Key takeaway: CDRs provide detailed billing data for transparent charging costs")

    async def interactive_menu(self):
        """Run interactive menu-driven demo."""
        while True:
            print("\n" + "=" * 60)
            print("🎓 OCPI Educational Demo - Interactive Menu")
            print("=" * 60)
            print("Choose a demo to run:")
            print("  1. Authentication & Credential Exchange")
            print("  2. Location Discovery Workflow")
            print("  3. Token Authorization Flow")
            print("  4. Session Management")
            print("  5. CDR Processing")
            print("  6. Run All Demos")
            print("  0. Exit")
            print("-" * 60)

            try:
                choice = input("Enter your choice (0-6): ").strip()

                if choice == "0":
                    print("👋 Thanks for learning about OCPI!")
                    break
                elif choice == "1":
                    await self.demo_authentication()
                elif choice == "2":
                    await self.demo_location_discovery()
                elif choice == "3":
                    await self.demo_token_authorization()
                elif choice == "4":
                    await self.demo_session_management()
                elif choice == "5":
                    await self.demo_cdr_processing()
                elif choice == "6":
                    await self.run_all_demos()
                else:
                    print("❌ Invalid choice. Please enter 0-6.")

            except KeyboardInterrupt:
                print("\n👋 Demo interrupted by user")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

    async def run_all_demos(self):
        """Run all educational demos in sequence."""
        print("\n🚀 Running all OCPI educational demos...")

        demos = [
            ("Authentication", self.demo_authentication),
            ("Location Discovery", self.demo_location_discovery),
            ("Token Authorization", self.demo_token_authorization),
            ("Session Management", self.demo_session_management),
            ("CDR Processing", self.demo_cdr_processing),
        ]

        for i, (name, demo_func) in enumerate(demos, 1):
            print(f"\n📚 Demo {i}/{len(demos)}: {name}")
            await demo_func()

            if i < len(demos):
                self.wait_for_user("Ready for next demo?")

        print("\n🎉 All demos completed!")
        print("💡 You now understand the key OCPI workflows!")


async def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="OCPI Educational Demo Runner", formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__
    )

    parser.add_argument(
        "demo_type",
        nargs="?",
        default="interactive",
        choices=["all", "authentication", "locations", "tokens", "sessions", "cdrs", "interactive"],
        help="Type of demo to run",
    )

    args = parser.parse_args()

    demo = OCPIEducationalDemo()

    try:
        if args.demo_type == "all":
            await demo.run_all_demos()
        elif args.demo_type == "authentication":
            await demo.demo_authentication()
        elif args.demo_type == "locations":
            await demo.demo_location_discovery()
        elif args.demo_type == "tokens":
            await demo.demo_token_authorization()
        elif args.demo_type == "sessions":
            await demo.demo_session_management()
        elif args.demo_type == "cdrs":
            await demo.demo_cdr_processing()
        else:  # interactive
            await demo.interactive_menu()

    except KeyboardInterrupt:
        print("\n👋 Demo stopped by user")
    except Exception as e:
        print(f"❌ Demo error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
