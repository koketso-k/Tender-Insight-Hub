import datetime
from typing import Optional, List

def parse_date(date_str: str) -> Optional[datetime.date]:
    """
    Parses a date string in ISO format (YYYY-MM-DD) and returns a date object.
    Returns None if the format is invalid.
    """
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None


def filter_dict_keys(d: dict, keys: List[str]) -> dict:
    """
    Returns a new dict containing only the specified keys from the input dictionary.
    """
    return {k: d[k] for k in keys if k in d}


def format_currency(value: float, currency_symbol: str = 'R') -> str:
    """
    Formats a number as currency with two decimals.
    Example: 1500.5 -> "R 1,500.50"
    """
    return f"{currency_symbol} {value:,.2f}"


def calculate_match_score(criteria_met: int, total_criteria: int) -> float:
    """
    Calculates a suitability match score out of 100.
    """
    if total_criteria == 0:
        return 0.0
    return round((criteria_met / total_criteria) * 100, 2)


def paginate_list(items: list, page: int = 1, page_size: int = 20) -> dict:
    """
    Utility to paginate a list.
    Returns dict with keys: items (current page), total_items, total_pages, current_page
    """
    total_items = len(items)
    total_pages = (total_items + page_size - 1) // page_size
    start = (page - 1) * page_size
    end = start + page_size
    paged_items = items[start:end]

    return {
        "items": paged_items,
        "total_items": total_items,
        "total_pages": total_pages,
        "current_page": page,
    }
