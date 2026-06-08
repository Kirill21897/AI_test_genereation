from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Any
from datetime import datetime
import uuid


class GenerationInput(BaseModel):
    """Основные праметры для генерации теста"""
    topic: str
    specialty: str
    level: Literal['Junior', 'Middle', 'Senior', "Expert"]
    num_questtions: int = Field(5, ge=3, le=15)


class Question(BaseModel):
    """Один вопрос в тесте"""
    id: str
    type: Literal['MCQ', 'Scenario', 'Calculation', 'Procedure']
    difficulty: Literal['Easy', 'Medium', 'Hard']
    bloom_level: Literal['Remeber', 'Understand', 'Apply', 'Analyze']
    
    question_text: str
    options: Optional(List[str]) = None
    correct_answer: Any
    explanation: str
    distractor_explanations: Optional[List[str]] = None
    
    metadata: dict = Field(default_factory=dict)
    pass


class GeneratedTest():
    """Полный тест - результат работы LLM-core"""
    test_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    topic: str
    specialty: str
    level: str
    duration_minutes: int
    questions: List[Question]
    standarts_covered: List[str] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: dict = Field(default_factory=dict)
    pass