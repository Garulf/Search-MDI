import json
import subprocess
import sys
from pathlib import Path

RUN_PY = Path(__file__).resolve().parents[1] / "src" / "run.py"


def test_plugin_answers_a_json_rpc_query():
    requests = [
        {"jsonrpc": "2.0", "id": 1, "method": "query", "params": [{"search": "home", "actionKeyword": "mdi"}, {}]},
        {"jsonrpc": "2.0", "id": 2, "method": "close", "params": []},
    ]
    stdin = "".join(json.dumps(request) + "\n" for request in requests)
    completed = subprocess.run(
        [sys.executable, str(RUN_PY)], input=stdin, capture_output=True, text=True, timeout=120, check=True
    )
    responses = {message["id"]: message for message in map(json.loads, completed.stdout.splitlines())}
    titles = [result["Title"] for result in responses[1]["result"]["result"]]
    assert "home" in titles
    assert responses[2]["result"] == {}
