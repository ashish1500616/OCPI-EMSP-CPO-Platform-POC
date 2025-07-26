"""
EMSP Data Models and Mock Data
==============================

This module provides data models and mock data for the OCPI-compliant EMSP backend.
It includes sample data structures for testing and development purposes.

The mock data includes:
- Sample locations from various CPOs
- Mock charging sessions
- Sample charge detail records (CDRs)
- Tariff information
- Token data
- Command examples
"""

import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List


@dataclass
class MockLocation:
    """Mock location data structure."""

    id: str
    type: str
    name: str
    address: str
    city: str
    postal_code: str
    country: str
    coordinates: Dict[str, float]
    party_id: str
    country_code: str
    publish: bool
    last_updated: str


@dataclass
class MockSession:
    """Mock charging session data structure."""

    id: str
    start_date_time: str
    end_date_time: str
    kwh: float
    cdr_token: Dict[str, str]
    auth_method: str
    authorization_reference: str
    location_id: str
    evse_uid: str
    connector_id: str
    meter_id: str
    currency: str
    status: str
    last_updated: str


@dataclass
class MockCDR:
    """Mock Charge Detail Record data structure."""

    id: str
    start_date_time: str
    end_date_time: str
    session_id: str
    cdr_token: Dict[str, str]
    auth_method: str
    authorization_reference: str
    cdr_location: Dict[str, Any]
    meter_id: str
    currency: str
    total_cost: Dict[str, Any]
    total_energy: float
    total_time: float
    last_updated: str


