USED_TOKENS = set()

def is_token_used(token):
    return token in USED_TOKENS

def mark_token_used(token):
    USED_TOKENS.add(token)