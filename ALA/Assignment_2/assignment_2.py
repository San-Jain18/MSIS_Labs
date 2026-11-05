
import re
import string
import numpy as np
import gensim.downloader as api

from vector import Vector


# =========================================================
# PART A: SELECT EXACTLY 20 TAGS
# =========================================================

TAGS = [
    "research", "innovation", "education", "university", "student",
    "faculty", "campus", "engineering", "medicine", "technology",
    "curriculum", "collaboration", "publication", "laboratory",
    "scholarship", "mentorship", "internship", "entrepreneurship",
    "accreditation", "alumni"
]


# =========================================================
# PART C: PREPROCESS THE INPUT TEXT
# =========================================================

STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "on",
    "for", "is", "are", "was", "were", "with", "at", "by",
    "from", "this", "that", "these", "those", "it", "its",
    "we", "our", "you", "your", "they", "their", "he", "she",
    "as", "be", "been", "being", "have", "has", "had", "do",
    "does", "did", "will", "would", "can", "could", "about",
    "into", "through", "after", "before", "over", "under",
    "more", "most", "some", "such", "not", "than", "also",
    "here", "there", "who", "which", "what", "when", "where"
}


def preprocess_text(text):
    """
    Convert text to lowercase, remove punctuation, tokenize,
    remove stopwords and short words.

    Returns:
        original_tokens: tokens before preprocessing
        processed_tokens: tokens after preprocessing
    """

    original_tokens = text.split()

    text = text.lower()

    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    tokens = text.split()

    processed_tokens = [
        word for word in tokens
        if word not in STOPWORDS and len(word) > 2
    ]

    return original_tokens, processed_tokens


# =========================================================
# PART D: BUILD TAG MATRIX
# =========================================================

def build_tag_matrix(model, tags):
    """
    Construct the tag matrix T.

    Returns:
        tag_names: list of 20 tags
        T: NumPy array of shape (20, 50)
    """

    if len(tags) != 20:
        raise ValueError("Exactly 20 tags are required.")

    tag_vectors = []

    for tag in tags:

        words = tag.lower().split()

        for word in words:
            if word not in model.key_to_index:
                raise ValueError(
                    f"Tag component not in vocabulary: {word}"
                )

        vectors = [model[word] for word in words]

        tag_vector = np.mean(vectors, axis=0)

        tag_vectors.append(tag_vector)

    T = np.array(tag_vectors)

    return tags, T


# =========================================================
# PART D: BUILD TEXT MATRIX
# =========================================================

def build_text_matrix(model, tokens):
    """
    Construct the text matrix W.

    Returns:
        in_vocab_tokens: words present in model vocabulary
        oov_tokens: words absent from model vocabulary
        W: NumPy array of shape (n, 50)
    """

    in_vocab_tokens = []
    oov_tokens = []

    word_vectors = []

    for token in tokens:

        if token in model.key_to_index:

            in_vocab_tokens.append(token)
            word_vectors.append(model[token])

        else:

            oov_tokens.append(token)

    if len(word_vectors) == 0:
        W = np.empty((0, 50))

    else:
        W = np.array(word_vectors)

    return in_vocab_tokens, oov_tokens, W


# =========================================================
# PART E: SIMILARITY USING VECTOR CLASS
# =========================================================

def similarity_matrix_vector_class(W, T):
    """
    Compute cosine similarity using Vector class and Python loops.

    Returns:
        S: similarity matrix of shape (n_words, 20)
    """

    n_words = W.shape[0]
    n_tags = T.shape[0]

    S = []

    for i in range(n_words):

        row = []

        word_vector = Vector(W[i])

        for j in range(n_tags):

            tag_vector = Vector(T[j])

            similarity = word_vector.cosine_similarity(
                tag_vector
            )

            row.append(similarity)

        S.append(row)

    return np.array(S)


# =========================================================
# PART F: SIMILARITY USING NUMPY
# =========================================================

