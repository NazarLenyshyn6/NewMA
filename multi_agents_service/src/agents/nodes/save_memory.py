"""..."""

import pickle

from agents.state import AgentState
from services.memory.conversation_summary import conversation_summary_memory_service
from services.memory.conversation import conversation_memory_service
from services.memory.code_summary import code_summary_memory_service
from services.memory.variables import variables_memory_service


class SaveMemoryNode:

    @staticmethod
    def save(state: AgentState):
        """..."""

        print("* SaveMemoryNode -> ")
        services = [
            conversation_summary_memory_service,
            code_summary_memory_service,
            variables_memory_service,
        ]
        update_values = [
            state.conversation_summary_memory,
            state.code_summary_memory,
            state.variables_memory,
        ]

        for service, update_value in zip(services, update_values):
            if update_value is None:
                continue
            service.update_memory_cache(
                db=state.db,
                user_id=state.user_id,
                session_id=state.session_id,
                file_name=state.file_name,
                storage_uri=state.storage_uri,
                update_value=pickle.dumps(update_value),
            )

        # Get prevous conversation memory and exted it with current conversation memory
        conversation_memory = pickle.loads(
            conversation_memory_service.get_memory(
                db=state.db,
                user_id=state.user_id,
                session_id=state.session_id,
                file_name=state.file_name,
                storage_uri=state.storage_uri,
            ).memory
        )

        conversation_memory_service.update_memory_cache(
            db=state.db,
            user_id=state.user_id,
            session_id=state.session_id,
            file_name=state.file_name,
            storage_uri=state.storage_uri,
            update_value=pickle.dumps(
                conversation_memory + state.conversation_memory,
            ),
        )
