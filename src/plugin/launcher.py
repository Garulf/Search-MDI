from pyflowlauncher import FlowLauncherV2


class KeywordLauncher(FlowLauncherV2):
    """FlowLauncherV2 that remembers the action keyword of the last query.

    pyflowlauncher 1.2.2 only hands ``Query.search`` to query handlers, but
    auto-complete text has to include the keyword the user typed.
    """

    def __init__(self) -> None:
        super().__init__()
        self.action_keyword = ""
        messages = self._client.messages

        async def track_action_keyword():
            async for request in messages():
                params = request.get("params") or []
                if request.get("method") == "query" and params and isinstance(params[0], dict):
                    self.action_keyword = params[0].get("actionKeyword") or ""
                yield request

        self._client.messages = track_action_keyword
