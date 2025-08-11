"""..."""

from typing import override, Optional, List
from uuid import UUID
import pickle

from sqlalchemy.orm import Session

from agent.nodes.base import BaseNode
from agent.models.anthropic_ import code_generation_model
from agent.prompts.code.generation import code_generation_prompt
from services.memory import agent_memory_service


dependencies = [
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


class CodeGenerationNode(BaseNode):
    """..."""

    @override
    def run(
        self,
        question: str,
        db: Optional[Session] = None,
        user_id: Optional[int] = None,
        session_id: Optional[UUID] = None,
        file_name: Optional[str] = None,
        storage_uri: Optional[str] = None,
    ): ...

    @override
    async def arun(
        self,
        question: str,
        instruction: str,
        dataset_summary: str,
        db: Optional[Session] = None,
        user_id: Optional[int] = None,
        session_id: Optional[UUID] = None,
        file_name: Optional[str] = None,
        storage_uri: Optional[str] = None,
        dependencies: List[str] = dependencies,
    ):
        """..."""
        code_history = pickle.loads(
            self.memory.get_memory(
                db=db,
                user_id=user_id,
                session_id=session_id,
                file_name=file_name,
                storage_uri=storage_uri,
            ).code_context
        )
        persisted_variables = pickle.loads(
            self.memory.get_memory(
                db=db,
                user_id=user_id,
                session_id=session_id,
                file_name=file_name,
                storage_uri=storage_uri,
            ).persisted_variables
        )
        persisted_variables = [key for key in persisted_variables.keys()]
        print("Code history:", code_history)
        async for chunk in self._chain.astream(
            {
                "instruction": instruction,
                "history": code_history,
                "dataset_summary": dataset_summary,
                "dependencies": dependencies,
                "question": question,
                "persisted_variables": persisted_variables
            }
        ):
            chunk = chunk.content
            self._token_buffer.append(chunk)
            yield chunk


code_generation_node = CodeGenerationNode(
    model=code_generation_model,
    prompt=code_generation_prompt,
    memory=agent_memory_service,
)
