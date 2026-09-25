# pip install sentence-transformers
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")   # ① free, fast, 384 dims

vec = model.encode("A cat is sleeping on the couch")  # ② that's an embedding!
print(vec.shape)         # → (384,)  — 384 numbers
print(vec[:5])           # → [-0.05, 0.12, 0.41, -0.08, 0.22] (something like that)

# to compare two pieces of text → encode both → take cosine similarity
from numpy import dot
from numpy.linalg import norm

v1 = model.encode("A cat is sleeping on the couch")
v2 = model.encode("A kitten is napping on the sofa")
similarity = dot(v1, v2) / (norm(v1) * norm(v2))   # cosine
print(similarity)        # → 0.87 (very similar 🎉)

king = model.encode("king")
man = model.encode("men")
woman = model.encode("women")
queen = model.encode("queen")
print('King = ', king[:5])
print('Men = ', man[:5])
print('Women = ', woman[:5])
print('Queen = ', queen[:5])
queen_approx = king - man + woman
print('queen_approx = ', queen_approx[:5])
similarity_queen = dot(queen_approx, queen) / (norm(queen_approx) * norm(queen))   # cosine
print(similarity_queen)        # → 0.84