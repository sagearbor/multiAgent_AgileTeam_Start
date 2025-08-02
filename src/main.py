#!/usr/bin/env python3
"""
Test FastAPI application for multi-agent template.
"""

from fastapi import FastAPI

app = FastAPI(title="Test App", version="1.0.0")

@app.get("/")
def read_root():
    """Root endpoint."""
    return {"message": "Hello World"}

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)