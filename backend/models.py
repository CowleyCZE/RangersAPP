from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://user:password@db/ranger_db"

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User")
    documents = relationship("Document", back_populates="project")
    progress_logs = relationship("ProgressLog", back_populates="project")
    phases = relationship("Phase", back_populates="project")

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    category = Column(String, nullable=True) # New field for category
    project_id = Column(Integer, ForeignKey('projects.id'))

    project = relationship("Project")

class ProgressLog(Base):
    __tablename__ = 'progress_logs'
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    date = Column(String) # For simplicity, store as string for now
    percentage_completed = Column(Integer)
    notes = Column(String)

    project = relationship("Project")

class ExtractedData(Base):
    __tablename__ = 'extracted_data'
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey('documents.id'))
    key = Column(String, index=True)
    value = Column(String)

    document = relationship("Document")

class Phase(Base):
    __tablename__ = 'phases'
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    name = Column(String, index=True)
    description = Column(String, nullable=True)

    project = relationship("Project", back_populates="phases")
    tasks = relationship("Task", back_populates="phase")

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    phase_id = Column(Integer, ForeignKey('phases.id'))
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    status = Column(String, default="pending") # e.g., pending, in_progress, completed

    phase = relationship("Phase", back_populates="tasks")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
