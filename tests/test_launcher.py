import asyncio

from pyflowlauncher.jsonrpc import JsonRPCV2Client

from launcher import KeywordLauncher


def test_action_keyword_is_tracked_from_query_requests(monkeypatch):
    requests = [
        {"id": 1, "method": "query", "params": [{"search": "home", "actionKeyword": "icons"}, {}]},
        {"id": 2, "method": "context_menu", "params": [["home"]]},
        {"id": 3, "method": "query", "params": [{"search": "home", "actionKeyword": ""}, {}]},
    ]
    seen = []

    async def messages(self):
        for request in requests:
            yield request

    monkeypatch.setattr(JsonRPCV2Client, "messages", messages)
    launcher = KeywordLauncher()

    async def drain():
        async for request in launcher._client.messages():
            seen.append((request["id"], launcher.action_keyword))

    asyncio.run(drain())
    assert seen == [(1, "icons"), (2, "icons"), (3, "")]
