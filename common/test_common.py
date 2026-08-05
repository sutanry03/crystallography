# このファイルは test_script.py として保存します
# 簡単なテスト関数を含むPythonファイル

def add(a, b):
    """2つの数値を加算する関数"""
    return a + b

def multiply(a, b):
    """2つの数値を掛け算する関数"""
    return a * b

if __name__ == "__main__":
    # 基本的な関数テスト
    assert add(2, 3) == 5, "加算テスト失敗"
    assert multiply(2, 3) == 6, "掛け算テスト失敗"
