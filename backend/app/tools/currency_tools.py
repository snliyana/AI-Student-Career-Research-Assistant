from langchain_core.tools import tool
import requests


@tool
def currency_converter_tool(query: str) -> str:
    """
    Convert currency using a simple input format.

    Example:
    1000 USD to MYR
    5000 SGD to MYR
    """

    try:
        parts = query.upper().split()

        if len(parts) != 4 or parts[2] != "TO":
            return (
                "Invalid format. "
                "Use format like: 1000 USD TO MYR"
            )

        amount = float(parts[0])
        from_currency = parts[1]
        to_currency = parts[3]

        url = (
            f"https://open.er-api.com/v6/latest/{from_currency}"
        )

        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get("result") != "success":
            return "Currency conversion service returned an error."

        rates = data.get("rates", {})

        if to_currency not in rates:
            return f"Currency {to_currency} is not supported."

        converted_amount = amount * rates[to_currency]

        return (
            f"{amount:.2f} {from_currency} = "
            f"{converted_amount:.2f} {to_currency}"
        )

    except Exception as e:
        return (
            "Currency conversion failed. "
            f"Error: {str(e)}"
        )