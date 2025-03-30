import re

# 定義 Token 類型與對應的正則表達式
TOKEN_SPECIFICATION = [
    ('KEYWORD', r'\b(set|display|assuming|always|magic|if|let)\b'),  # 關鍵字
    ('BOOLEAN', r'\b(true|false)\b'),  # 布林值
    ('NULL', r'\b(null)\b'),  # 空值
    ('NUMBER', r'\d+(\.\d+)?'),  # 整數或浮點數
    ('STRING', r'"(?:\\.|[^"\\])*"'),  # 字串
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),  # 變數或函數名稱
    ('OPERATOR', r'[+\-*/%]'),  # 運算符
    ('COMPARISON', r'==|!=|>=|<=|>|<'),  # 比較運算符
    ('PUNCTUATION', r'[{}();,]'),  # 標點符號
    ('COMMENT', r'//.*'),  # 單行註解
    ('MULTI_COMMENT', r'/\*[\s\S]*?\*/'),  # 多行註解
    ('WHITESPACE', r'[ \t]+'),  # 空白符
    ('NEWLINE', r'\n'),  # 換行符
    ('ESCAPE_SEQUENCE', r'\\[nt\\]'),  # 轉義字符
    ('ERROR', r'[^\s]')  # 捕捉未識別的字符
]

# 編譯 Regex 模式
TOKEN_REGEX = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_SPECIFICATION)

def lexer(code):
    tokens = []
    for match in re.finditer(TOKEN_REGEX, code):
        kind = match.lastgroup  # Token 類型
        value = match.group()   # Token 值
        if kind == 'ERROR':  # 處理錯誤字符
            raise ValueError(f"Unrecognized token: {value}")
        if kind not in ('WHITESPACE', 'NEWLINE'):  # 忽略空白符和換行
            tokens.append((kind, value))
    return tokens

# 測試 Lexer
TEST_CASES = [
    ("set x = 42;", [('KEYWORD', 'set'), ('IDENTIFIER', 'x'), ('OPERATOR', '='), ('NUMBER', '42'), ('PUNCTUATION', ';')]),
    ("assuming x > 5 { display(\"Hello!\"); }", [
        ('KEYWORD', 'assuming'), ('IDENTIFIER', 'x'), ('COMPARISON', '>'), ('NUMBER', '5'), ('PUNCTUATION', '{'),
        ('IDENTIFIER', 'display'), ('PUNCTUATION', '('), ('STRING', '"Hello!"'), ('PUNCTUATION', ')'), ('PUNCTUATION', '}')
    ]),
    ("$%^ invalid_token", ValueError),
]

for source, expected in TEST_CASES:
    try:
        result = lexer(source)
        assert result == expected, f"Test failed for input: {source}\nExpected: {expected}\nGot: {result}"
        print(f"Test passed for input: {source}")
    except ValueError as e:
        if expected == ValueError:
            print(f"Test passed for error case: {source} -> {e}")
        else:
            print(e)
