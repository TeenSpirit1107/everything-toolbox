import json
import os
import requests

print("================================================")
print("Note: This is for JustMySocks API.")
print("================================================")
def get_bandwidth():
    api_url = os.environ.get("CHECK_API")
    if not api_url:
        print("CHECK_API environment variable is not set")
        return

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

        print(f"📊 Bandwidth used: {used_gb:.2f} / {limit_gb:.2f} GB (resets day {reset_day})")
        used_mb = used_bytes / (1024**2)
        limit_mb = limit_b / (1024**2)
        print(f"(Namely {used_mb:.2f} MB)")

    except Exception as e:
        print(f"Query failed: {e}")


if __name__ == "__main__":
    get_bandwidth()
