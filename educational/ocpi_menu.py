#!/usr/bin/env python3
"""
OCPI EMSP-CPO Interactive Menu System
=====================================

A comprehensive menu-driven interface for exploring OCPI concepts,
running tests, and managing the demo environment.

🎯 Features:
- Interactive menu system
- Educational explanations
- Test execution with explanations
- Environment management
- Troubleshooting guidance

Usage:
    python ocpi_menu.py
"""

import asyncio
import os
import subprocess
import sys
import time
from typing import Optional, List, Dict, Any
import httpx


class OCPIMenuSystem:
    """Interactive menu system for OCPI learning and testing."""
    
    def __init__(self):
        self.emsp_port = 8000
        self.cpo_port = 8001
        self.services_running = False
        
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def print_header(self):
        """Print the main header."""
        print("🚗⚡ OCPI EMSP-CPO Learning Environment")
        print("=" * 60)
        print("📚 Open Charge Point Interface (OCPI) 2.2.1 Demo")
        print("🎯 Learn EV charging ecosystem communication")
        print("=" * 60)
        
    def print_menu(self, title: str, options: List[str], back_option: bool = True):
        """Print a formatted menu."""
        print(f"\n📋 {title}")
        print("-" * 50)
        
        for i, option in enumerate(options, 1):
            print(f"  {i}. {option}")
            
        if back_option:
            print(f"  0. Back to Main Menu")
        else:
            print(f"  0. Exit")
            
        print("-" * 50)
        
    def get_user_choice(self, max_choice: int) -> int:
        """Get and validate user choice."""
        while True:
            try:
                choice = input(f"Enter your choice (0-{max_choice}): ").strip()
                choice_int = int(choice)
                if 0 <= choice_int <= max_choice:
                    return choice_int
                else:
                    print(f"❌ Please enter a number between 0 and {max_choice}")
            except ValueError:
                print("❌ Please enter a valid number")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                sys.exit(0)
                
    def wait_for_user(self, message: str = "Press Enter to continue..."):
        """Wait for user input."""
        try:
            input(f"\n⏸️  {message}")
        except KeyboardInterrupt:
            print("\n👋 Returning to menu...")
            
    async def check_services_status(self) -> Dict[str, bool]:
        """Check if EMSP and CPO services are running."""
        status = {"emsp": False, "cpo": False}
        
        async with httpx.AsyncClient(timeout=2.0) as client:
            # Check EMSP
            try:
                response = await client.get(f"http://localhost:{self.emsp_port}/")
                status["emsp"] = response.status_code == 200
            except:
                status["emsp"] = False
                
            # Check CPO
            try:
                response = await client.get(f"http://localhost:{self.cpo_port}/")
                status["cpo"] = response.status_code == 200
            except:
                status["cpo"] = False
                
        self.services_running = status["emsp"] and status["cpo"]
        return status
        
    def print_service_status(self, status: Dict[str, bool]):
        """Print service status."""
        print("\n🔍 Service Status:")
        emsp_status = "🟢 Running" if status["emsp"] else "🔴 Stopped"
        cpo_status = "🟢 Running" if status["cpo"] else "🔴 Stopped"
        
        print(f"   📱 EMSP Backend (:{self.emsp_port}): {emsp_status}")
        print(f"   🔌 Mock CPO Server (:{self.cpo_port}): {cpo_status}")
        
        if not (status["emsp"] and status["cpo"]):
            print("\n💡 To start services: python start_ocpi_demo.py")
            
    async def main_menu(self):
        """Display and handle main menu."""
        while True:
            self.clear_screen()
            self.print_header()
            
            # Check service status
            status = await self.check_services_status()
            self.print_service_status(status)
            
            options = [
                "🎓 Educational Demos (Learn OCPI Concepts)",
                "🧪 Run Tests (Validate Implementation)",
                "🚀 Environment Management (Start/Stop Services)",
                "📊 API Documentation & Endpoints",
                "🔧 Troubleshooting & Help",
                "📚 OCPI Learning Resources"
            ]
            
            self.print_menu("Main Menu", options, back_option=False)
            choice = self.get_user_choice(len(options))
            
            if choice == 0:
                print("👋 Thanks for learning about OCPI!")
                break
            elif choice == 1:
                await self.educational_menu()
            elif choice == 2:
                await self.testing_menu()
            elif choice == 3:
                await self.environment_menu()
            elif choice == 4:
                await self.documentation_menu()
            elif choice == 5:
                await self.troubleshooting_menu()
            elif choice == 6:
                await self.learning_resources_menu()
                
    async def educational_menu(self):
        """Educational demos menu."""
        while True:
            self.clear_screen()
            print("🎓 OCPI Educational Demos")
            print("=" * 50)
            print("Learn OCPI concepts through interactive demonstrations")
            
            if not self.services_running:
                print("\n⚠️  Services not running. Some demos may not work.")
                print("💡 Start services from Environment Management menu")
                
            options = [
                "🔐 Authentication & Credential Exchange",
                "📍 Location Discovery (Charging Stations)",
                "🎫 Token Authorization (User Validation)",
                "⚡ Session Management (Start/Stop Charging)",
                "💳 CDR Processing (Billing Records)",
                "🎯 Interactive Step-by-Step Demo",
                "🚀 Run All Demos in Sequence"
            ]
            
            self.print_menu("Educational Demos", options)
            choice = self.get_user_choice(len(options))
            
            if choice == 0:
                break
            elif choice == 1:
                await self.run_educational_demo("authentication")
            elif choice == 2:
                await self.run_educational_demo("locations")
            elif choice == 3:
                await self.run_educational_demo("tokens")
            elif choice == 4:
                await self.run_educational_demo("sessions")
            elif choice == 5:
                await self.run_educational_demo("cdrs")
            elif choice == 6:
                await self.run_educational_demo("interactive")
            elif choice == 7:
                await self.run_educational_demo("all")
                
    async def testing_menu(self):
        """Testing menu."""
        while True:
            self.clear_screen()
            print("🧪 OCPI Testing Suite")
            print("=" * 50)
            print("Validate OCPI implementation with comprehensive tests")
            
            options = [
                "🔧 Unit Tests (Individual Components)",
                "🔄 Integration Tests (EMSP-CPO Interactions)",
                "✅ Compliance Tests (OCPI 2.2.1 Specification)",
                "⚡ Performance Tests (Load & Scalability)",
                "🎯 Quick Test Suite (Unit + Integration)",
                "📊 Generate Test Reports",
                "🔍 Test Framework Validation"
            ]
            
            self.print_menu("Testing Options", options)
            choice = self.get_user_choice(len(options))
            
            if choice == 0:
                break
            elif choice == 1:
                await self.run_tests("unit")
            elif choice == 2:
                await self.run_tests("integration")
            elif choice == 3:
                await self.run_tests("compliance")
            elif choice == 4:
                await self.run_tests("performance")
            elif choice == 5:
                await self.run_tests("quick")
            elif choice == 6:
                await self.show_test_reports()
            elif choice == 7:
                await self.validate_test_framework()
                
    async def environment_menu(self):
        """Environment management menu."""
        while True:
            self.clear_screen()
            print("🚀 Environment Management")
            print("=" * 50)
            print("Manage OCPI demo services and environment")
            
            status = await self.check_services_status()
            self.print_service_status(status)
            
            options = [
                "🚀 Start Complete Demo Environment",
                "📱 Start EMSP Backend Only",
                "🔌 Start Mock CPO Server Only",
                "🛑 Stop All Services",
                "🔍 Check Service Health",
                "📋 View Service Logs",
                "⚙️  Environment Configuration"
            ]
            
            self.print_menu("Environment Options", options)
            choice = self.get_user_choice(len(options))
            
            if choice == 0:
                break
            elif choice == 1:
                await self.start_services("both")
            elif choice == 2:
                await self.start_services("emsp")
            elif choice == 3:
                await self.start_services("cpo")
            elif choice == 4:
                await self.stop_services()
            elif choice == 5:
                await self.check_service_health()
            elif choice == 6:
                await self.view_service_logs()
            elif choice == 7:
                await self.show_configuration()
                
    async def documentation_menu(self):
        """API documentation menu."""
        self.clear_screen()
        print("📊 API Documentation & Endpoints")
        print("=" * 50)
        
        print("\n🌐 Available API Documentation:")
        print(f"   📱 EMSP Backend: http://localhost:{self.emsp_port}/docs")
        print(f"   🔌 Mock CPO Server: http://localhost:{self.cpo_port}/docs")
        
        print("\n📋 Key OCPI Endpoints:")
        print("   EMSP Endpoints:")
        print(f"   • Versions: http://localhost:{self.emsp_port}/ocpi/emsp/2.2.1/versions")
        print(f"   • Locations: http://localhost:{self.emsp_port}/ocpi/emsp/2.2.1/locations")
        print(f"   • Sessions: http://localhost:{self.emsp_port}/ocpi/emsp/2.2.1/sessions")
        print(f"   • Commands: http://localhost:{self.emsp_port}/ocpi/emsp/2.2.1/commands")
        
        print("\n   CPO Endpoints:")
        print(f"   • Versions: http://localhost:{self.cpo_port}/ocpi/cpo/2.2.1/versions")
        print(f"   • Locations: http://localhost:{self.cpo_port}/ocpi/cpo/2.2.1/locations")
        print(f"   • Tokens: http://localhost:{self.cpo_port}/ocpi/cpo/2.2.1/tokens")
        
        print("\n💡 Authentication Headers:")
        print("   EMSP: Authorization: Token emsp_token_a_12345")
        print("   CPO:  Authorization: Token cpo_token_c_abcdef")
        
        self.wait_for_user()
        
    async def troubleshooting_menu(self):
        """Troubleshooting and help menu."""
        self.clear_screen()
        print("🔧 Troubleshooting & Help")
        print("=" * 50)
        
        print("\n🚨 Common Issues & Solutions:")
        print("\n1. Services won't start:")
        print("   • Check if ports 8000/8001 are in use: lsof -i :8000")
        print("   • Kill existing processes: kill -9 <PID>")
        print("   • Install dependencies: pipenv install")
        
        print("\n2. Import errors:")
        print("   • Ensure you're in project root directory")
        print("   • Install dependencies: pipenv install")
        print("   • Check Python version: python --version (3.9+ required)")
        
        print("\n3. Test failures:")
        print("   • Ensure services are running")
        print("   • Check authentication tokens")
        print("   • Run validation: python test_framework_validation.py")
        
        print("\n4. Connection errors:")
        print("   • Verify service URLs and ports")
        print("   • Check firewall settings")
        print("   • Ensure services are healthy")
        
        print("\n📚 Getting Help:")
        print("   • Check logs: tail -f ocpi_demo.log")
        print("   • Run validation: python test_framework_validation.py")
        print("   • View test reports: tests/reports/report.html")
        
        self.wait_for_user()
        
    async def learning_resources_menu(self):
        """Learning resources menu."""
        self.clear_screen()
        print("📚 OCPI Learning Resources")
        print("=" * 50)
        
        print("\n📖 Official OCPI Resources:")
        print("   • OCPI 2.2.1 Specification: https://evroaming.org/")
        print("   • OCPI GitHub: https://github.com/ocpi/ocpi")
        print("   • EVRoaming Foundation: https://evroaming.org/")
        
        print("\n🎓 Key OCPI Concepts:")
        print("   • EMSP: E-Mobility Service Provider (charging apps/services)")
        print("   • CPO: Charge Point Operator (charging station operators)")
        print("   • MSP: Mobility Service Provider (roaming services)")
        print("   • Token: User authentication credential (RFID, app)")
        print("   • CDR: Charge Detail Record (billing information)")
        print("   • Location: Charging station with EVSEs and connectors")
        
        print("\n🔄 OCPI Message Flow:")
        print("   1. Credential Exchange (establish trust)")
        print("   2. Location Discovery (find charging stations)")
        print("   3. Token Authorization (validate users)")
        print("   4. Session Management (control charging)")
        print("   5. CDR Exchange (billing information)")
        
        print("\n🛠️  Technical Details:")
        print("   • Protocol: REST API over HTTPS")
        print("   • Authentication: Token-based")
        print("   • Data Format: JSON")
        print("   • Version: 2.2.1 (latest stable)")
        
        self.wait_for_user()
        
    async def run_educational_demo(self, demo_type: str):
        """Run educational demo."""
        print(f"\n🚀 Starting {demo_type} demo...")
        
        try:
            if os.path.exists("Pipfile"):
                cmd = ["pipenv", "run", "python", "ocpi_educational_demo.py", demo_type]
            else:
                cmd = ["python", "ocpi_educational_demo.py", demo_type]
                
            process = subprocess.run(cmd, check=False)
            
            if process.returncode == 0:
                print("✅ Demo completed successfully!")
            else:
                print("⚠️  Demo completed with warnings")
                
        except Exception as e:
            print(f"❌ Error running demo: {e}")
            
        self.wait_for_user()
        
    async def run_tests(self, test_type: str):
        """Run tests with explanations."""
        print(f"\n🧪 Running {test_type} tests...")
        print(f"📚 {test_type.title()} tests validate:")
        
        explanations = {
            "unit": "Individual component functionality and authentication",
            "integration": "End-to-end EMSP-CPO communication flows",
            "compliance": "OCPI 2.2.1 specification adherence",
            "performance": "System performance under load",
            "quick": "Essential functionality (unit + integration)"
        }
        
        print(f"   • {explanations.get(test_type, 'System functionality')}")
        
        try:
            if os.path.exists("Pipfile"):
                cmd = ["pipenv", "run", "python", "run_tests.py", test_type, "--verbose"]
            else:
                cmd = ["python", "run_tests.py", test_type, "--verbose"]
                
            process = subprocess.run(cmd, check=False)
            
            if process.returncode == 0:
                print("✅ All tests passed!")
            else:
                print("❌ Some tests failed. Check reports for details.")
                
        except Exception as e:
            print(f"❌ Error running tests: {e}")
            
        self.wait_for_user()
        
    async def start_services(self, service_type: str):
        """Start services."""
        print(f"\n🚀 Starting {service_type} service(s)...")
        
        try:
            cmd = ["python", "start_ocpi_demo.py"]
            
            if service_type == "emsp":
                cmd.append("--cpo-only")
            elif service_type == "cpo":
                cmd.append("--emsp-only")
                
            print("💡 Services will start in background...")
            print("💡 Use 'Check Service Health' to verify status")
            
            # Start in background
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            print("✅ Service startup initiated!")
            
        except Exception as e:
            print(f"❌ Error starting services: {e}")
            
        self.wait_for_user()
        
    async def stop_services(self):
        """Stop services."""
        print("\n🛑 Stopping services...")
        
        try:
            # Kill processes on ports
            for port in [self.emsp_port, self.cpo_port]:
                subprocess.run(f"lsof -ti:{port} | xargs kill -9", 
                             shell=True, check=False, 
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                             
            print("✅ Services stopped!")
            
        except Exception as e:
            print(f"❌ Error stopping services: {e}")
            
        self.wait_for_user()
        
    async def check_service_health(self):
        """Check service health."""
        print("\n🔍 Checking service health...")
        
        status = await self.check_services_status()
        self.print_service_status(status)
        
        if status["emsp"] and status["cpo"]:
            print("\n✅ All services are healthy!")
        else:
            print("\n⚠️  Some services are not responding")
            print("💡 Try restarting services from Environment Management")
            
        self.wait_for_user()
        
    async def show_test_reports(self):
        """Show test reports."""
        print("\n📊 Test Reports")
        print("=" * 30)
        
        report_files = [
            ("HTML Report", "tests/reports/report.html"),
            ("Coverage Report", "tests/reports/coverage/index.html"),
            ("JUnit XML", "tests/reports/junit.xml"),
            ("Coverage XML", "tests/reports/coverage.xml")
        ]
        
        for name, path in report_files:
            if os.path.exists(path):
                print(f"✅ {name}: {path}")
            else:
                print(f"❌ {name}: Not found")
                
        print("\n💡 Run tests first to generate reports")
        self.wait_for_user()
        
    async def validate_test_framework(self):
        """Validate test framework."""
        print("\n🔍 Validating test framework...")
        
        try:
            if os.path.exists("Pipfile"):
                cmd = ["pipenv", "run", "python", "test_framework_validation.py"]
            else:
                cmd = ["python", "test_framework_validation.py"]
                
            process = subprocess.run(cmd, check=False)
            
            if process.returncode == 0:
                print("✅ Test framework validation passed!")
            else:
                print("❌ Test framework validation failed")
                
        except Exception as e:
            print(f"❌ Error validating framework: {e}")
            
        self.wait_for_user()
        
    async def view_service_logs(self):
        """View service logs."""
        print("\n📋 Service Logs")
        print("=" * 30)
        
        log_files = ["ocpi_demo.log", "emsp.log", "cpo.log"]
        
        for log_file in log_files:
            if os.path.exists(log_file):
                print(f"\n📄 {log_file}:")
                try:
                    with open(log_file, 'r') as f:
                        lines = f.readlines()
                        # Show last 10 lines
                        for line in lines[-10:]:
                            print(f"   {line.strip()}")
                except Exception as e:
                    print(f"   Error reading log: {e}")
            else:
                print(f"❌ {log_file}: Not found")
                
        self.wait_for_user()
        
    async def show_configuration(self):
        """Show environment configuration."""
        print("\n⚙️  Environment Configuration")
        print("=" * 40)
        
        print(f"🌐 Service Ports:")
        print(f"   • EMSP Backend: {self.emsp_port}")
        print(f"   • Mock CPO Server: {self.cpo_port}")
        
        print(f"\n🔐 Authentication Tokens:")
        print(f"   • EMSP Token A: emsp_token_a_12345")
        print(f"   • CPO Token C: cpo_token_c_abcdef")
        
        print(f"\n📁 Key Files:")
        print(f"   • Main App: main.py")
        print(f"   • Mock CPO: tests/mock_cpo_server.py")
        print(f"   • Tests: tests/")
        print(f"   • Reports: tests/reports/")
        
        print(f"\n🐍 Python Environment:")
        print(f"   • Python: {sys.version}")
        print(f"   • Working Dir: {os.getcwd()}")
        print(f"   • Pipenv: {'Available' if os.path.exists('Pipfile') else 'Not found'}")
        
        self.wait_for_user()


async def main():
    """Main entry point."""
    menu = OCPIMenuSystem()
    
    try:
        await menu.main_menu()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Menu system error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
