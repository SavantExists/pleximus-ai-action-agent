import requests


def convert_currency(amount: float, from_currency: str, to_currency: str):
    """Convert an amount between currencies using Frankfurter."""

    try:
        from_currency = from_currency.upper().strip()
        to_currency = to_currency.upper().strip()

        if amount < 0:
            return {
                "success": False,
                "error": "Amount cannot be negative."
            }

        if from_currency == to_currency:
            return {
                "success": True,
                "amount": amount,
                "from_currency": from_currency,
                "to_currency": to_currency,
                "rate": 1,
                "converted_amount": amount
            }

        url = (
            f"https://api.frankfurter.dev/v2/rate/"
            f"{from_currency}/{to_currency}"
        )

        response = requests.get(url, timeout=10)

        if response.status_code == 404:
            return {
                "success": False,
                "error": (
                    f"Currency pair {from_currency}/{to_currency} "
                    "was not found."
                )
            }

        response.raise_for_status()

        data = response.json()

        rate = float(data["rate"])
        converted = amount * rate

        return {
            "success": True,
            "amount": amount,
            "from_currency": from_currency,
            "to_currency": to_currency,
            "rate": rate,
            "converted_amount": round(converted, 2),
            "date": data.get("date")
        }

    except requests.RequestException as e:
        return {
            "success": False,
            "error": f"Currency service unavailable: {str(e)}"
        }

    except (ValueError, KeyError) as e:
        return {
            "success": False,
            "error": f"Invalid currency data: {str(e)}"
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected currency error: {str(e)}"
        }