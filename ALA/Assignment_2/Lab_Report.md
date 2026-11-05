# Lab Report Answers

## Tag vocabulary justification
The 20 tags are the suggested list. Each names an academic, research, educational, professional or campus concept, and all are single words (no multi-word tags). `build_tag_matrix` raises `ValueError` if any tag word is missing from the model vocabulary.

## Preprocessing notes
Starter stopwords extended with: it, its, this, that, these, those, our, we, us, you, your, they, their, them, he, she, his, her, i, my, be, been, has, have, had, will, can, as, but, not, all, also, who, which, what, more, than, into, about. Punctuation is replaced by a space (so "university's" becomes "university", "s", and "s" is dropped by the length filter).

## 1. Dimensions
(a) one word vector: 50 (a vector in R^50)
(b) W: n x 50
(c) T: 20 x 50
(d) T^T: 50 x 20
(e) S: n x 20

## 2. Why the normalized dot product equals cosine similarity
Row i of W-hat is W_i / ||W_i||, and row j of T-hat is T_j / ||T_j||. Then
W-hat_i · T-hat_j = (W_i · T_j) / (||W_i|| ||T_j||) = cos(W_i, T_j),
because scalar factors come out of the dot product. Both rows have norm 1, so only the angle between them remains.

## 3. Why one matrix product gives all 20n similarities
Entry (i, j) of the product W-hat T-hat^T is the dot product of row i of W-hat with column j of T-hat^T, which is row j of T-hat. Matrix multiplication computes that for every (i, j) pair, so the n x 50 times 50 x 20 product has exactly the 20n cosine similarities.

## 4. One word highly similar to "medicine"
Max pooling takes the largest entry in the medicine column, so that single word sets the score and medicine gets a high r_j. The many low-similarity words have no effect on it.

## 5. Does a high max-pool score mean the tag is the dominant topic?
No. The score reflects only the single best-matching word. One word appearing once can give a high score, while the tag may be nearly irrelevant to the rest of the text. Max pooling detects local evidence, not frequency or coverage.

## 6. Identical vs different matches in the top eight
Fill this in from your program output (the Match column). Tags matched by an identical word score exactly 1.0 and sit at the top. Tags matched by a different word score below 1.0, and show where embeddings find semantic relatedness (for example "technology" matched by "digital"). What this shows: cosine similarity over word embeddings measures closeness of word meaning and usage in the training corpus. It does not measure topic, importance, frequency or context, and an identical word is a trivial match that tells you only that the word appears.

## 7. Can the ranking add a new tag?
No. The algorithm only scores the fixed 20 tag vectors in T. A concept outside the vocabulary can show up only indirectly, as a weak similarity to some existing tag.

## 8. Why out-of-vocabulary tokens are excluded from W
They have no embedding vector, so no row of W can be built for them. Inventing one (such as a zero vector) would make the norm zero, so cosine similarity would be undefined (division by zero) and would distort the results.

## 9. Relationship between Vector.cosine_similarity and the matrix product
The Vector class computes S_ij = (W_i · T_j) / (||W_i|| ||T_j||) one pair at a time in a Python double loop. The NumPy version normalizes the rows first and then evaluates all the dot products at once as W-hat T-hat^T. The two are algebraically identical, since dividing by the norms before or after the dot product gives the same value. They differ only by floating-point rounding (around 1e-16), and the vectorized one is much faster.
