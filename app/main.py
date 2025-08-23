from fastapi import FastAPI
from .tree_builder import build_tree

app = FastAPI()

@app.get("/tree")
def get_tree(root: int = 8, q: int = 5, depth: int = 5):
    Q = [None, q]
    tree = build_tree(root, Q, depth)
    return tree
