from typing import Protocol, Optional, List, Dict, Any, Union
from datetime import datetime, date
from uuid import UUID
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
    OTHER = 'other'

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

# =======================================
# Interfaces Base
# =======================================

class DatabaseEntity(Protocol):
    """Interface base para todas as entidades do banco"""
    
    def __str__(self) -> str:
        ...
    
    def __repr__(self) -> str:
        ...
    
    def serialize(self) -> Dict[str, Any]:
        """Serializa o objeto para dicionário"""
        ...

# =======================================
# Tabelas Base
# =======================================

class ICountry(DatabaseEntity):
    id: int
    locale_code: str
    created_at: datetime
    updated_at: datetime

class IUser(DatabaseEntity):
    id: UUID
    country_id: int
    username: str
    email: str
    password_hash: str
    role: EUserRole
    nickname: Optional[str]
    profile_bio: Optional[str]
    profile_banner: Optional[str]
    karma_score: int
    is_active: bool
    is_banned: bool
    allow_nsfw: bool
    created_at: datetime
    updated_at: datetime

# =======================================
# Sistema Social
# =======================================

class IUserFollow(DatabaseEntity):
    follower_id: UUID
    following_id: UUID
    created_at: datetime

class IUserBlock(DatabaseEntity):
    blocker_id: UUID
    blocked_id: UUID
    created_at: datetime

# =======================================
# Mangás e Capítulos
# =======================================

class IComicTypeEntity(DatabaseEntity):
    id: int
    name: str
    description: Optional[str]

class IManga(DatabaseEntity):
    id: UUID
    country_id: int
    user_id: UUID
    title_english: str
    title_native: str
    release_date: date
    finish_date: Optional[date]
    age_rating: EAgeRating
    status: EMangaStatus
    comic_type_id: int
    mal_id: Optional[int]
    kitsu_id: Optional[int]
    created_at: datetime
    updated_at: datetime

class IMangaExternalLink(DatabaseEntity):
    id: UUID
    manga_id: UUID
    link_type: ELinkType
    url: str
    title: Optional[str]
    description: Optional[str]
    user_id: UUID
    is_approved: bool
    created_at: datetime
    updated_at: datetime

class IChapter(DatabaseEntity):
    id: UUID
    manga_id: UUID
    user_id: UUID
    country_id: int
    title: str
    cover_url: str
    ch_number: float
    created_at: datetime
    updated_at: datetime

# =======================================
# Staff e Roles
# =======================================

class IStaffProfile(DatabaseEntity):
    id: UUID
    user_id: Optional[UUID]
    name: Optional[str]
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

class IStaffRole(DatabaseEntity):
    id: int
    name: str
    description: Optional[str]

class IMangaStaff(DatabaseEntity):
    id: UUID
    manga_id: UUID
    staff_profile_id: UUID
    staff_role_id: int
    created_at: datetime
    updated_at: datetime

# =======================================
# Tags
# =======================================

class ITag(DatabaseEntity):
    id: int
    name: str
    created_at: datetime

class IContentTagging(DatabaseEntity):
    """Interface base para tagging de conteúdo"""
    user_id: UUID
    tag_id: int
    created_at: datetime

class IMangaTag(IContentTagging):
    manga_id: UUID

class IDiscussionTag(IContentTagging):
    discussion_id: UUID

class IChapterTag(IContentTagging):
    chapter_id: UUID

# =======================================
# Grupos
# =======================================

class IGroup(DatabaseEntity):
    id: UUID
    owner_id: UUID
    name: str
    description: Optional[str]
    is_open: bool
    created_at: datetime
    updated_at: datetime

class IGroupMember(DatabaseEntity):
    group_id: UUID
    user_id: UUID
    is_moderator: bool
    created_at: datetime

# =======================================
# Discussões e Comentários
# =======================================

class IDiscussion(DatabaseEntity):
    id: UUID
    manga_id: Optional[UUID]
    chapter_id: Optional[UUID]
    group_id: Optional[UUID]
    user_id: UUID
    country_id: int
    title: str
    content: str
    is_read_only: bool
    is_mod_only: bool
    is_deleted: bool
    karma_score: int
    created_at: datetime
    updated_at: datetime

class IDiscussionVote(DatabaseEntity):
    discussion_id: UUID
    user_id: UUID
    vote: int
    created_at: datetime

class IDiscussionRead(DatabaseEntity):
    discussion_id: UUID
    user_id: UUID
    last_read_at: datetime

class IComment(DatabaseEntity):
    id: UUID
    discussion_id: UUID
    user_id: UUID
    content: str
    reply_to: Optional[UUID]
    karma_score: int
    created_at: datetime
    updated_at: datetime

class ICommentVote(DatabaseEntity):
    comment_id: UUID
    user_id: UUID
    vote: int
    created_at: datetime

# =======================================
# Anexos
# =======================================

class IAttachmentType(DatabaseEntity):
    id: int
    name: str
    mime_type: Optional[str]
    icon_url: Optional[str]

class IAttachment(DatabaseEntity):
    id: UUID
    target_type: str
    target_id: UUID
    file_name: str
    file_url: str
    type_id: int
    file_size: Optional[int]
    created_at: datetime

# =======================================
# Reviews e Progresso de Leitura
# =======================================

class IReview(DatabaseEntity):
    user_id: UUID
    manga_id: UUID
    status: EReadingStatus
    score: Optional[int]
    review: Optional[str]
    created_at: datetime
    updated_at: datetime

class IReadingProgress(DatabaseEntity):
    user_id: UUID
    chapter_id: UUID
    status: EReadingStatus
    score: Optional[int]
    review: Optional[str]
    created_at: datetime
    updated_at: datetime

# =======================================
# Notificações e Flags
# =======================================

class INotification(DatabaseEntity):
    id: UUID
    user_id: UUID
    target_type: str
    target_id: UUID
    type: str
    title: str
    content: Optional[str]
    is_read: bool
    created_at: datetime

class IFlag(DatabaseEntity):
    id: UUID
    target_type: str
    target_id: UUID
    user_id: UUID
    reason: str
    status: EFlagStatus
    reviewed_by: Optional[UUID]
    reviewed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

