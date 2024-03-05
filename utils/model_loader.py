import os
from sentence_transformers import SentenceTransformer


class ModelLoaderSingleton:
    _model_instance = None
    MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    MODEL_DIRECTORY = './sentence_similarity_model'
    MODEL_PATH = MODEL_DIRECTORY + "/sentence-transformers_paraphrase-multilingual-MiniLM-L12-v2"

    @classmethod
    def get_model(cls):
        if cls._model_instance is None:
            cls._model_instance = cls.load_or_download_model()
        return cls._model_instance

    @classmethod
    def load_or_download_model(cls):
        # Check if the model directory exists
        if not os.path.exists(cls.MODEL_DIRECTORY):
            # If the directory does not exist, create it
            os.makedirs(cls.MODEL_DIRECTORY)
            print(f"Directory {cls.MODEL_DIRECTORY} created and downloading model and tokenizer.")
            # Download and save the model and tokenizer
            _model = SentenceTransformer(cls.MODEL_NAME, cache_folder=cls.MODEL_DIRECTORY)
            print(f"Model and tokenizer downloaded and saved to {cls.MODEL_DIRECTORY} successfully.")
        else:
            # If the directory exists, load the model and tokenizer from it
            print(f"Loading model and tokenizer from {cls.MODEL_DIRECTORY}.")
            _model = SentenceTransformer(cls.MODEL_PATH)
            print(f"Model and tokenizer loaded from {cls.MODEL_DIRECTORY} successfully.")

        return _model
