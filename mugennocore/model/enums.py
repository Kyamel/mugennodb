from enum import Enum

# =======================================
# Enums para os tipos do banco
# =======================================

class EUserRole(str, Enum):
    ADMIN = 'ADMIN'
    MODERATOR = 'MODERATOR'
    USER = 'USER'

class EComicType(str, Enum):
    MANGA = 'MANGA'
    MANHWA = 'MANHWA'
    MANHUA = 'MANHUA'
    DOUJINSHI = 'DOUJINSHI'
    NOVEL = 'NOVEL'

class EMangaStatus(str, Enum):
    ONGOING = 'ONGOING'
    COMPLETED = 'COMPLETED'
    HIATUS = 'HIATUS'
    CANCELLED = 'CANCELLED'

class EAgeRating(str, Enum):
    G = 'G'
    PG12 = 'PG12'
    R15 = 'R15+'
    R18 = 'R18+'

class ELinkType(str, Enum):
    PURCHASE = 'PURCHASE'
    OFFICIAL = 'OFFICIAL'
    COMMUNITY = 'COMMUNITY'
    INFORMATION = 'INFORMATION'

class EReadingStatus(str, Enum):
    PLANNING = 'PLANNING'
    READING = 'READING'
    COMPLETED = 'COMPLETED'
    DROPPED = 'DROPPED'

class EFlagStatus(str, Enum):
    PENDING = 'PENDING'
    REVIEWED = 'REVIEWED'
    DISMISSED = 'DISMISSED'
    ACCEPTED = 'ACCEPTED'

class EMangaRelationshipType(str, Enum):
    MAIN_STORY = 'MAIN_STORY'
    PREQUEL = 'PREQUEL'
    SEQUEL = 'SEQUEL'
    SIDE_STORY = 'SIDE_STORY'
    SPIN_OFF = 'SPIN_OFF'
    ADAPTATION = 'ADAPTATION'
    ALTERNATIVE_VERSION = 'ALTERNATIVE_VERSION'
    CHARACTER = 'CHARACTER'
    OVA = 'OVA'
    SPECIAL = 'SPECIAL'
    ONESHOT = 'ONESHOT'
    DOUJINSHI = 'DOUJINSHI'
