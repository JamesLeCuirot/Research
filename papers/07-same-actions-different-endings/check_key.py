"""Check that the OpenRouter key in .env works, without spending anything.

It calls OpenRouter's key-information endpoint, which costs nothing. It prints
whether the key works, its spending limit and what has been used so far. It
never prints the key itself.
"""
import json
import pathlib
import sys
import urllib.error
import urllib.request

env = pathlib.Path(__file__).with_name(".env")
key = ""
for line in env.read_text(encoding="utf-8").splitlines():
    if line.strip().startswith("OPENROUTER_API_KEY="):
        key = line.split("=", 1)[1].strip().strip('"').strip("'")

if not key:
    sys.exit("No key found yet: paste it after OPENROUTER_API_KEY= in .env and save.")

req = urllib.request.Request(
    "https://openrouter.ai/api/v1/key",
    headers={"Authorization": f"Bearer {key}"},
)
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r).get("data", {})
except urllib.error.HTTPError as e:
    sys.exit(f"OpenRouter rejected the key (HTTP {e.code}). Check it was pasted in full.")

print("Key works.")
print("  spend limit:  ", data.get("limit"), "(US dollars; None means no limit on the key)")
print("  used so far:  ", data.get("usage"))
print("  free tier:    ", data.get("is_free_tier"))

# Account credit balance: the prepaid money the key can draw on.
req = urllib.request.Request(
    "https://openrouter.ai/api/v1/credits",
    headers={"Authorization": f"Bearer {key}"},
)
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        c = json.load(r).get("data", {})
    bought, used = c.get("total_credits"), c.get("total_usage")
    print("  credits bought:", bought, "| used:", used)
except urllib.error.HTTPError as e:
    print(f"  (credit balance not available to this key: HTTP {e.code})")
