import math
import operator
from typing import Dict, Any, Union, List
from models.schema import Tool

# Define allowed operators and their corresponding functions
OPERATORS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '%': operator.mod,
    '^': operator.pow,
    'sqrt': math.sqrt,
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'log': math.log10,
    'ln': math.log,
    'abs': abs,
}

async def calculate(expression: str) -> Dict[str, Any]:
    """
    Evaluate a mathematical expression
    
    Args:
        expression: Mathematical expression as a string
        
    Returns:
        Dictionary containing result or error message
    """
    try:
        # For security reasons, we don't use eval()
        # Instead, implement a simple parser for basic arithmetic
        # This is a simplified implementation and not suitable for complex expressions
        
        # Replace common mathematical functions with their values
        expression = expression.replace("pi", str(math.pi))
        expression = expression.replace("e", str(math.e))
        
        # This is a basic example - in a real application, 
        # you would implement a proper expression parser
        # For this POC, we'll assume simple expressions like "2 + 2" or "5 * 3"
        
        # Split by operators and parse
        tokens = []
        current_token = ""
        
        for char in expression:
            if char in "+-*/^%()":
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
                tokens.append(char)
            elif char.isdigit() or char == '.':
                current_token += char
            elif char.isspace():
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
            else:
                # For simplicity, we'll just handle basic operators
                return {"error": f"Unsupported character in expression: {char}"}
        
        if current_token:
            tokens.append(current_token)
        
        # For this POC, we'll just handle simple expressions like "2 + 2"
        # A full implementation would include a proper expression parser
        if len(tokens) == 3 and tokens[1] in OPERATORS:
            left = float(tokens[0])
            op = tokens[1]
            right = float(tokens[2])
            
            result = OPERATORS[op](left, right)
            return {
                "expression": expression,
                "result": result,
                "formatted_result": f"{result:g}"  # Clean formatting for floats
            }
        else:
            # For more complex expressions, suggest using a library like sympy
            return {"error": "Only simple expressions like '2 + 2' are supported in this POC"}
        
    except (ValueError, ZeroDivisionError, TypeError) as e:
        return {"error": f"Calculation error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

def register_calculator_tool(mcp_server):
    """Register the calculator tool with the MCP server"""
    calculator_tool = Tool(
        name="calculate",
        description="Evaluate a mathematical expression",
        parameters={
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression to evaluate, e.g., '2 + 2', '5 * 3'"
                }
            },
            "required": ["expression"]
        },
        function=calculate
    )
    
    mcp_server.register_tool(calculator_tool)
