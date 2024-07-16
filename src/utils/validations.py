from re import Match, match


def check_email(email: str) -> Match[str] | None:
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return match(regex, email)