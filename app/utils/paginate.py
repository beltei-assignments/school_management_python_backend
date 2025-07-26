def getSkip(page: int = 1, limit: int = 10) -> int:
    skip = (page - 1) * limit

    return skip
