from pydantic import Field
from App.Objects.Mixins.Model import Model
from App.Objects.Misc.SavedVia import SavedVia
from typing import Optional
from datetime import datetime, timezone
from App.Objects.Relations.Link import Link
from App.Objects.Misc.Geo import Geo

class LocalObjectMeta(Model):
    # custom saved via
    saved_via: Optional[list[SavedVia]] = Field(default = [])
    allowed_to_link: list[str] = Field(default = None)
    dynamic_links: bool = Field(default = False)

    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    collection: Optional[bool] = Field(default=False)

    width: Optional[float] = Field(default = None)
    height: Optional[float] = Field(default = None)

    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    edited_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)
    # accessed_at: Optional[datetime] = Field(default=None)

    geo: Optional[list[Geo]] = Field(default = None)
    public: Optional[bool] = Field(default=False)
    role: Optional[list[str]] = Field(default = [])

    links: list[Link] = Field(default=[], exclude = True, repr = False)

    def make_public(self):
        self.public = True

    def set_edited(self):
        self.edited_at = datetime.now()

    def set_updated(self):
        self.updated_at = datetime.now()

    def make_possible_to_use_dynamic_links(self):
        self.dynamic_links = True
