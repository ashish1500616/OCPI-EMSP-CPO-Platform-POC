"""
Test Data Factory for OCPI Objects
==================================

This module provides factories for generating realistic OCPI test data
following the OCPI 2.2.1 specification. It includes factories for all
major OCPI objects used in EMSP-CPO interactions.
"""

import random
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict


class TestDataFactory:
    """Factory for generating OCPI test data objects."""

    def __init__(self):
        """Initialize the test data factory."""
        self.country_codes = ["US", "DE", "NL", "FR", "UK"]
        self.party_ids = ["EMS", "CPO", "BEC", "TNM", "EVN"]
        self.currencies = ["USD", "EUR", "GBP"]

    def generate_id(self, prefix: str = "") -> str:
        """Generate a unique ID with optional prefix."""
        return f"{prefix}{uuid.uuid4().hex[:8]}" if prefix else uuid.uuid4().hex[:12]

    def generate_timestamp(self, offset_hours: int = 0) -> str:
        """Generate ISO timestamp with optional offset."""
        dt = datetime.now(timezone.utc) + timedelta(hours=offset_hours)
        return dt.isoformat().replace("+00:00", "Z")

    def create_location(self, **kwargs) -> Dict[str, Any]:
        """Create a test Location object."""
        defaults = {
            "country_code": random.choice(self.country_codes),
            "party_id": random.choice(self.party_ids),
            "id": self.generate_id("LOC"),
            "publish": True,
            "name": f"Test Charging Station {random.randint(1, 999)}",
            "address": f"{random.randint(100, 9999)} Test Street",
            "city": "Test City",
            "postal_code": f"{random.randint(10000, 99999)}",
            "state": "Test State",
            "country": "USA",
            "coordinates": {
                "latitude": str(round(random.uniform(25.0, 49.0), 6)),
                "longitude": str(round(random.uniform(-125.0, -66.0), 6)),
            },
            "related_locations": [],
            "parking_type": "ON_STREET",
            "evses": [self.create_evse()],
            "directions": [],
            "operator": {"name": "Test Operator"},
            "suboperator": None,
            "owner": None,
            "facilities": ["HOTEL", "RESTAURANT"],
            "time_zone": "America/New_York",
            "opening_times": {"twentyfourseven": True},
            "charging_when_closed": True,
            "images": [],
            "energy_mix": None,
            "last_updated": self.generate_timestamp(),
        }
        defaults.update(kwargs)
        return defaults

    def create_evse(self, **kwargs) -> Dict[str, Any]:
        """Create a test EVSE object."""
        defaults = {
            "uid": self.generate_id("EVSE"),
            "evse_id": f"US*{random.choice(self.party_ids)}*E{random.randint(100000, 999999)}",
            "status": "AVAILABLE",
            "status_schedule": [],
            "capabilities": ["RESERVABLE", "CHARGING_PROFILE_CAPABLE"],
            "connectors": [self.create_connector()],
            "floor_level": None,
            "coordinates": {
                "latitude": str(round(random.uniform(25.0, 49.0), 6)),
                "longitude": str(round(random.uniform(-125.0, -66.0), 6)),
            },
            "physical_reference": f"Bay {random.randint(1, 10)}",
            "directions": [],
            "parking_restrictions": [],
            "images": [],
            "last_updated": self.generate_timestamp(),
        }
        defaults.update(kwargs)
        return defaults

    def create_connector(self, **kwargs) -> Dict[str, Any]:
        """Create a test Connector object."""
        defaults = {
            "id": str(random.randint(1, 4)),
            "standard": "IEC_62196_T2",
            "format": "SOCKET",
            "power_type": "AC_3_PHASE",
            "max_voltage": 400,
            "max_amperage": 32,
            "max_electric_power": 22000,
            "tariff_ids": [self.generate_id("TRF")],
            "terms_and_conditions": None,
            "last_updated": self.generate_timestamp(),
        }
        defaults.update(kwargs)
        return defaults

    def create_session(self, **kwargs) -> Dict[str, Any]:
        """Create a test Session object."""
        start_time = datetime.now(timezone.utc) - timedelta(hours=2)
        defaults = {
            "country_code": random.choice(self.country_codes),
            "party_id": random.choice(self.party_ids),
            "id": self.generate_id("SES"),
            "start_date_time": start_time.isoformat().replace("+00:00", "Z"),
            "end_date_time": None,
            "kwh": round(random.uniform(5.0, 50.0), 3),
            "cdr_token": self.create_cdr_token(),
            "auth_method": "AUTH_REQUEST",
            "authorization_reference": self.generate_id("AUTH"),
            "location_id": self.generate_id("LOC"),
            "evse_uid": self.generate_id("EVSE"),
            "connector_id": "1",
            "meter_id": self.generate_id("MTR"),
            "currency": random.choice(self.currencies),
            "charging_periods": [self.create_charging_period()],
            "total_cost": {
                "excl_vat": round(random.uniform(5.0, 25.0), 2),
                "incl_vat": round(random.uniform(6.0, 30.0), 2),
            },
            "status": "ACTIVE",
            "last_updated": self.generate_timestamp(),
        }
        defaults.update(kwargs)
        return defaults

    def create_cdr_token(self, **kwargs) -> Dict[str, Any]:
        """Create a test CDR Token object."""
        defaults = {
            "country_code": random.choice(self.country_codes),
            "party_id": random.choice(self.party_ids),
            "uid": self.generate_id(),
            "type": "RFID",
            "contract_id": self.generate_id("CNT"),
        }
        defaults.update(kwargs)
        return defaults

    def create_charging_period(self, **kwargs) -> Dict[str, Any]:
        """Create a test Charging Period object."""
        start_time = datetime.now(timezone.utc) - timedelta(hours=1)
        defaults = {
            "start_date_time": start_time.isoformat().replace("+00:00", "Z"),
            "dimensions": [
                {"type": "ENERGY", "volume": round(random.uniform(10.0, 50.0), 3)},
                {"type": "TIME", "volume": round(random.uniform(30.0, 120.0), 1)},
            ],
            "tariff_id": self.generate_id("TRF"),
        }
        defaults.update(kwargs)
        return defaults

    def create_token(self, **kwargs) -> Dict[str, Any]:
        """Create a test Token object."""
        defaults = {
            "country_code": random.choice(self.country_codes),
            "party_id": random.choice(self.party_ids),
            "uid": self.generate_id(),
            "type": "RFID",
            "contract_id": self.generate_id("CNT"),
            "visual_number": f"DF000-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1, 9)}",
            "issuer": "Test Issuer",
            "group_id": f"DF000-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
            "valid": True,
            "whitelist": "ALWAYS",
            "language": "en",
            "default_profile_type": None,
            "energy_contract": None,
            "last_updated": self.generate_timestamp(),
        }
        defaults.update(kwargs)
        return defaults

    def create_command(self, command_type: str = "START_SESSION", **kwargs) -> Dict[str, Any]:
        """Create a test Command object."""
        defaults = {
            "response_url": "https://emsp.example.com/ocpi/emsp/2.2.1/commands/START_SESSION/123",
            "token": self.create_cdr_token(),
            "location_id": self.generate_id("LOC"),
            "evse_uid": self.generate_id("EVSE"),
            "connector_id": "1",
        }

        if command_type == "RESERVE_NOW":
            defaults.update(
                {
                    "reservation_id": self.generate_id("RES"),
                    "expiry_date": self.generate_timestamp(offset_hours=2),
                }
            )
        elif command_type == "CANCEL_RESERVATION":
            defaults.update({"reservation_id": self.generate_id("RES")})
        elif command_type == "UNLOCK_CONNECTOR":
            # Only location_id, evse_uid, connector_id needed
            pass

        defaults.update(kwargs)
        return defaults

    def create_command_response(self, result: str = "ACCEPTED", **kwargs) -> Dict[str, Any]:
        """Create a test Command Response object."""
        defaults = {"result": result, "timeout": 30, "message": []}
        defaults.update(kwargs)
        return defaults

    def create_tariff(self, **kwargs) -> Dict[str, Any]:
        """Create a test Tariff object."""
        defaults = {
            "country_code": random.choice(self.country_codes),
            "party_id": random.choice(self.party_ids),
            "id": self.generate_id("TRF"),
            "currency": random.choice(self.currencies),
            "type": "REGULAR",
            "tariff_alt_text": [],
            "tariff_alt_url": None,
            "min_price": None,
            "max_price": {
                "excl_vat": round(random.uniform(0.50, 2.00), 2),
                "incl_vat": round(random.uniform(0.60, 2.40), 2),
            },
            "elements": [self.create_tariff_element()],
            "start_date_time": None,
            "end_date_time": None,
            "energy_mix": None,
            "last_updated": self.generate_timestamp(),
        }
        defaults.update(kwargs)
        return defaults

    def create_tariff_element(self, **kwargs) -> Dict[str, Any]:
        """Create a test Tariff Element object."""
        defaults = {
            "price_components": [
                {
                    "type": "ENERGY",
                    "price": round(random.uniform(0.20, 0.50), 3),
                    "vat": round(random.uniform(15.0, 25.0), 1),
                    "step_size": 1,
                },
                {
                    "type": "TIME",
                    "price": round(random.uniform(0.05, 0.15), 3),
                    "vat": round(random.uniform(15.0, 25.0), 1),
                    "step_size": 60,
                },
            ],
            "restrictions": None,
        }
        defaults.update(kwargs)
        return defaults

    def create_cdr(self, **kwargs) -> Dict[str, Any]:
        """Create a test CDR (Charge Detail Record) object."""
        start_time = datetime.now(timezone.utc) - timedelta(hours=3)
        end_time = start_time + timedelta(hours=2)
        defaults = {
            "country_code": random.choice(self.country_codes),
            "party_id": random.choice(self.party_ids),
            "id": self.generate_id("CDR"),
            "start_date_time": start_time.isoformat().replace("+00:00", "Z"),
            "end_date_time": end_time.isoformat().replace("+00:00", "Z"),
            "session_id": self.generate_id("SES"),
            "cdr_token": self.create_cdr_token(),
            "auth_method": "AUTH_REQUEST",
            "authorization_reference": self.generate_id("AUTH"),
            "cdr_location": self.create_cdr_location(),
            "meter_id": self.generate_id("MTR"),
            "currency": random.choice(self.currencies),
            "tariffs": [self.create_tariff()],
            "charging_periods": [self.create_charging_period()],
            "signed_data": None,
            "total_cost": {
                "excl_vat": round(random.uniform(10.0, 50.0), 2),
                "incl_vat": round(random.uniform(12.0, 60.0), 2),
            },
            "total_fixed_cost": None,
            "total_energy": round(random.uniform(15.0, 75.0), 3),
            "total_energy_cost": {
                "excl_vat": round(random.uniform(8.0, 40.0), 2),
                "incl_vat": round(random.uniform(10.0, 48.0), 2),
            },
            "total_time": round(random.uniform(60.0, 180.0), 1),
            "total_time_cost": None,
            "total_parking_time": None,
            "total_parking_cost": None,
            "total_reservation_cost": None,
            "remark": "Test CDR",
            "invoice_reference_id": self.generate_id("INV"),
            "credit": False,
            "credit_reference_id": None,
            "last_updated": self.generate_timestamp(),
        }
        defaults.update(kwargs)
        return defaults

    def create_cdr_location(self, **kwargs) -> Dict[str, Any]:
        """Create a test CDR Location object."""
        defaults = {
            "id": self.generate_id("LOC"),
            "name": f"Test Charging Location {random.randint(1, 999)}",
            "address": f"{random.randint(100, 9999)} Test Avenue",
            "city": "Test City",
            "postal_code": f"{random.randint(10000, 99999)}",
            "state": "Test State",
            "country": "USA",
            "coordinates": {
                "latitude": str(round(random.uniform(25.0, 49.0), 6)),
                "longitude": str(round(random.uniform(-125.0, -66.0), 6)),
            },
            "evse_uid": self.generate_id("EVSE"),
            "evse_id": f"US*{random.choice(self.party_ids)}*E{random.randint(100000, 999999)}",
            "connector_id": str(random.randint(1, 4)),
            "connector_standard": "IEC_62196_T2",
            "connector_format": "SOCKET",
            "connector_power_type": "AC_3_PHASE",
        }
        defaults.update(kwargs)
        return defaults
