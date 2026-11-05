import string
import sys
from pathlib import Path

import numpy as np


TAGS = [
    "research", "innovation", "education", "university", "students",
    "faculty", "campus", "engineering", "medicine", "technology",
    "curriculum", "collaboration", "publication", "laboratory",
    "scholarship", "mentorship", "internship", "entrepreneurship",
    "accreditation", "alumni",
]


STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "for",
    "is", "are", "was", "were", "with", "at", "by", "from", "it",
    "this", "that", "these", "those", "our", "we", "us", "you",
    "your", "their", "they", "them", "he", "she", "his", "her",
    "has", "have", "had", "be", "been", "being", "as", "into",
    "its", "who", "which", "what", "when", "where", "how", "will",
    "would", "can", "could", "may", "might", "also", "more",
}


class Vector:
    
    def __init__(self, values):
        self.values = tuple(float(x) for x in values)

    def add(self, other):
        if len(self.values) != len(other.values):
            raise ValueError("Vectors must have the same dimension.")
        return Vector(a + b for a, b in zip(self.values, other.values))

    def scale(self, scalar):
        return Vector(scalar * x for x in self.values)

    def dot(self, other):
        if len(self.values) != len(other.values):
            raise ValueError("Vectors must have the same dimension.")
        return sum(a * b for a, b in zip(self.values, other.values))

    def norm(self):
        return sum(x * x for x in self.values) ** 0.5

    def cosine_similarity(self, other):
        denominator = self.norm() * other.norm()
        if denominator == 0:
            raise ValueError("Cosine similarity is undefined for a zero vector.")
        return self.dot(other) / denominator


def preprocess_text(text, stopwords=None):
   
    if stopwords is None:
        stopwords = STOPWORDS

    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens_before = text.split()
    tokens_after = [
        token for token in tokens_before
        if token not in stopwords and len(token) > 2
    ]
    return tokens_before, tokens_after


def build_tag_matrix(model, tags):
    if len(tags) != 20:
        raise ValueError(f"Exactly 20 tags are required; received {len(tags)}.")

    rows = []
    for tag in tags:
        components = tag.lower().split()
        if not components:
            raise ValueError("A tag cannot be empty.")

        missing = [word for word in components if word not in model.key_to_index]
        if missing:
            raise ValueError(
                f"Tag '{tag}' contains word(s) not in model vocabulary: {missing}"
            )

        component_vectors = [np.asarray(model[word], dtype=float) for word in components]
        rows.append(np.mean(component_vectors, axis=0))

    T = np.vstack(rows)
    if T.shape != (20, 50):
        raise ValueError(f"Expected tag matrix shape (20, 50), got {T.shape}.")
    return list(tags), T


def build_text_matrix(model, tokens):
    in_vocab_tokens = []
    oov_tokens = []
    rows = []

    for token in tokens:
        if token in model.key_to_index:
            in_vocab_tokens.append(token)
            rows.append(np.asarray(model[token], dtype=float))
        else:
            oov_tokens.append(token)

    if rows:
        W = np.vstack(rows)
    else:
        W = np.empty((0, 50), dtype=float)

    return in_vocab_tokens, oov_tokens, W


def similarity_matrix_vector_class(W, T):
    """Compute all pairwise cosine similarities using Vector and Python loops."""
    if W.ndim != 2 or T.ndim != 2 or W.shape[1] != T.shape[1]:
        raise ValueError("W and T must be 2-D arrays with matching dimensions.")

    result = []
    for i in range(W.shape[0]):
        row = []
        for j in range(T.shape[0]):
            word_vector = Vector(W[i])
            tag_vector = Vector(T[j])
            row.append(word_vector.cosine_similarity(tag_vector))
        result.append(row)

    return np.asarray(result, dtype=float).reshape(W.shape[0], T.shape[0])


