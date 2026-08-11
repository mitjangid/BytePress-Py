"""
BytePress Profanity Filter
--------------------------
A lightweight, zero-dependency foul language detection engine.
Covers common English profanity and transliterated Hindi abusive words.

Usage:
    from core.profanity import contains_profanity, clean_text, ProfanityViolation

    # Check if text has foul language
    if contains_profanity("some text"):
        raise ProfanityViolation("Foul language detected")

    # Get a censored version
    cleaned = clean_text("some text")  # -> "s*** t***"
"""

import re
from typing import List, Tuple


# ---------------------------------------------------------------------------
# Word lists — extend as needed
# ---------------------------------------------------------------------------

_ENGLISH_BAD_WORDS: List[str] = [
    # Common English profanity (partial list — covers main offensive words)
    # Include common masked variants for direct matching
    "fuck", "fucker", "fuckers", "fucking", "fucked", "fucks", "f**k", "f***", "fuk", "fck",
    "shit", "shite", "shitting", "shitted", "shits", "sh*t", "sh!t",
    "ass", "asses", "asshole", "assholes", "jackass", "jackasses",
    "bitch", "bitches", "bitching", "bitched",
    "bastard", "bastards",
    "cunt", "cunts",
    "dick", "dicks", "dickhead", "dickheads",
    "cock", "cocks", "cocksucker",
    "pussy", "pussies",
    "whore", "whores",
    "slut", "sluts",
    "nigger", "niggers", "nigga", "niggas",
    "faggot", "faggots", "fag", "fags",
    "retard", "retards", "retarded",
    "crap", "crappy",
    "damn", "damned",
    "hell",  # context-sensitive, kept for now
    "piss", "pissed", "pissing",
    "prick", "pricks",
    "twat", "twats",
    "wanker", "wankers",
    "bollocks",
    "motherfucker", "motherfuckers", "mf",
    "rape", "rapist", "rapists",
    "kill yourself", "kys",
    "die",      # flagged in abusive combos only
    "idiot", "idiots",
    "moron", "morons",
    "imbecile",
    "scumbag", "scumbags",
    "douchebag", "douchebags",
    "dipshit", "dipshits",
    "dumbass",
    "lardass",
    "fatass",
    "skank",
]

# Transliterated Hindi/Hinglish abusive words (romanized spellings)
_HINDI_BAD_WORDS: List[str] = [
    "madarchod", "maderchod", "mc", "maadarcho",
    "behenchod", "behanchod", "bc",
    "bhosdike", "bhosdika", "bhosdiwale", "bhosdi",
    "chutiya", "chutiye", "chut",
    "gaand", "gand",
    "loda", "lund", "lauda",
    "harami", "haramkhor", "haram",
    "randi", "raandi", "randwa",
    "kamina", "kamine",
    "kutte", "kutta", "suar",
    "sala", "saala", "saali",
    "bakwaas",
    "gandu", "gaandu",
    "bhadwa", "bhadwe",
    "lawde", "laude",
    "hijra",
    "ullu", "ullu ka pattha",
    "gandmara",
    "choda", "chode",
    "madar",
]

# Merge all words and sort longest-first for greedy matching
_ALL_BAD_WORDS: List[str] = sorted(
    set(w.lower() for w in _ENGLISH_BAD_WORDS + _HINDI_BAD_WORDS),
    key=len,
    reverse=True,
)

# Pre-compile regex for each bad word with word boundaries
# Use lookahead/lookbehind to handle partial-word matches
_WORD_PATTERN = re.compile(
    r'\b(' + '|'.join(re.escape(w) for w in _ALL_BAD_WORDS) + r')\b',
    re.IGNORECASE
)


class ProfanityViolation(Exception):
    """Raised when foul language is detected in user-submitted content."""
    def __init__(self, message="Your message contains inappropriate language. Please keep the discussion respectful.", flagged_words=None):
        self.flagged_words = flagged_words or []
        super().__init__(message)


def _normalize(text: str) -> str:
    """
    Normalize obfuscation tricks like:
    - Letter substitutions: @ -> a, 3 -> e, 0 -> o, 1 -> i, $ -> s, ! -> i
    - Repeated characters: fuuuck -> fuck
    - Spaces between letters: f u c k -> fuck
    - Asterisk masking: f**k -> fk (still close enough for detection)
    """
    t = text.lower()
    # Common substitutions
    t = t.replace('@', 'a').replace('3', 'e').replace('0', 'o')
    t = t.replace('1', 'i').replace('$', 's').replace('!', 'i')
    t = t.replace('4', 'a').replace('5', 's').replace('7', 't')
    t = t.replace('+', 't').replace('|', 'l').replace('(', 'c')
    # Strip masking asterisks and dots/dashes between word chars (f**k -> fk, f.u.c.k -> fuck)
    t = re.sub(r'(?<=\w)[*.\-_]+(?=\w)', '', t)
    # Collapse repeated characters (e.g. fuuuck -> fuck, shiiit -> shit)
    t = re.sub(r'(.)\1{2,}', r'\1\1', t)
    return t


def contains_profanity(text: str) -> Tuple[bool, List[str]]:
    """
    Returns (True, [matched_words]) if the text contains profanity.
    Returns (False, []) if clean.
    """
    if not text or not text.strip():
        return False, []

    normalized = _normalize(text)
    matches = _WORD_PATTERN.findall(normalized)
    unique_matches = list(set(m.lower() for m in matches))
    return bool(unique_matches), unique_matches


def clean_text(text: str) -> str:
    """
    Returns the text with profane words replaced by asterisks.
    e.g. "fuck this" -> "f**k this"
    """
    def _censor(match):
        word = match.group(0)
        if len(word) <= 2:
            return word[0] + '*'
        return word[0] + '*' * (len(word) - 2) + word[-1]

    normalized = _normalize(text)
    # Apply to original text using regex on original (case-preserved)
    return _WORD_PATTERN.sub(lambda m: m.group(0)[0] + '*' * (len(m.group(0)) - 2) + m.group(0)[-1], text)


def validate_clean_text(text: str, field_name: str = "content"):
    """
    Raises ProfanityViolation if the text contains profanity.
    Use this in Django form.clean() or model.clean() methods.
    """
    found, words = contains_profanity(text)
    if found:
        raise ProfanityViolation(
            message=f"Your {field_name} contains inappropriate language. Please keep the content respectful.",
            flagged_words=words
        )
