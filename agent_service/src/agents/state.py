"""
Agent State Management Module

This module defines the `AgentState` model, which encapsulates the current state of
a machine learning / data analysis assistant agent. It is responsible for:

- Tracking session- and user-specific context.
- Storing metadata about datasets, files, and dependencies.
- Maintaining summaries for analysis, visualization, code, and user preferences.
- Managing subtasks, task flows, and agent execution modes.
- Capturing action plans, execution artifacts, and debugging progress.

The `AgentState` serves as a central structure that enables consistent state
management across ML, data analysis, visualization, and advisory workflows.
"""

from uuid import UUID
from typing import Optional, List, Dict, Literal, Deque

from pydantic import BaseModel, ConfigDict, Field
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
    "matplotlib.pyplot",  # import matplotlib.pyplot as plt
    "seaborn",  # import seaborn as sns
    "plotly.express",  # import plotly.express as px
    "nltk",  # import nltk
    "spacy",  # import spacy
    "tqdm",  # from tqdm import tqdm
    "networkx",  # import networkx as nx
]


class AgentState(BaseModel):
    """
    Represents the state of an analysis/ML agent session.

    This model is used to maintain context about the user, active dataset,
    task progression, and execution artifacts. It enables continuity across
    multiple subtasks (e.g., analysis, visualization, debugging) within a
    session and provides summaries that can be surfaced to the user.

    Attributes:
        question (str): The latest user question or instruction.
        db (Session): SQLAlchemy database session used for persistence.
        user_id (int): Identifier of the current user.
        session_id (UUID): Unique identifier of the active session.
        file_name (str): Name of the dataset or file being analyzed.
        storage_uri (str): URI for persistent dataset/file storage.
        dataset_summary (str): Textual summary of the dataset.
        dependencies (List[str]): List of dependencies relevant to analysis.

        analysis_summary (Optional[str]): Summary of analysis steps performed.
        visualization_summary (Optional[str]): Summary of visualizations created.
        code_summary (Optional[str]): Summary of code generated.
        user_preferences_summary (Optional[str]): Summary of user preferences.
        variables (Optional[Dict]): Dictionary of variables in the current session.

        new_conversation (List[Dict]): Log of the current conversation turn
            (question and answer pairs).

        agent_mode (Optional[Literal["TECHNICAL", "QUICK"]]): Execution mode of the agent.
        task_flow (Optional[Literal["ADVISORY", "EXPLORATORY"]]): Overall task flow type.
        subtasks (Optional[Deque[str]]): Queue of subtasks to be executed.
        subtask_flow (Optional[Literal["ANALYSIS", "VISUALIZATION", "DIRECT_RESPONSE"]]):
            Current subtask flow category.

        analysis_action_plan (Optional[str]): Planned steps for analysis execution.
        visualization_action_plan (Optional[str]): Planned steps for visualization execution.

        code (Optional[str]): Generated code snippet.
        error_message (Optional[str]): Error message if code execution fails.

        max_debugging_attempts (int): Maximum retries allowed for debugging.
        current_debugging_attempt (int): Number of debugging attempts made so far.

        analysis_report (Optional[List]): Detailed report of the analysis.
        visualization (Optional[str]): Visualization artifact or representation.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    # --------------------
    question: str
    db: Session
    user_id: int
    session_id: UUID
    file_name: str
    storage_uri: str
    dataset_summary: str
    dependencies: List[str] = Field(default=dependencies)

    # --------------------
    analysis_summary: Optional[str] = Field(default=None)
    visualization_summary: Optional[str] = Field(default=None)
    code_summary: Optional[str] = Field(default=None)
    user_preferences_summary: Optional[str] = Field(default=None)
    variables: Optional[Dict] = Field(default=None)

    # --------------------
    new_conversation: List[Dict] = Field(
        default=[
            {
                "question": "",
                "answer": "",
            }
        ]
    )

    # --------------------
    agent_mode: Optional[Literal["TECHNICAL", "QUICK"]] = Field(default=None)
    task_flow: Optional[Literal["ADVISORY", "EXPLORATORY"]] = Field(default=None)
    subtasks: Optional[Deque[str]] = Field(default=None)
    subtask_flow: Optional[Literal["ANALYSIS", "VISUALIZATION", "DIRECT_RESPONSE"]] = (
        Field(default=None)
    )

    # --------------------
    analysis_action_plan: Optional[str] = Field(default=None)
    visualization_action_plan: Optional[str] = Field(default=None)

    # --------------------
    code: Optional[str] = Field(default=None)
    error_message: Optional[str] = Field(default=None)

    # --------------------
    max_debugging_attempts: int = Field(default=5)
    current_debugging_attempt: int = Field(default=0)

    # --------------------
    analysis_report: Optional[List] = Field(default=None)
    visualization: Optional[str] = Field(default=None)
