"""
OCPI-compliant EMSP (E-Mobility Service Provider) Backend
========================================================

This module provides a complete EMSP implementation using the extrawest_ocpi library
and FastAPI. It supports OCPI version 2.2.1 and includes all required EMSP modules.

Features:
- OCPI 2.2.1 compliance
- EMSP role implementation
- Token-based authentication
- All EMSP modules: locations, sessions, cdrs, tariffs, commands, tokens, hub_client_info, charging_profile
- Production-ready configuration
"""

import uvicorn
from auth import ClientAuthenticator
from config import settings
from crud import EMSPCrud
from fastapi import FastAPI
from py_ocpi import get_application
from py_ocpi.core.enums import ModuleID, RoleEnum
from py_ocpi.modules.versions.enums import VersionNumber


def create_emsp_application() -> FastAPI:
    """
    Create and configure the EMSP FastAPI application.

    Returns:
        FastAPI: Configured EMSP application
    """
    # Define all EMSP modules according to OCPI 2.2.1 specification
    emsp_modules = [
        # Receiver modules (EMSP receives data from CPO)
        ModuleID.locations,  # Location information from CPOs
        ModuleID.sessions,  # Charging session information
        ModuleID.cdrs,  # Charge Detail Records
        ModuleID.tariffs,  # Tariff information
        ModuleID.hub_client_info,  # Hub client information
        ModuleID.credentials_and_registration,  # Credentials and registration
        # Sender modules (EMSP sends data to CPO)
        ModuleID.commands,  # Commands to charging stations
        ModuleID.tokens,  # Token authorization
        ModuleID.charging_profile,  # Charging profile management
    ]

    # Create the OCPI application
    ocpi_app = get_application(
        version_numbers=[VersionNumber.v_2_2_1],
        roles=[RoleEnum.emsp],
        crud=EMSPCrud,
        modules=emsp_modules,
        authenticator=ClientAuthenticator,
        http_push=True,
        websocket_push=False,
    )

    # Mount the OCPI application under the specified prefix
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        debug=settings.DEBUG,
    )
    for route in ocpi_app.routes:
        app.routes.append(route)

    for dependency in ocpi_app.dependency_overrides:
        app.dependency_overrides[dependency] = ocpi_app.dependency_overrides[dependency]

    @app.get("/")
    async def root():
        return {
            "service": "OCPI EMSP Backend",
            "version": settings.VERSION,
            "role": "EMSP",
            "status": "operational",
            "endpoints": {
                "ocpi": f"/{settings.OCPI_PREFIX}",
                "docs": "/docs",
                "redoc": "/redoc",
            },
        }

    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "service": "EMSP Backend", "version": settings.VERSION}

    return app


# Create the application instance
app = create_emsp_application()

# Print all registered routes for debugging
for route in app.routes:
    print(f"Registered route: {route.path}")


if __name__ == "__main__":
    # Run the application with uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True,
    )
