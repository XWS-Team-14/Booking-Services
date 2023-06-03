import json
from uuid import UUID


class UUIDEncoder(json.JSONEncoder):
    def default(self, value) -> str:
        """JSON serialization conversion function."""
        if isinstance(value, UUID):
            return str(value)
        return super(UUIDEncoder, self).default(value)
