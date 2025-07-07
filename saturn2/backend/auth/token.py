#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2025- SATURN
# AUTHORS:
# Sukbong Kwon (Galois)

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

API_TOKENS = [
    "token-temp",
]

auth_scheme = HTTPBearer()

async def api_token(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    if credentials.credentials not in API_TOKENS:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)