from datetime import date, timedelta

SHIPPING_DAYS = {"standard": 5, "express": 2}


def add_business_days(start: date, days: int) -> date:
    current = start
    added = 0
    while added < days:
        current += timedelta(days=1)
        if current.weekday() > 5:  # skip weekends
            continue
        added += 1
    return current


def estimated_delivery(order_date: date, shipping: str = "standard") -> date:
    if shipping not in SHIPPING_DAYS:
        raise ValueError(f"unknown shipping method: {shipping}")
    return add_business_days(order_date, SHIPPING_DAYS[shipping])
