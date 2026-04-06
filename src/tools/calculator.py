import ast
import math
from typing import Any, Dict, Callable


_ALLOWED_FUNCS: Dict[str, Callable[..., float]] = {
    "abs": abs,
    "round": round,
    "ceil": math.ceil,
    "floor": math.floor,
    "sqrt": math.sqrt,
    "log": math.log,
    "log10": math.log10,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
}

_ALLOWED_CONSTS: Dict[str, float] = {
    "pi": math.pi,
    "e": math.e,
}


def _format_number(x: float) -> str:
    if isinstance(x, bool):
        return str(x)
    if isinstance(x, int):
        return str(x)
    if isinstance(x, float) and x.is_integer():
        return str(int(x))
    return str(x)


def _eval_expr(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _eval_expr(node.body)

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return float(node.value)
        raise ValueError("Chỉ hỗ trợ số (int/float).")

    if isinstance(node, ast.Name):
        if node.id in _ALLOWED_CONSTS:
            return float(_ALLOWED_CONSTS[node.id])
        raise ValueError(f"Biến không hợp lệ: {node.id}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval_expr(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +operand
        if isinstance(node.op, ast.USub):
            return -operand
        raise ValueError("Toán tử một ngôi không được hỗ trợ.")

    if isinstance(node, ast.BinOp):
        left = _eval_expr(node.left)
        right = _eval_expr(node.right)

        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            return left / right
        if isinstance(node.op, ast.FloorDiv):
            return left // right
        if isinstance(node.op, ast.Mod):
            return left % right
        if isinstance(node.op, ast.Pow):
            return left ** right

        raise ValueError("Toán tử không được hỗ trợ.")

    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Chỉ hỗ trợ gọi hàm dạng tên hàm, ví dụ: sqrt(9).")

        fn_name = node.func.id
        fn = _ALLOWED_FUNCS.get(fn_name)
        if fn is None:
            raise ValueError(f"Hàm không được hỗ trợ: {fn_name}")

        if node.keywords:
            raise ValueError("Không hỗ trợ tham số keyword, chỉ hỗ trợ positional args.")

        args = [_eval_expr(a) for a in node.args]
        return float(fn(*args))

    raise ValueError("Biểu thức không hợp lệ hoặc không được hỗ trợ.")


def calculator(expression: str) -> str:
    """
    Công cụ máy tính (an toàn) để agent gọi.

    Supports:
    - Operators: +, -, *, /, //, %, **, parentheses
    - Constants: pi, e
    - Functions: abs, round, ceil, floor, sqrt, log, log10, sin, cos, tan, asin, acos, atan

    Args:
        expression: Chuỗi biểu thức toán học. Ví dụ: "2*(3+4)", "sqrt(9)+1", "sin(pi/2)"

    Returns:
        Kết quả dưới dạng chuỗi, hoặc thông báo lỗi nếu expression không hợp lệ.
    """
    if not isinstance(expression, str) or not expression.strip():
        return "Lỗi: expression phải là chuỗi không rỗng."

    try:
        tree = ast.parse(expression, mode="eval")
        value = _eval_expr(tree)
        if math.isfinite(value):
            return _format_number(value)
        return "Lỗi: kết quả không hữu hạn (inf/nan)."
    except ZeroDivisionError:
        return "Lỗi: chia cho 0."
    except SyntaxError:
        return "Lỗi: cú pháp không hợp lệ."
    except Exception as e:
        return f"Lỗi: {e}"

