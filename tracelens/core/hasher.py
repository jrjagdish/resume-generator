import hashlib

_HASH_PREFIX = "hash:"

def hash_endpoint(endpoint: str) -> str:
    """Hash the given endpoint using SHA-256 and return the hashed value.

    Args:
        endpoint (str): The endpoint to hash."""
    if not endpoint:
        return f"{_HASH_PREFIX}unknown"
    normalized = endpoint.strip().lower()
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    short_hash = digest[:8]

    return f"{_HASH_PREFIX}{short_hash}"
    