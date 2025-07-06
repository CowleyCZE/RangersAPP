from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext
from .data_extraction import extract_key_data_from_text

# --- Hesla a uživatelé ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role or "user"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

from minio import Minio
import pytesseract
from PIL import Image
from io import BytesIO
import spacy
import cv2
import numpy as np
from PyPDF2 import PdfReader
from openpyxl import load_workbook

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_xlsx(file_bytes: bytes) -> str:
    workbook = load_workbook(BytesIO(file_bytes))
    text = ""
    for sheet_name in workbook.sheetnames:
        sheet = workbook[sheet_name]
        for row in sheet.iter_rows():
            for cell in row:
                if cell.value:
                    text += str(cell.value) + " "
    return text

def count_aisles_in_image(document_id: int, minio_client: Minio):
    # This is a placeholder for actual aisle counting logic.
    # In a real scenario, you would use advanced Computer Vision techniques
    # to identify and count aisles in the image.
    # For demonstration, we'll return a simulated number.

    # Simulate loading image (though not strictly necessary for a simulation)
    bucket_name = "ranger-bucket"
    try:
        # In a real scenario, process image_bytes with OpenCV to count aisles

        # Simulate a random number of aisles for demonstration
        import random
        num_aisles = random.randint(1, 10) # Simulate between 1 and 10 aisles
        return {"num_aisles": num_aisles, "message": f"Simulovaný počet uliček: {num_aisles}"}

    except Exception as e:
        print(f"Error during aisle counting: {e}")
        return {"num_aisles": 0, "message": f"Chyba při počítání uliček: {str(e)}"}

def perform_ocr_on_document(db: Session, document_id: int, minio_client: Minio):
    db_document = db.query(models.Document).filter(models.Document.id == document_id).first()
    if not db_document:
        return None, None

    bucket_name = "ranger-bucket"
    try:
        response = minio_client.get_object(bucket_name, db_document.filename)
        file_bytes = response.read()

        text = ""
        if db_document.filename.lower().endswith('.pdf'):
            text = extract_text_from_pdf(file_bytes)
        elif db_document.filename.lower().endswith('.xlsx'):
            text = extract_text_from_xlsx(file_bytes)
        elif db_document.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image = Image.open(BytesIO(file_bytes))
            text = pytesseract.image_to_string(image)
        else:
            return None, None # Unsupported file type for text extraction

        extracted_data = extract_key_data_from_text(text)

        # Store extracted data in the database
        for item in extracted_data:
            db_extracted_data = models.ExtractedData(document_id=document_id, key=item["label"], value=item["text"])
            db.add(db_extracted_data)
        db.commit()

        return text, extracted_data
    except Exception as e:
        print(f"Error performing OCR/data extraction: {e}")
        return None, None

def create_phase(db: Session, phase: schemas.PhaseCreate, project_id: int):
    db_phase = models.Phase(**phase.dict(), project_id=project_id)
    db.add(db_phase)
    db.commit()
    db.refresh(db_phase)
    return db_phase

def get_phase(db: Session, phase_id: int):
    return db.query(models.Phase).filter(models.Phase.id == phase_id).first()

def update_phase(db: Session, phase_id: int, phase: schemas.PhaseCreate):
    db_phase = db.query(models.Phase).filter(models.Phase.id == phase_id).first()
    if db_phase:
        db_phase.name = phase.name
        db_phase.description = phase.description
        db.commit()
        db.refresh(db_phase)
    return db_phase

def delete_phase(db: Session, phase_id: int):
    db_phase = db.query(models.Phase).filter(models.Phase.id == phase_id).first()
    if db_phase:
        db.delete(db_phase)
        db.commit()
    return db_phase

def create_task(db: Session, task: schemas.TaskCreate, phase_id: int):
    db_task = models.Task(**task.dict(), phase_id=phase_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def update_task(db: Session, task_id: int, task: schemas.TaskCreate):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        db_task.name = task.name
        db_task.description = task.description
        db_task.status = task.status
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task