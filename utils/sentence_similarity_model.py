from sentence_transformers import util
from .model_loader import ModelLoaderSingleton

model = ModelLoaderSingleton.get_model()


def compute_embedding(texts):
    # Compute embeddings for a batch of texts using the SentenceTransformer model
    embeddings = model.encode(texts, convert_to_tensor=True)
    return embeddings


def compute_similarity(source_embedding, target_embeddings):
    # Compute cosine similarity between a source embedding and a batch of target embeddings
    # Utilizes vectorized operations for efficiency.
    return util.pytorch_cos_sim(source_embedding, target_embeddings)


def get_similarity_scores(source_sentence, sentences):
    # Compute embeddings for source sentence and all target sentences in one go
    all_sentences = [source_sentence] + sentences
    all_embeddings = compute_embedding(all_sentences)

    # Extract source embedding and target embeddings
    source_embedding = all_embeddings[0].unsqueeze(0)  # Add batch dimension to source embedding
    target_embeddings = all_embeddings[1:]  # Rest are target embeddings

    # Compute similarities in a vectorized manner
    similarities = compute_similarity(source_embedding, target_embeddings)

    # Convert similarity tensor to a list of scores
    scores = similarities.squeeze(0).tolist()  # Remove unnecessary dimensions and convert to list

    return scores
