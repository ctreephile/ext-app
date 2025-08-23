# tests/test_tree_builder.py
import json
import logging
import pytest
from app.tree_builder import build_tree, to_adjacency

logger = logging.getLogger(__name__)

def test_reverse_tree_q1_depth3_structure_and_logging():
    """
    標準コラッツ (q=1) で root=8, depth=3 の逆木が
    8→[16], 16→[32,5], 5→[10], 32→[64] になることを検証。
    さらに、この隣接リストを tests/logs にログ出力。
    """
    Q = [None, 1]
    tree = build_tree(root_value=8, Q=Q, depth=3, p=3)
    adj = to_adjacency(tree)

    expected = {
        8:  [16],
        16: [32, 5],
        5:  [10],
        32: [64],
        # 叶うなら下位もあるが depth=3 なのでここまで
    }

    # 期待キーが含まれ、内容が一致
    for k, v in expected.items():
        assert k in adj, f"missing node {k} in adjacency"
        assert adj[k] == v, f"adj[{k}] expected {v} but got {adj[k]}"

    # ログ出力（JSON）
    logger.info("adjacency (q=1, root=8, depth=3) = %s", json.dumps(adj, ensure_ascii=False))

def test_expr_strings_q1():
    """
    子ノードに付与される SymPy 文字列表現と LaTeX を確認。
    """
    Q = [None, 1]
    tree = build_tree(root_value=16, Q=Q, depth=1, p=3)
    children = tree["children"]
    vals = {c["value"]: c for c in children}

    # 偶数側: 32, 式は "2*n", latex "2 n"
    assert 32 in vals
    assert vals[32]["expr"]["text"] == "2*n"
    assert vals[32]["expr"]["latex"] == "2 n"

    # 奇数側: 5, 式は "(n - 1)/3", latex "\frac{n - 1}{3}"
    assert 5 in vals
    assert vals[5]["expr"]["text"] == "(n - 1)/3"
    assert vals[5]["expr"]["latex"] in (r"\frac{n - 1}{3}", r"\frac{n-1}{3}")

def test_reverse_tree_q5_depth2_structure_and_logging():
    """
    拡張コラッツ (q=5) で root=8, depth=2 の逆木：
    8→[16,1], 16→[32], 1→[2]
    """
    Q = [None, 5]
    tree = build_tree(root_value=8, Q=Q, depth=2, p=3)
    adj = to_adjacency(tree)

    expected = {
        8:  [16, 1],
        16: [32],
        1:  [2],
    }
    for k, v in expected.items():
        assert k in adj
        assert adj[k] == v

    logger.info("adjacency (q=5, root=8, depth=2) = %s", json.dumps(adj, ensure_ascii=False))

def test_no_zero_or_negative_values_in_tree():
    """
    生成ノードが正の整数のみであることを確認。
    """
    Q = [None, 1]
    tree = build_tree(root_value=8, Q=Q, depth=4, p=3)

    def collect(node):
        out = [node["value"]]
        for c in node["children"]:
            out += collect(c)
        return out

    vals = collect(tree)
    assert all(isinstance(v, int) and v > 0 for v in vals)
