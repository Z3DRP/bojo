

from bojojo.providers.db_session_provider import session_provider


class DbSession:
    def __init__(self):
        self.db = session_provider()