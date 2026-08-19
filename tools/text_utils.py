def text_utility(text: str, operation: str):
    """Perform basic text analysis."""

    if not text or not text.strip():
        return {
            "success": False,
            "error": "Text cannot be empty."
        }

    text = text.strip()

    if operation == "word_count":
        return {
            "success": True,
            "operation": operation,
            "result": len(text.split())
        }

    if operation == "character_count":
        return {
            "success": True,
            "operation": operation,
            "result": len(text)
        }

    if operation == "uppercase":
        return {
            "success": True,
            "operation": operation,
            "result": text.upper()
        }

    if operation == "lowercase":
        return {
            "success": True,
            "operation": operation,
            "result": text.lower()
        }

    if operation == "reverse":
        return {
            "success": True,
            "operation": operation,
            "result": text[::-1]
        }

    return {
        "success": False,
        "error": f"Unknown operation: {operation}"
    }