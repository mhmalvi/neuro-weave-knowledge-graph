#!/usr/bin/env python3
"""
Health check endpoint for Vercel deployment
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import time

app = FastAPI()

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": int(time.time()),
        "service": "NeuroWeave MCP Server",
        "version": "1.0.0"
    }

# For Vercel
def handler(request):
    from fastapi.responses import JSONResponse
    
    if request.method == "GET":
        return JSONResponse(content=health_check())
    else:
        return JSONResponse(content={"error": "Method not allowed"}, status_code=405)

