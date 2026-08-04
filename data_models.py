from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal

class CodePair(BaseModel):
    """The two versions of the code we compare."""
    wrong_code: str
    fixed_code: str
    language: str = "python"

class MistakeEval(BaseModel):
    """Is the change a real logic mistake? (Stage 2)"""
    is_real_mistake: bool
    reason: str

class ReasoningHypothesis(BaseModel):
    """What was the developer probably thinking? (Stage 3)"""
    mistake_type: str = Field(description="e.g. 'resource lifecycle', 'type confusion'")
    hypothesized_reasoning: str
    confidence: Literal["inferred"] = "inferred"

class CorrectReasoning(BaseModel):
    """Why the fixed version is correct. (Stage 4)"""
    correct_reasoning: str

class DivergencePoint(BaseModel):
    """The exact moment the two reasoning paths split. (Stage 5)"""
    divergence_point: str

class MemoryNode(BaseModel):
    """The thing we store for future learning. (Stage 6)"""
    mistake_type: str = "unknown"
    divergence_point: str
    confidence: str = "inferred"
    language: str = "python"
    tags: list[str] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())