class MockDataGenerator:
    """Generator for mock OCPI data."""

    @staticmethod
    def generate_locations() -> List[Dict[str, Any]]:
        """Generate mock location data."""
        locations = [
            MockLocation(
                id="LOC001",
                type="ON_STREET",
                name="Downtown Charging Station",
                address="123 Main Street",
                city="San Francisco",
                postal_code="94102",
                country="USA",
                coordinates={"latitude": 37.7749, "longitude": -122.4194},
                party_id="CPO",
                country_code="US",
                publish=True,
                last_updated=datetime.now(timezone.utc).isoformat(),
            ),
            MockLocation(
                id="LOC002",
                type="PARKING_LOT",
                name="Shopping Mall Charging Hub",
                address="456 Commerce Blvd",
                city="Los Angeles",
                postal_code="90210",
                country="USA",
                coordinates={"latitude": 34.0522, "longitude": -118.2437},
                party_id="CPO",
                country_code="US",
                publish=True,
                last_updated=datetime.now(timezone.utc).isoformat(),
            ),
            MockLocation(
                id="LOC003",
                type="HIGHWAY",
                name="Highway Rest Stop Chargers",
                address="789 Highway 101",
                city="San Jose",
                postal_code="95110",
                country="USA",
                coordinates={"latitude": 37.3382, "longitude": -121.8863},
                party_id="CPO",
                country_code="US",
                publish=True,
                last_updated=datetime.now(timezone.utc).isoformat(),
            ),
        ]
        return [asdict(loc) for loc in locations]

    @staticmethod
    def generate_sessions() -> List[Dict[str, Any]]:
        """Generate mock session data."""
        now = datetime.now(timezone.utc)
        sessions = [
            MockSession(
                id="SES001",
                start_date_time=(now - timedelta(hours=2)).isoformat(),
                end_date_time=(now - timedelta(hours=1)).isoformat(),
                kwh=25.5,
                cdr_token={"uid": "TOKEN123", "type": "RFID"},
                auth_method="AUTH_REQUEST",
                authorization_reference="AUTH001",
                location_id="LOC001",
                evse_uid="EVSE001",
                connector_id="CONN001",
                meter_id="METER001",
                currency="USD",
                status="COMPLETED",
                last_updated=now.isoformat(),
            ),
            MockSession(
                id="SES002",
                start_date_time=(now - timedelta(hours=4)).isoformat(),
                end_date_time=(now - timedelta(hours=3)).isoformat(),
                kwh=18.2,
                cdr_token={"uid": "TOKEN456", "type": "RFID"},
                auth_method="AUTH_REQUEST",
                authorization_reference="AUTH002",
                location_id="LOC002",
                evse_uid="EVSE002",
                connector_id="CONN002",
                meter_id="METER002",
                currency="USD",
                status="COMPLETED",
                last_updated=now.isoformat(),
            ),
        ]
        return [asdict(session) for session in sessions]

    @staticmethod
    def generate_cdrs() -> List[Dict[str, Any]]:
        """Generate mock CDR data."""
        now = datetime.now(timezone.utc)
        cdrs = [
            MockCDR(
                id="CDR001",
                start_date_time=(now - timedelta(hours=2)).isoformat(),
                end_date_time=(now - timedelta(hours=1)).isoformat(),
                session_id="SES001",
                cdr_token={"uid": "TOKEN123", "type": "RFID"},
                auth_method="AUTH_REQUEST",
                authorization_reference="AUTH001",
                cdr_location={"id": "LOC001", "name": "Downtown Charging Station", "address": "123 Main Street"},
                meter_id="METER001",
                currency="USD",
                total_cost={"excl_vat": 12.75, "incl_vat": 14.03},
                total_energy=25.5,
                total_time=1.0,
                last_updated=now.isoformat(),
            )
        ]
        return [asdict(cdr) for cdr in cdrs]

    @staticmethod
    def generate_tariffs() -> List[Dict[str, Any]]:
        """Generate mock tariff data."""
        return [
            {
                "id": "TARIFF001",
                "currency": "USD",
                "type": "REGULAR",
                "tariff_alt_text": [{"language": "en", "text": "Standard charging rate"}],
                "tariff_alt_url": "https://example.com/tariff/001",
                "min_price": {"excl_vat": 0.50, "incl_vat": 0.55},
                "max_price": {"excl_vat": 0.75, "incl_vat": 0.83},
                "elements": [{"price_components": [{"type": "ENERGY", "price": 0.30, "vat": 10.0, "step_size": 1}]}],
                "start_date_time": datetime.now(timezone.utc).isoformat(),
                "end_date_time": (datetime.now(timezone.utc) + timedelta(days=365)).isoformat(),
                "energy_mix": {
                    "is_green_energy": True,
                    "energy_sources": [{"source": "SOLAR", "percentage": 60.0}, {"source": "WIND", "percentage": 40.0}],
                },
                "last_updated": datetime.now(timezone.utc).isoformat(),
            }
        ]

    @staticmethod
    def generate_tokens() -> List[Dict[str, Any]]:
        """Generate mock token data."""
        return [
            {
                "uid": "TOKEN123",
                "type": "RFID",
                "auth_id": "AUTH123",
                "visual_number": "1234",
                "issuer": "EMSP_COMPANY",
                "group_id": "GROUP001",
                "valid": True,
                "whitelist": "ALWAYS",
                "language": "en",
                "default_profile_type": "REGULAR",
                "energy_contract": {"supplier_name": "Green Energy Co", "contract_id": "CONTRACT123"},
                "last_updated": datetime.now(timezone.utc).isoformat(),
            },
            {
                "uid": "TOKEN456",
                "type": "RFID",
                "auth_id": "AUTH456",
                "visual_number": "5678",
                "issuer": "EMSP_COMPANY",
                "group_id": "GROUP002",
                "valid": True,
                "whitelist": "ALWAYS",
                "language": "en",
                "default_profile_type": "REGULAR",
                "energy_contract": {"supplier_name": "Clean Power Inc", "contract_id": "CONTRACT456"},
                "last_updated": datetime.now(timezone.utc).isoformat(),
            },
        ]


# Initialize mock data
MOCK_DATA = {
    "locations": MockDataGenerator.generate_locations(),
    "sessions": MockDataGenerator.generate_sessions(),
    "cdrs": MockDataGenerator.generate_cdrs(),
    "tariffs": MockDataGenerator.generate_tariffs(),
    "tokens": MockDataGenerator.generate_tokens(),
    "commands": [],
    "hub_client_info": [],
    "charging_profiles": [],
    "credentials": [],
}


def get_mock_data(module: str) -> List[Dict[str, Any]]:
    """
    Get mock data for a specific module.

    Args:
        module: The module name

    Returns:
        List of mock data objects
    """
    return MOCK_DATA.get(module, [])


def populate_storage_with_mock_data(storage: Dict[str, Dict[str, Any]]) -> None:
    """
    Populate storage with mock data.

    Args:
        storage: The storage dictionary to populate
    """
    for module, data_list in MOCK_DATA.items():
        if module in storage:
            for item in data_list:
                item_id = item.get("id", str(uuid.uuid4()))
                storage[module][item_id] = item
