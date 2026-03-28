import calendar
import csv
import json
import os
from datetime import date, datetime

import requests

print("================================================")
print("Note: This is for JustMySocks API.")
print("================================================")


def _last_reset_date(today: date, reset_day: int) -> date:
    """Return the billing cycle start (last reset date) for today."""
    if today.day >= reset_day:
        y, m = today.year, today.month
    else:
        if today.month == 1:
            y, m = today.year - 1, 12
        else:
            y, m = today.year, today.month - 1
    _, last_dom = calendar.monthrange(y, m)
    d = min(reset_day, last_dom)
    return date(y, m, d)


def get_bandwidth():
    """
    Fetch bandwidth from API. Returns a dict with usage metrics, or None on failure.
    Keys: used_mb, limit_mb, used_pct, reset_day, days_in_cycle, avg_mb_per_day, avg_pct_per_day.
    """
    api_url = os.environ.get("CHECK_API")
    if not api_url:
        print("CHECK_API environment variable is not set")
        return None

    try:
        response = requests.get(api_url)
        text = response.text.strip()
        # API returns JSON: monthly_bw_limit_b, bw_counter_b, bw_reset_day_of_month
        data = json.loads(text)
        used_bytes = int(data["bw_counter_b"])
        limit_b = int(data["monthly_bw_limit_b"])
        reset_day = int(data["bw_reset_day_of_month"])

        used_gb = used_bytes / (1024**3)
        limit_gb = limit_b / (1024**3)

        print(
            f"Bandwidth used: {used_gb:.2f} / {limit_gb:.2f} GB (resets day {reset_day})"
        )
        used_mb = used_bytes / (1024**2)
        limit_mb = limit_b / (1024**2)
        print(f"(Namely {used_mb:.2f} MB)")

        used_pct = (used_mb / limit_mb * 100) if limit_mb else 0.0
        today = date.today()
        cycle_start = _last_reset_date(today, reset_day)
        days_in_cycle = max(1, (today - cycle_start).days + 1)
        avg_mb_per_day = used_mb / days_in_cycle
        avg_pct_per_day = used_pct / days_in_cycle

        print(f"Data usage: {used_pct:.2f}% of monthly limit")
        print(f"Days in current billing cycle (approx.): {days_in_cycle}")
        print(f"Average data usage per day: {avg_mb_per_day:.2f} MB")
        print(
            f"Average share of monthly quota used per day: {avg_pct_per_day:.4f}%"
        )

        return {
            "used_mb": used_mb,
            "limit_mb": limit_mb,
            "used_pct": used_pct,
            "reset_day": reset_day,
            "days_in_cycle": days_in_cycle,
            "avg_mb_per_day": avg_mb_per_day,
            "avg_pct_per_day": avg_pct_per_day,
        }

    except Exception as e:
        print(f"Query failed: {e}")
        return None


_CSV_FIELDNAMES = [
    "date",
    "time",
    "data_usage_mb",
    "data_usage_pct",
    "avg_data_usage_per_day_mb",
    "avg_data_usage_pct_per_day",
]


def _csv_row_from_record(record: dict, now: datetime) -> dict[str, str]:
    return {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "data_usage_mb": f"{record['used_mb']:.4f}",
        "data_usage_pct": f"{record['used_pct']:.4f}",
        "avg_data_usage_per_day_mb": f"{record['avg_mb_per_day']:.6f}",
        "avg_data_usage_pct_per_day": f"{record['avg_pct_per_day']:.8f}",
    }


def _count_rows_for_date(csv_path: str, date_str: str) -> int:
    """Return how many data rows in the CSV have the given date column."""
    if not os.path.isfile(csv_path) or os.path.getsize(csv_path) == 0:
        return 0
    n = 0
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            return 0
        for r in reader:
            if r and r.get("date") == date_str:
                n += 1
    return n


def _input_yes_default(prompt: str) -> bool:
    """True unless the user explicitly answers n or no (empty line counts as yes)."""
    s = input(prompt).strip().lower()
    return s not in ("n", "no")


def _append_record_csv(record: dict, csv_path: str, *, overwrite_today: bool) -> None:
    """
    Write one row to data_usage.csv.
    If overwrite_today is True, drop existing rows whose date is today, then write the new row.
    Otherwise append only (multiple rows per day are allowed).
    """
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    row = _csv_row_from_record(record, now)

    if overwrite_today and os.path.isfile(csv_path) and os.path.getsize(csv_path) > 0:
        kept_rows: list[dict[str, str]] = []
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames:
                for r in reader:
                    if not r:
                        continue
                    if r.get("date") == today_str:
                        continue
                    kept_rows.append({k: (r.get(k) or "") for k in _CSV_FIELDNAMES})
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=_CSV_FIELDNAMES)
            writer.writeheader()
            writer.writerows(kept_rows)
            writer.writerow(row)
        print(
            f"Earlier records from {today_str} were removed (if any); "
            f"record written to {csv_path}"
        )
        return

    file_exists = os.path.isfile(csv_path)
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=_CSV_FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)
    print(f"Record appended to {csv_path}")


def main():
    result = get_bandwidth()
    if result is None:
        return

    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "output", "data_usage.csv")
    today_str = datetime.now().strftime("%Y-%m-%d")
    n_today = _count_rows_for_date(csv_path, today_str)

    if not _input_yes_default(
        "Do you want to save this query record to output/data_usage.csv? (Y/n): "
    ):
        print("Record not saved.")
        return

    overwrite_today = False
    if n_today > 0:
        overwrite_today = _input_yes_default(
            "Overwrite earlier records from today in the CSV? (Y/n): "
        )

    _append_record_csv(result, csv_path, overwrite_today=overwrite_today)


if __name__ == "__main__":
    main()
