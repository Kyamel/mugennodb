from enum import Enum

# =======================================
# Enums para os tipos do banco
# =======================================

class EUserRole(str, Enum):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

class EComicType(str, Enum):
    MANGA = 'manga'
    MANHWA = 'manhwa'
    MANHUA = 'manhua'
    DOUJINSHI = 'doujinshi'
    NOVEL = 'novel'

class EMangaStatus(str, Enum):
    ONGOING = 'ongoing'
    COMPLETED = 'completed'
    HIATUS = 'hiatus'
    CANCELLED = 'cancelled'

class EAgeRating(str, Enum):
    G = 'G'
    PG_12 = 'PG-12'
    R15 = 'R15+'
    R18 = 'R18+'

class ELinkType(str, Enum):
    PURCHASE = 'purchase'
    OFFICIAL = 'official'
    COMMUNITY = 'community'
    INFORMATION = 'information'

class EReadingStatus(str, Enum):
    PLANNING = 'planning'
    READING = 'reading'
    COMPLETED = 'completed'
    DROPPED = 'dropped'

class EFlagStatus(str, Enum):
    PENDING = 'pending'
    REVIEWED = 'reviewed'
    DISMISSED = 'dismissed'
    ACCEPTED = 'accepted'

class EMangaRelationshipType(str, Enum):
    MAIN_STORY = 'main_story'
    PREQUEL = 'prequel'
    SEQUEL = 'sequel'
    SIDE_STORY = 'side_story'
    SPIN_OFF = 'spin_off'
    ADAPTATION = 'adaptation'
    ALTERNATIVE_VERSION = 'alternative_version'
    CHARACTER = 'character'
    OVA = 'ova'
    SPECIAL = 'special'
    ONESHOT = 'oneshot'
    DOUJINSHI = 'doujinshi'
