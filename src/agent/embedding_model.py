import time
import random


class EmbeddingModel:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model = None
        self.dim = 1536

        self.load_model()

    def load_model(self):
        # Simulate loading a model (e.g., from disk or a remote source)
        print(f"Loading embedding model '{self.model_name}'...")
        self.model = f"Loaded {self.model_name} embedding model"
        print(f"Model '{self.model_name}' loaded successfully.")

    def get_embedding(self, text: str):
        if self.model is None:
            raise ValueError("Model not loaded. Please call load_model() first.")
        # Simulate generating an embedding for the input text
        print(f"Generating embedding for: '{text}'")
        time.sleep(1)  # Simulate time taken to generate the embedding
        embedding = [random.random() for _ in range(self.dim)]
        print(f"Generated embedding for '{text}': {embedding}")
        return embedding
    
    def get_multiple_embeddings(self, texts: list):
        return [self.get_embedding(text) for text in texts]
    