def similarity_matrix_numpy(W, T):
    """Compute cosine similarities using row normalization and matrix multiplication."""
    if W.ndim != 2 or T.ndim != 2 or W.shape[1] != T.shape[1]:
        raise ValueError("W and T must be 2-D arrays with matching dimensions.")

    W_norm = np.linalg.norm(W, axis=1, keepdims=True)
    T_norm = np.linalg.norm(T, axis=1, keepdims=True)

    if np.any(W_norm == 0) or np.any(T_norm == 0):
        raise ValueError("Cosine similarity is undefined for zero-vector rows.")

    W_hat = W / W_norm
    T_hat = T / T_norm
    return W_hat @ T_hat.T


def rank_tags(tag_names, S, in_vocab_tokens):
    if S.ndim != 2 or S.shape != (len(in_vocab_tokens), len(tag_names)):
        raise ValueError("S dimensions must match the text tokens and tag names.")
    if S.shape[0] == 0:
        raise ValueError("Cannot rank tags because there are no in-vocabulary words.")

    ranking = []
    for j, tag in enumerate(tag_names):
        best_index = int(np.argmax(S[:, j]))
        score = float(S[best_index, j])
        best_word = in_vocab_tokens[best_index]
        identical_match = best_word == tag.lower()
        ranking.append((tag, score, best_word, identical_match))

    return sorted(ranking, key=lambda item: item[1], reverse=True)


def load_glove_model():
    """Load the pretrained GloVe 50-dimensional model using gensim."""
    try:
        import gensim.downloader as api
    except ImportError as exc:
        raise RuntimeError(
            "gensim is not installed. Run: pip install -r requirements.txt"
        ) from exc

    print("Loading glove-wiki-gigaword-50 (first download may take some time)...")
    return api.load("glove-wiki-gigaword-50")


def main():
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("input.txt")
    if not input_path.exists():
        print(
            f"ERROR: {input_path} was not found. Create input.txt containing "
            "up to 400 words of real LinkedIn text about Manipal University."
        )
        return

    raw_text = input_path.read_text(encoding="utf-8")
    tokens_before, processed_tokens = preprocess_text(raw_text)

    model = load_glove_model()
    tag_names, T = build_tag_matrix(model, TAGS)
    in_vocab_tokens, oov_tokens, W = build_text_matrix(model, processed_tokens)

    print("TOKEN STATISTICS")
    print("Tokens before preprocessing:", len(tokens_before))
    print("Tokens after preprocessing:", len(processed_tokens))
    print("In-vocabulary tokens:", len(in_vocab_tokens))
    print("Out-of-vocabulary tokens:", len(oov_tokens))
    print("Distinct OOV tokens:", sorted(set(oov_tokens)))

    print("MATRIX SHAPES")
    print("T.shape =", T.shape)
    print("W.shape =", W.shape)

    if W.shape[0] == 0:
        print("ERROR: No usable in-vocabulary words. Similarity computation stopped.")
        return

    S_vector = similarity_matrix_vector_class(W, T)
    S_numpy = similarity_matrix_numpy(W, T)

    print("SIMILARITY VERIFICATION")
    print("S_vector.shape =", S_vector.shape)
    print("S_numpy.shape  =", S_numpy.shape)
    print("np.allclose(S_vector, S_numpy) =", np.allclose(
        S_vector, S_numpy, rtol=1e-5, atol=1e-8
    ))
    print("Maximum absolute difference =", np.max(np.abs(S_vector - S_numpy)))

    ranking = rank_tags(tag_names, S_numpy, in_vocab_tokens)
    print("TOP EIGHT TAGS (MAX POOLING)")
    print(f"{'Rank':<6}{'Tag':<20}{'Score':<12}{'Best-matching word':<24}{'Match type'}")
    print("-" * 78)
    for rank, (tag, score, word, identical) in enumerate(ranking[:8], start=1):
        match_type = "Identical" if identical else "Different word"
        print(f"{rank:<6}{tag:<20}{score:<12.6f}{word:<24}{match_type}")


if __name__ == "__main__":
    main()