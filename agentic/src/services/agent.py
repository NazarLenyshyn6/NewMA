"""..."""

from uuid import UUID

from sqlalchemy.orm import Session

from agent.nodes.decision import decision_node
from agent.nodes.responses.contextual import contextual_response_node
from agent.nodes.planning import planning_node
from agent.nodes.code.generation import code_generation_node
from agent.nodes.code.execution import code_execution_node
from agent.nodes.responses.techical import techical_response_node
from services.memory import agent_memory_service


class AgentService:

    @staticmethod
    async def chat_stream(
        question: str,
        db: Session,
        user_id: int,
        session_id: UUID,
        file_name: str,
        dataset_summary: str,
        storage_uri: str,
    ):
        """..."""
        response = decision_node.run(
            question=question,
            db=db,
            user_id=user_id,
            session_id=session_id,
            file_name=file_name,
            storage_uri=storage_uri,
        )
        if response == "RESPONSE":
            async for chunk in contextual_response_node.arun(
                question=question,
                db=db,
                user_id=user_id,
                session_id=session_id,
                file_name=file_name,
                storage_uri=storage_uri,
            ):
                yield chunk

        else:
            async for chunk in planning_node.arun(
                question=question,
                db=db,
                user_id=user_id,
                session_id=session_id,
                file_name=file_name,
                storage_uri=storage_uri,
            ):
                yield chunk
            async for chunk in code_generation_node.arun(
                instruction=planning_node.get_steamed_tokens(),
                dataset_summary=dataset_summary,
                db=db,
                user_id=user_id,
                session_id=session_id,
                file_name=file_name,
                storage_uri=storage_uri,
            ):
                yield chunk
            persisted_variables = None
            async for chunk in code_execution_node.arun(
                code_generation_message=code_generation_node.get_steamed_tokens(),
                db=db,
                user_id=user_id,
                session_id=session_id,
                file_name=file_name,
                storage_uri=storage_uri,
            ):
                if isinstance(chunk, dict):
                    persisted_variables = chunk
                else:
                    yield chunk
            analysis_report = persisted_variables.get("analysis_report")
            if analysis_report is not None:
                async for chunk in techical_response_node.arun(
                    question=question,
                    analysis_report=analysis_report,
                    db=db,
                    user_id=user_id,
                    session_id=session_id,
                    file_name=file_name,
                    storage_uri=storage_uri,
                ):
                    yield chunk
                conversation_history = agent_memory_service.get_conversation_memory(
                    db=db,
                    user_id=user_id,
                    session_id=session_id,
                    file_name=file_name,
                    storage_uri=storage_uri,
                )
                agent_memory_service.update_memory_cache(
                    db=db,
                    user_id=user_id,
                    session_id=session_id,
                    file_name=file_name,
                    storage_uri=storage_uri,
                    conversation_history=conversation_history
                    + [
                        {
                            "question": question,
                            "answer": planning_node.get_steamed_tokens()
                            + code_generation_node.get_steamed_tokens()
                            + techical_response_node.get_steamed_tokens(),
                        }
                    ],
                )
                print(
                    conversation_history
                    + [
                        {
                            "question": question,
                            "answer": planning_node.get_steamed_tokens()
                            + code_generation_node.get_steamed_tokens()
                            + techical_response_node.get_steamed_tokens(),
                        }
                    ],
                )

            else:
                yield "Code execution failed"
