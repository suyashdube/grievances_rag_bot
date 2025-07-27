from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db, Grievance, create_tables
from typing import Optional
import random

app = FastAPI(title="Grievance Management API")

# Create tables on startup
create_tables()

class GrievanceCreate(BaseModel):
    name: str
    mobile: str
    complaint_details: str

class GrievanceResponse(BaseModel):
    id: int
    message: str

class StatusResponse(BaseModel):
    complaint_id: int
    name: str
    mobile: str
    complaint_details: str
    status: str
    created_at: str

@app.post("/register_complaint", response_model=GrievanceResponse)
def register_complaint(grievance: GrievanceCreate, db: Session = Depends(get_db)):
    """Register a new grievance"""
    db_grievance = Grievance(
        name=grievance.name,
        mobile=grievance.mobile,
        complaint_details=grievance.complaint_details
    )
    db.add(db_grievance)
    db.commit()
    db.refresh(db_grievance)
    
    return GrievanceResponse(
        id=db_grievance.id,
        message=f"Complaint registered successfully with ID: {db_grievance.id}"
    )

@app.get("/complaint_status/{complaint_id}", response_model=StatusResponse)
def get_complaint_status(complaint_id: int, db: Session = Depends(get_db)):
    """Get complaint status by ID"""
    grievance = db.query(Grievance).filter(Grievance.id == complaint_id).first()
    if not grievance:
        raise HTTPException(status_code=404, detail="Complaint not found")
    
    # Simulate status progression
    statuses = ["Registered", "In Progress", "Under Review", "Resolved", "Closed"]
    if grievance.status == "Registered":
        grievance.status = random.choice(["In Progress", "Under Review"])
        db.commit()
    
    return StatusResponse(
        complaint_id=grievance.id,
        name=grievance.name,
        mobile=grievance.mobile,
        complaint_details=grievance.complaint_details,
        status=grievance.status,
        created_at=grievance.created_at.strftime("%Y-%m-%d %H:%M:%S")
    )

@app.get("/complaint_status_by_mobile/{mobile}")
def get_complaint_by_mobile(mobile: str, db: Session = Depends(get_db)):
    """Get latest complaint status by mobile number"""
    grievance = db.query(Grievance).filter(
        Grievance.mobile == mobile
    ).order_by(Grievance.created_at.desc()).first()
    
    if not grievance:
        raise HTTPException(status_code=404, detail="No complaints found for this mobile number")
    
    return StatusResponse(
        complaint_id=grievance.id,
        name=grievance.name,
        mobile=grievance.mobile,
        complaint_details=grievance.complaint_details,
        status=grievance.status,
        created_at=grievance.created_at.strftime("%Y-%m-%d %H:%M:%S")
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 