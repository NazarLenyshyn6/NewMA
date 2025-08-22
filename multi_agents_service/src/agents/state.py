"""..."""

from uuid import UUID
from typing import Deque, Optional, List, Literal, Dict

from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy.orm import Session

dependencies = dependencies = [
    "numpy",  # import numpy as np
    "pandas",  # import pandas as pd
    "scipy",  # import scipy
    "sklearn",  # from sklearn import ...
    "statsmodels.api",  # import statsmodels.api as sm
    "joblib",  # import joblib
    "torch",  # import torch
    "torchvision",
    "lightgbm",
    "xgboost",
    "optuna",
    "sentence_transformers",
    "gensim==4.3.2",
    # "matplotlib.pyplot",  # import matplotlib.pyplot as plt
    "seaborn",  # import seaborn as sns
    "plotly.express",  # import plotly.express as px
    "nltk",  # import nltk
    "spacy",  # import spacy
    "tqdm",  # from tqdm import tqdm
    "networkx",  # import networkx as nx
]

default_conversation_memory = [
    {
        "question": "",
        "answer": "",
    }
]


class AgentState(BaseModel):
    """..."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    # Metadata
    question: str
    db: Session
    user_id: int
    file_name: str
    session_id: UUID
    storage_uri: str
    dataset_summary: str

    # Memory
    conversation_summary_memory: Optional[str] = None
    conversation_memory: Optional[List[Dict]] = Field(
        default=default_conversation_memory
    )
    code_summary_memory: Optional[str] = None
    variables_memory: Optional[dict] = None

    # Store which branch follow
    request_type: Optional[Literal["SUGGESTION", "ACTION"]] = None

    # Subtasks to sovle user question, controls loop stop condition
    subtasks: Optional[Deque[str]] = None

    # Store what was planned to do then referec in reporting
    execution_plan: Optional[str] = None

    # Store what will be code to naswer subtask code or image
    code_mode: Optional[Literal["VISUALIZATION", "CODE"]] = None

    # Code generated for execution
    code: Optional[str] = None

    # Error happend during execution, if one
    code_error: Optional[str] = None

    # Analysis report we get if in code mode and exeuction secessfull
    analysis_report: Optional[List] = None
    image: Optional[str] = None

    # Suggestion propbly will be removed
    suggestion: Optional[str] = None

    # Report
    report: Optional[str] = None

    # Recursion stop condifition for code debagging
    max_code_debagging_attempts: int = 5
    current_code_debagging_attempt: int = 1

    # Libraries to execute code
    dependencies: List[str] = Field(default=dependencies)
