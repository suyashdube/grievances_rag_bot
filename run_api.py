import uvicorn

if __name__ == "__main__":
    print("🚀 Starting Grievance Management API...")
    print("📊 API Documentation will be available at: http://localhost:8000/docs")
    print("🔄 Health check endpoint: http://localhost:8000/")
    print("⏳ Starting server... Press Ctrl+C to stop")
    
    uvicorn.run(
        "api:app",  # Use import string instead of app object
        host="0.0.0.0", 
        port=8000,
        reload=True,
        log_level="info"
    ) 