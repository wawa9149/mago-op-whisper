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
    root_path=f"/{APP_SYMBOL}",
    docs_url=f"/docs",
    openapi_url=f"/openapi.json",
)

# Include router
app.include_router(router)

# CORS to allow all origins
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Run server
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=59005,
        workers=1,
        reload=True,
        log_level="debug",
    )
