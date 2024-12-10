from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Depends, Form
from app.models.user import User
from app.auth.jwt import create_access_token, get_current_user
from app.db.database import sessions_collection,transcriptions_collection, audio_files_collection
from app.models.transcription import SessionCreateResponse, SessionEndRequest, TranscriptionSaveRequest, TranscriptionResponse
from bson import ObjectId
from datetime import datetime, timedelta
import uuid
import os

app = APIRouter()


@app.post("/sessions/create")
async def create_session():
    """Create a new transcription session"""
    session_id = str(uuid.uuid4())
    session_data = {
        "_id": session_id,
        "start_time": datetime.utcnow(),
        "status": "active",
        "final_transcript": None
    }
    sessions_collection.insert_one(session_data)
    return SessionCreateResponse(session_id=session_id)

@app.post("/transcriptions/save")
async def save_transcription(request: TranscriptionSaveRequest):
    """Save a transcription segment"""
    try:
        # Verify session exists
        session = sessions_collection.find_one({"_id": request.session_id})
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        transcription_data = {
            "session_id": request.session_id,
            "text": request.text,
            "is_final": request.is_final,
            "timestamp": datetime.utcnow()
        }
        transcriptions_collection.insert_one(transcription_data)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/notes/daily")
async def get_daily_notes(current_user: User = Depends(get_current_user)):
    """Retrieve daily notes for authenticated user"""
    try:
        # Calculate the timestamp for 24 hours ago
        one_day_ago = datetime.utcnow() - timedelta(days=1)

        # Retrieve transcriptions from the last 24 hours for current user
        daily_notes = await transcriptions_collection.find({
            "user_id": current_user.id,
            "timestamp": {"$gte": one_day_ago},
            "is_final": True  
        }).sort("timestamp", -1).to_list(length=None)

        # Convert MongoDB documents to Pydantic model
        formatted_notes = [
            TranscriptionResponse(
                session_id=note['session_id'],
                text=note['text'],
                timestamp=note['timestamp'],
                is_final=note['is_final']
            ) for note in daily_notes
        ]

        return {
            "total_notes": len(formatted_notes),
            "notes": formatted_notes
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/audio/upload")
async def upload_audio(
    audio: UploadFile = File(...), 
    session_id: str = Form(...)
):
    """Upload audio file for a specific session"""
    try:
        # Verify session exists
        session = sessions_collection.find_one({"_id": session_id})
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        # Create uploads directory if not exists
        os.makedirs('uploads', exist_ok=True)
        
        # Generate unique filename
        file_extension = os.path.splitext(audio.filename)[1]
        filename = f"uploads/{session_id}_{datetime.utcnow().isoformat()}{file_extension}"
        
        # Save file
        with open(filename, "wb") as buffer:
            buffer.write(await audio.read())

        # Save file metadata to MongoDB
        audio_data = {
            "session_id": session_id,
            "filename": filename,
            "uploaded_at": datetime.utcnow()
        }
        audio_files_collection.insert_one(audio_data)

        return {"status": "success", "filename": filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/sessions/{session_id}/end")
async def end_session(
    session_id: str, 
    request: SessionEndRequest
):
    """End a transcription session"""
    try:
        # Update session status
        result = sessions_collection.update_one(
            {"_id": session_id},
            {
                "$set": {
                    "status": "completed", 
                    "end_time": datetime.utcnow(),
                    "final_transcript": request.final_transcript
                }
            }
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Session not found")

        return {"status": "session ended successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
