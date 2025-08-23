# app/tree_builder.py
from __future__ import annotations
from typing import Dict, Any, List
import logging
from sympy import symbols, latex

logger = logging.getLogger(__name__)
n = symbols("n")

def _odd_predecessor(m: int, q: int, p: int = 3) -> int | None:
    """
    奇数側の前駆候補 n = (m - q)/p を返す。
    - 整数
    - 正
    - 奇数
    のときのみ有効。
    """
    num = m - q
    if num % p != 0:
        return None
    cand = num // p
    if cand <= 0 or cand % 2 == 0:
        return None
    return cand

def build_tree(root_value: int, Q: List[int], depth: int, p: int = 3) -> Dict[str, Any]:
    """
    逆木を「子 = 前駆ノード」として段数固定で構築。
    children には root_value の前駆（2n と (n-q)/p 条件付）が入る。
    """
    q = Q[1]

    def expand(value: int, level: int) -> Dict[str, Any]:
        node = {"value": value, "children": []}
        if level == depth:
            return node

        children: List[Dict[str, Any]] = []

        # 偶数側（常に有効）: 2n
        expr_even = 2 * n
        v_even = int(expr_even.subs(n, value))
        children.append({
            "value": v_even,
            "expr": {
                "sympy": str(expr_even),
                "text": str(expr_even),
                "latex": latex(expr_even),
            },
            "children": [],  # 後で埋める
        })

        # 奇数側（条件付き）: (n - q)/p が整数かつ奇数
        odd = _odd_predecessor(value, q, p)
        if odd is not None:
            expr_odd = (n - q) / p
            children.append({
                "value": odd,
                "expr": {
                    "sympy": str(expr_odd),
                    "text": str(expr_odd),
                    "latex": latex(expr_odd),
                },
                "children": [],
            })

        logger.info("expand level=%d value=%d -> children=%s",
                    level, value, [c["value"] for c in children])

        # 再帰
        for c in children:
            sub = expand(c["value"], level + 1)
            c["children"] = sub["children"]

        node["children"] = children
        return node

    return expand(root_value, 0)

def to_adjacency(tree: Dict[str, Any]) -> Dict[int, List[int]]:
    """
    ネスト木 → 隣接リスト {node: [children_values,...]} に変換。
    """
    adj: Dict[int, List[int]] = {}

    def walk(node: Dict[str, Any]) -> None:
        v = int(node["value"])
        adj[v] = [int(c["value"]) for c in node.get("children", [])]
        for c in node.get("children", []):
            walk(c)

    walk(tree)
    return adj
