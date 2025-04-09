from fastapi import FastAPI

# Create FastAPI application - making sure it's at module level
app = FastAPI(
    title="Law Assistant API",
    description="API for legal assistance and document processing",
    version="0.1.0"
)

@app.get("/")
async def root():
    """Root endpoint that returns a welcome message."""
    return {"message": "Welcome to Law Assistant API"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

# Add this if you need to run the app directly from this file
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
