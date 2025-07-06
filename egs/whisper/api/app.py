#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2025- SATURN
# AUTHORS:
# Sukbong Kwon (Galois)

from fastapi import FastAPI
import uvicorn

from api.route import router
from api.config import APP_NAME, DESCRIPTION, VERSION, COMPANY, CONTACT, APP_SYMBOL


# Initialize FastAPI
app = FastAPI(
    title=APP_NAME,
    description=DESCRIPTION,
    version=VERSION,
    contact={
        "name": COMPANY,
        "email": CONTACT,
    },
    docs_url=f"/{APP_SYMBOL}/docs",
    openapi_url=f"/{APP_SYMBOL}/openapi.json",
    servers=[
        {"url": "https://api.magovoice.com", "description": "Production"},
    ]
)

# Include router
app.include_router(router)

# Run server
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=59110,
        # workers=2,
        reload=False,
        log_level="debug",
    )
