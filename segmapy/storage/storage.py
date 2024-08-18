import os
import chromadb
from typing import Dict, List
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction, OllamaEmbeddingFunction
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings

from segmapy.utils.can_import import can_import
from segmapy.logs import logger


def use_chroma():
    print("\nUsing results storage: " + "\033[93m\033[1m" + "Chroma (Default)" + "\033[0m\033[0m")
    return DefaultResultsStorage()


# Results storage using local ChromaDB
class DefaultResultsStorage:
    def __init__(self):
        logger.info("Using ChromaDB for results storage")
        # Create Chroma collection
        chroma_persist_dir = "chroma"
        chroma_client = chromadb.PersistentClient(
            settings=chromadb.config.Settings(
                persist_directory=chroma_persist_dir,
            )
        )
        metric = "cosine"
        embedding_function = OllamaEmbeddingFunction(url=os.getenv("EMBEDDING_URL"), model_name="shaw/dmeta-embedding-zh:latest")
        self.collection = chroma_client.get_or_create_collection(
            name=os.environ("RESULTS_STORE_NAME", "results"),
            metadata={"hnsw:space": metric},
            embedding_function=embedding_function,
        )

    def add(self, task: Dict, result: str, result_id: str):
        if (
                len(self.collection.get(ids=[result_id], include=[])["ids"]) > 0
        ):  # Check if the result already exists
            self.collection.update(
                ids=result_id,
                documents=result,
                metadatas={"task": task["task_name"], "result": result},
            )
        else:
            self.collection.add(
                ids=result_id,
                documents=result,
                metadatas={"task": task["task_name"], "result": result},
            )

    def query(self, query: str, top_results_num: int) -> List[dict]:
        count: int = self.collection.count()
        if count == 0:
            return []
        results = self.collection.query(
            query_texts=query,
            n_results=min(top_results_num, count),
            include=["metadatas"]
        )
        return [item["task"] for item in results["metadatas"][0]]


local_storage = use_chroma()

if __name__ == "__main__":
    task = {"task_name": "test"}
    result = "哈哈哈啊哈"
    result_id = "test"
    local_storage.add(task, result, result_id)
    print(local_storage.query("test", 1))
