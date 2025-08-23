import pytest
from app.tree_builder import build_tree

@pytest.mark.parametrize("root,q,depth,expected_child,expected_expr", [
    # root=8, q=5 → (8-5)/3=1 が子に登場、式は (n - 5)/3
    (8, 5, 2, 1, "(n - 5)/3"),
    # root=8, q=1 → (8-1)/3=7 が子に登場、式は (n - 1)/3
    (8, 1, 2, 16, "2*n"),
])
def test_tree_with_q_and_expr(root, q, depth, expected_child, expected_expr):
    Q = [None, q]
    tree = build_tree(root, Q, depth)
    # 子ノードを抽出
    child_nodes = tree["children"]
    # 値の確認
    child_values = [c["value"] for c in child_nodes]
    print(f'q: {q}, chiled_values: {child_values}')
    assert expected_child in child_values
    # 該当ノードの式を確認
    exprs = [c["expr"]["text"] for c in child_nodes if c["value"] == expected_child]
    assert expected_expr in exprs

def test_tree_even_branch_always_present_and_expr():
    Q = [None, 5]
    tree = build_tree(8, Q, 1)
    child_nodes = tree["children"]
    # 偶数経路があるか確認
    even_child = [c for c in child_nodes if c["value"] == 16]
    assert even_child, "偶数経路が見つからない"
    # 式が "2*n" になっているか
    assert even_child[0]["expr"]["text"] == "2*n"
    assert even_child[0]["expr"]["latex"] == "2 n"