def similarity_matrix_numpy(W, T):
    """
    Compute cosine similarity using NumPy row normalization
    and matrix multiplication.

    Returns:
        S: similarity matrix of shape (n_words, 20)
    """

    W_norm = np.linalg.norm(W, axis=1, keepdims=True)

    T_norm = np.linalg.norm(T, axis=1, keepdims=True)

    if np.any(W_norm == 0):
        raise ValueError("W contains a zero vector.")

    if np.any(T_norm == 0):
        raise ValueError("T contains a zero vector.")

    W_hat = W / W_norm

    T_hat = T / T_norm

    S = W_hat @ T_hat.T

    return S


# =========================================================
# PART H: RANK TAGS USING MAX POOLING
# =========================================================

def rank_tags(tag_names, S, in_vocab_tokens):
    """
    Rank tags by maximum similarity across all text words.

    Returns:
        list of tuples:
        (tag, score, best_matching_word)
    """

    rankings = []

    for j, tag in enumerate(tag_names):

        column = S[:, j]

        max_index = np.argmax(column)

        max_score = column[max_index]

        best_word = in_vocab_tokens[max_index]

        rankings.append(
            (tag, float(max_score), best_word)
        )

    rankings.sort(
        key=lambda item: item[1],
        reverse=True
    )

    return rankings


# =========================================================
# MAIN PROGRAM
# =========================================================

def main():

    print("=" * 60)
    print("SEMANTIC TAGGING WITH GLOVE AND NUMPY")
    print("=" * 60)

    # Load pretrained GloVe model
    print("\nLoading GloVe model...")

    model = api.load("glove-wiki-gigaword-50")

    print("Model loaded successfully!")

    # Read input text
    with open("input_text.txt", "r", encoding="utf-8") as file:

        text = file.read()

    # Preprocessing
    original_tokens, processed_tokens = preprocess_text(text)

    # OOV and in-vocabulary handling
    in_vocab_tokens, oov_tokens, W = build_text_matrix(
        model, processed_tokens
    )

    print("\n" + "=" * 60)
    print("TOKEN STATISTICS")
    print("=" * 60)

    print("Tokens before preprocessing:", len(original_tokens))

    print("Tokens after preprocessing:", len(processed_tokens))

    print("In-vocabulary tokens:", len(in_vocab_tokens))

    print("Out-of-vocabulary tokens:", len(oov_tokens))

    print("Distinct OOV tokens:", sorted(set(oov_tokens)))

    # Handle empty text matrix
    if W.shape[0] == 0:

        print("\nERROR: No usable in-vocabulary words found.")

        return

    # Build tag matrix
    tag_names, T = build_tag_matrix(model, TAGS)

    print("\nTag matrix shape:", T.shape)

    print("Text matrix shape:", W.shape)

    # Vector class similarity
    S_vector = similarity_matrix_vector_class(W, T)

    # NumPy similarity
    S_numpy = similarity_matrix_numpy(W, T)

    # Numerical verification
    print("\n" + "=" * 60)
    print("NUMERICAL VERIFICATION")
    print("=" * 60)

    print(
        "Matrices are approximately equal:",
        np.allclose(S_vector, S_numpy, atol=1e-8)
    )

    max_difference = np.max(
        np.abs(S_vector - S_numpy)
    )

    print("Maximum absolute difference:", max_difference)

    # Max pooling and tag ranking
    rankings = rank_tags(
        tag_names, S_numpy, in_vocab_tokens
    )

    print("\n" + "=" * 60)
    print("TOP 8 TAGS")
    print("=" * 60)

    print(
        f"{'Rank':<8}{'Tag':<22}"
        f"{'Score':<15}{'Best matching word'}"
    )

    print("-" * 65)

    for rank, (tag, score, word) in enumerate(
        rankings[:8], start=1
    ):

        print(
            f"{rank:<8}{tag:<22}"
            f"{score:<15.4f}{word}"
        )

        if tag == word:
            print(" " * 8 + "(Exact word match)")
        else:
            print(" " * 8 + "(Semantic match)")


if __name__ == "__main__":
    main()