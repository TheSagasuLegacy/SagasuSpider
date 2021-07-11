import json
from datetime import datetime
from enum import IntEnum
from typing import List, Optional

import dateparser
from pydantic import validator
from pydantic.fields import Field
from pydantic.main import BaseModel, Extra


class DataModel(BaseModel):
    class Config:
        extra = Extra.allow


class UploadModel(BaseModel):
    def export(self, **kwargs):
        return json.loads(self.json(**kwargs))


class BangumiSubjectType(IntEnum):
    Book = 1
    Anime = 2
    Music = 3
    Game = 4
    Real = 6


class BangumiEpisodeType(IntEnum):
    Main = 0
    Special = 1
    Opening = 2
    Ending = 3
    Advertising = 4
    MAD = 5
    Other = 6


class BangumiEpisode(DataModel):
    id: int
    type: BangumiEpisodeType
    name: Optional[str] = None
    name_cn: Optional[str] = None
    sort: float
    air_date: Optional[datetime] = Field(alias="airdate")

    @validator("name", "name_cn")
    def validate_string(cls, value):
        if not isinstance(value, str):
            return None
        stripped = value.strip()
        return stripped if stripped else None

    @validator("air_date", pre=True)
    def validate_date(cls, value):
        return dateparser.parse(value) if isinstance(value, str) else value


class BangumiSubject(DataModel):
    id: int
    type: BangumiSubjectType
    name: str
    name_cn: Optional[str] = None
    summary: Optional[str] = None
    air_date: Optional[datetime] = None
    eps: List[BangumiEpisode] = []

    @validator("name_cn", "summary")
    def validate_string(cls, value):
        if not isinstance(value, str):
            return None
        stripped = value.strip()
        return stripped if stripped else None

    @validator("eps", pre=True)
    def validate_eps(cls, value):
        return value if isinstance(value, list) else []

    @validator("air_date", pre=True)
    def validate_date(cls, value):
        return dateparser.parse(value) if isinstance(value, str) else value


class CreateSagasuSeries(UploadModel):
    name: str
    name_cn: Optional[str] = None
    description: Optional[str] = None
    air_date: Optional[datetime] = None
    bangumi_id: int


class ReadSagasuSeries(CreateSagasuSeries):
    id: int


class CreateSagasuEpisodes(UploadModel):
    name: Optional[str] = None
    name_cn: Optional[str] = None
    sort: float
    type: BangumiEpisodeType
    series: int
    air_date: Optional[datetime] = None


class ReadSagasuEpisodes(CreateSagasuEpisodes):
    id: int
