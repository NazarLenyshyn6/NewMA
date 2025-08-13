"""..."""

from uuid import UUID
import pickle

from sqlalchemy.orm import Session

from services.memory import agent_memory_service


from agents.nodes.technical.routing import routing_node
from agents.nodes.technical.planning import planning_node
from agents.nodes.technical.code.generation import code_generation_node
from agents.nodes.technical.code.debagging import code_debagging_node
from agents.nodes.technical.code.execution import code_execution_node
from agents.nodes.technical.conversation import techical_conversation_node
from agents.nodes.technical.reporting import techical_reporting_node
from agents.nodes.business.conversation import business_conversation_node
from agents.nodes.summarization.conversation.business import business_conversation_summarization_node
from agents.nodes.summarization.conversation.technical import technical_conversation_summarization_node 
from agents.nodes.summarization.parallel import parallel_summarization_node



class AgentService:
    
    @staticmethod
    async def techical_chat_stream(
        question: str,
        db: Session,
        user_id: int,
        session_id: UUID,
        file_name: str,
        dataset_summary: str,
        storage_uri: str,
    ):
        """..."""
        code_execution_node._token_buffer = []
        response = routing_node.run(
            question=question,
            db=db,
            user_id=user_id,
            session_id=session_id,
            file_name=file_name,
            storage_uri=storage_uri,
        )
        if response == "RESPONSE":
            async for chunk in techical_conversation_node.arun(
                question=question,
                db=db,
                user_id=user_id,
                session_id=session_id,
                file_name=file_name,
                storage_uri=storage_uri,
            ):
                yield chunk
            new_conversation = [
                {
                    "question": question,
                    "answer": techical_conversation_node.get_steamed_tokens(),
                }
            ]
            conversation_summary = technical_conversation_summarization_node.run(
                conversation=technical_conversation_summarization_node.get_steamed_tokens(),
                db=db,
                question=question,
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
                conversation_context=pickle.dumps(conversation_summary),
            )

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
                question=question,
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
                question=question,
                dataset_summary=dataset_summary,
                code_generation_message=code_generation_node.get_steamed_tokens(),
                db=db,
                user_id=user_id,
                session_id=session_id,
                file_name=file_name,
                storage_uri=storage_uri,
            ):
                if isinstance(chunk, dict):
                    persisted_variables = chunk
                    break
                elif chunk == "Failed":
                    break
                else:
                    yield chunk
            if persisted_variables is not None:
                analysis_report = persisted_variables.get("analysis_report")
                async for chunk in techical_reporting_node.arun(
                    question=question,
                    analysis_report=analysis_report,
                    instruction=planning_node.get_steamed_tokens(),
                    db=db,
                    user_id=user_id,
                    session_id=session_id,
                    file_name=file_name,
                    storage_uri=storage_uri,
                ):
                    yield chunk

                summary = parallel_summarization_node.run(
                    db=db,
                    persisted_variables=[
                        variable for variable in persisted_variables.keys()
                    ],
                    question=question,
                    user_id=user_id,
                    session_id=session_id,
                    file_name=file_name,
                    storage_uri=storage_uri,
                    code_generation_message=code_generation_node.get_steamed_tokens(),
                    conversation=planning_node.get_steamed_tokens()
                    + techical_reporting_node.get_steamed_tokens(),
                )
                agent_memory_service.update_memory_cache(
                    db=db,
                    user_id=user_id,
                    session_id=session_id,
                    file_name=file_name,
                    storage_uri=storage_uri,
                    conversation_context=pickle.dumps(
                        summary["conversation_memory"].content
                    ),
                    code_context=pickle.dumps(summary["code_memory"].content),
                    persisted_variables=pickle.dumps(persisted_variables),
                )

            else:
                yield "Unexptexted error happend, try again."

            new_conversation = [
                {
                    "question": question,
                    "answer": planning_node.get_steamed_tokens()
                    + code_generation_node.get_steamed_tokens()
                    + code_execution_node.get_steamed_tokens()
                    + techical_reporting_node.get_steamed_tokens(),
                }
            ]
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
            conversation_history=pickle.dumps(conversation_history + new_conversation),
        )
   
                    
    @staticmethod
    async def business_chat_stream(
        question: str,
        db: Session,
        user_id: int,
        session_id: UUID,
        file_name: str,
        dataset_summary: str,
        storage_uri: str,
    ):
        """..."""
        async for chunk in business_conversation_node.arun(
                question=question,
                db=db,
                user_id=user_id,
                session_id=session_id,
                file_name=file_name,
                storage_uri=storage_uri,
            ):
                yield chunk
        new_conversation = [{
                    "question": question,
                    "answer": business_conversation_node.get_steamed_tokens(),
                }]
        business_conversation_summary = business_conversation_summarization_node.run(
                conversation=business_conversation_node.get_steamed_tokens(),
                db=db,
                question=question,
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
                conversation_context=pickle.dumps(business_conversation_summary),
            )
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
            conversation_history=pickle.dumps(conversation_history + new_conversation),
        )
            

    # @staticmethod
    # async def chat_stream(
    #     question: str,
    #     db: Session,
    #     user_id: int,
    #     session_id: UUID,
    #     file_name: str,
    #     dataset_summary: str,
    #     storage_uri: str,
    # ):
    #     """..."""
    #     code_execution_node._token_buffer = []
    #     response = decision_node.run(
    #         question=question,
    #         db=db,
    #         user_id=user_id,
    #         session_id=session_id,
    #         file_name=file_name,
    #         storage_uri=storage_uri,
    #     )
    #     if response == "RESPONSE":
    #         async for chunk in contextual_response_node.arun(
    #             question=question,
    #             db=db,
    #             user_id=user_id,
    #             session_id=session_id,
    #             file_name=file_name,
    #             storage_uri=storage_uri,
    #         ):
    #             yield chunk
    #         new_conversation = [
    #             {
    #                 "question": question,
    #                 "answer": contextual_response_node.get_steamed_tokens(),
    #             }
    #         ]
    #         conversation_summary = conversation_summarization_node.run(
    #             conversation=conversation_summarization_node.get_steamed_tokens(),
    #             db=db,
    #             question=question,
    #             user_id=user_id,
    #             session_id=session_id,
    #             file_name=file_name,
    #             storage_uri=storage_uri,
    #         )
    #         agent_memory_service.update_memory_cache(
    #             db=db,
    #             user_id=user_id,
    #             session_id=session_id,
    #             file_name=file_name,
    #             storage_uri=storage_uri,
    #             conversation_context=pickle.dumps(conversation_summary),
    #         )

    #     else:
    #         async for chunk in planning_node.arun(
    #             question=question,
    #             db=db,
    #             user_id=user_id,
    #             session_id=session_id,
    #             file_name=file_name,
    #             storage_uri=storage_uri,
    #         ):
    #             yield chunk
    #         async for chunk in code_generation_node.arun(
    #             question=question,
    #             instruction=planning_node.get_steamed_tokens(),
    #             dataset_summary=dataset_summary,
    #             db=db,
    #             user_id=user_id,
    #             session_id=session_id,
    #             file_name=file_name,
    #             storage_uri=storage_uri,
    #         ):
    #             yield chunk
    #         persisted_variables = None
    #         async for chunk in code_execution_node.arun(
    #             question=question,
    #             dataset_summary=dataset_summary,
    #             code_generation_message=code_generation_node.get_steamed_tokens(),
    #             db=db,
    #             user_id=user_id,
    #             session_id=session_id,
    #             file_name=file_name,
    #             storage_uri=storage_uri,
    #         ):
    #             if isinstance(chunk, dict):
    #                 persisted_variables = chunk
    #                 break
    #             elif chunk == "Failed":
    #                 break
    #             else:
    #                 yield chunk
    #         if persisted_variables is not None:
    #             analysis_report = persisted_variables.get("analysis_report")
    #             async for chunk in techical_response_node.arun(
    #                 question=question,
    #                 analysis_report=analysis_report,
    #                 instruction=planning_node.get_steamed_tokens(),
    #                 db=db,
    #                 user_id=user_id,
    #                 session_id=session_id,
    #                 file_name=file_name,
    #                 storage_uri=storage_uri,
    #             ):
    #                 yield chunk

    #             summary = parallel_summarization_node.run(
    #                 db=db,
    #                 persisted_variables=[
    #                     variable for variable in persisted_variables.keys()
    #                 ],
    #                 question=question,
    #                 user_id=user_id,
    #                 session_id=session_id,
    #                 file_name=file_name,
    #                 storage_uri=storage_uri,
    #                 code_generation_message=code_generation_node.get_steamed_tokens(),
    #                 conversation=planning_node.get_steamed_tokens()
    #                 + techical_response_node.get_steamed_tokens(),
    #             )
    #             agent_memory_service.update_memory_cache(
    #                 db=db,
    #                 user_id=user_id,
    #                 session_id=session_id,
    #                 file_name=file_name,
    #                 storage_uri=storage_uri,
    #                 conversation_context=pickle.dumps(
    #                     summary["conversation_memory"].content
    #                 ),
    #                 code_context=pickle.dumps(summary["code_memory"].content),
    #                 persisted_variables=pickle.dumps(persisted_variables),
    #             )

    #         else:
    #             yield "Unexptexted error happend, try again."

    #         new_conversation = [
    #             {
    #                 "question": question,
    #                 "answer": planning_node.get_steamed_tokens()
    #                 + code_generation_node.get_steamed_tokens()
    #                 + code_execution_node.get_steamed_tokens()
    #                 + techical_response_node.get_steamed_tokens(),
    #             }
    #         ]
    #     conversation_history = agent_memory_service.get_conversation_memory(
    #         db=db,
    #         user_id=user_id,
    #         session_id=session_id,
    #         file_name=file_name,
    #         storage_uri=storage_uri,
    #     )
    #     agent_memory_service.update_memory_cache(
    #         db=db,
    #         user_id=user_id,
    #         session_id=session_id,
    #         file_name=file_name,
    #         storage_uri=storage_uri,
    #         conversation_history=pickle.dumps(conversation_history + new_conversation),
    #     )
