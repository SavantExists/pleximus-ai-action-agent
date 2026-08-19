import os
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types

from tools.calculator import calculate
from tools.weather import get_weather
from tools.text_utils import text_utility
from tools.currency import convert_currency

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


# ---------------------------------------------------------
# TOOL DEFINITIONS
# ---------------------------------------------------------

calculator_tool = types.FunctionDeclaration(
    name="calculate",
    description=(
        "Perform mathematical calculations. "
        "Use this whenever the user asks to calculate, "
        "add, subtract, multiply, divide, find percentages, "
        "or solve a numerical expression."
    ),
    parameters_json_schema={
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "Mathematical expression such as 25 * 4 + 10"
            }
        },
        "required": ["expression"]
    }
)


weather_tool = types.FunctionDeclaration(
    name="get_weather",
    description=(
        "Get current weather information for a city. "
        "Use this when the user asks about current weather, "
        "temperature, humidity, or wind."
    ),
    parameters_json_schema={
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "Name of the city"
            }
        },
        "required": ["city"]
    }
)


text_tool = types.FunctionDeclaration(
    name="text_utility",
    description=(
        "Perform operations on text. "
        "Can count words, count characters, convert to uppercase, "
        "convert to lowercase, or reverse text."
    ),
    parameters_json_schema={
        "type": "object",
        "properties": {
            "text": {
                "type": "string",
                "description": "Text to process"
            },
            "operation": {
                "type": "string",
                "enum": [
                    "word_count",
                    "character_count",
                    "uppercase",
                    "lowercase",
                    "reverse"
                ],
                "description": "Operation to perform"
            }
        },
        "required": ["text", "operation"]
    }
)


currency_tool = types.FunctionDeclaration(
    name="convert_currency",
    description=(
        "Convert an amount from one currency to another using "
        "current exchange rates. Use this whenever the user asks "
        "to convert money between currencies."
    ),
    parameters_json_schema={
        "type": "object",
        "properties": {
            "amount": {
                "type": "number",
                "description": "Amount of money to convert"
            },
            "from_currency": {
                "type": "string",
                "description": "Three-letter source currency code, e.g. USD"
            },
            "to_currency": {
                "type": "string",
                "description": "Three-letter target currency code, e.g. INR"
            }
        },
        "required": [
            "amount",
            "from_currency",
            "to_currency"
        ]
    }
)


tool_definitions = types.Tool(
    function_declarations=[
        calculator_tool,
        weather_tool,
        text_tool,
        currency_tool
    ]
)


# ---------------------------------------------------------
# TOOL EXECUTION
# ---------------------------------------------------------

def execute_tool(name, args):

    if name == "calculate":
        return calculate(args["expression"])

    if name == "get_weather":
        return get_weather(args["city"])

    if name == "text_utility":
        return text_utility(
            args["text"],
            args["operation"]
        )
    if name == "convert_currency":
        return convert_currency(
            args["amount"],
            args["from_currency"],
            args["to_currency"]
        )

    return {
        "success": False,
        "error": f"Unknown tool: {name}"
    }


# ---------------------------------------------------------
# AGENT
# ---------------------------------------------------------

def ask_agent(user_message):

    response = client.models.generate_content(
        model="gemini-3.6-flash",

        contents=user_message,

        config=types.GenerateContentConfig(
            system_instruction=(
                "You are a helpful AI action agent. "

                "You have access to several tools. "
                "Always use a tool when the user's request requires "
                "real calculation, current information, or text processing. "

                "Never invent results that a tool can provide. "

                "If the user asks for multiple independent actions "
                "in one message, identify and execute ALL required tools "
                "before giving the final answer. "

                "For example, if the user asks for weather AND currency "
                "conversion, call both tools. "

                "After receiving all tool results, provide one clear "
                "natural-language response."
            ),

            tools=[tool_definitions]
        )
    )

    # -----------------------------------------------------
    # NO TOOL NEEDED
    # -----------------------------------------------------

    if not response.function_calls:
        return response.text

    # -----------------------------------------------------
    # EXECUTE ALL REQUESTED TOOLS
    # -----------------------------------------------------

    tool_response_parts = []

    for function_call in response.function_calls:

        tool_name = function_call.name
        tool_args = dict(function_call.args)

        print(f"\n🔧 Tool selected: {tool_name}")
        print(f"📥 Arguments: {tool_args}")

        try:
            tool_result = execute_tool(
                tool_name,
                tool_args
            )

        except Exception as e:
            tool_result = {
                "success": False,
                "error": str(e)
            }

        print(f"📤 Tool result: {tool_result}")

        tool_response_parts.append(
            types.Part.from_function_response(
                name=tool_name,
                response=tool_result
            )
        )

    # -----------------------------------------------------
    # SEND ALL TOOL RESULTS BACK TO GEMINI
    # -----------------------------------------------------

    final_response = client.models.generate_content(
        model="gemini-3.6-flash",

        contents=[
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text=user_message
                    )
                ]
            ),

            response.candidates[0].content,

            types.Content(
                role="user",
                parts=tool_response_parts
            )
        ],

        config=types.GenerateContentConfig(
            system_instruction=(
                "You are a helpful AI assistant. "

                "Use the tool results provided to answer the user's "
                "original request. "

                "If multiple tools were used, combine ALL of their "
                "results into the final answer. "

                "Do not invent values or perform your own calculations "
                "when a tool result is available. "

                "Clearly mention if any tool failed."
            )
        )
    )

    return final_response.text