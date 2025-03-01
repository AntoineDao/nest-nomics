from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, field_validator


def parse_date(value):
    if value is None:
        return None
    for fmt in ('%d %B %Y', '%d %b %Y'):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError(
        f"time data '{value}' does not match any of the formats '%d %B %Y' or '%d %b %Y'")


class ImageInfo(BaseModel):
    imageUrl: str
    mediumImageUrl: str
    count: int


class Transaction(BaseModel):
    displayPrice: str
    dateSold: Optional[datetime] = None
    tenure: Optional[str] = None
    newBuild: bool

    @field_validator('dateSold', mode='before')
    def validate_date_sold(cls, value):
        return parse_date(value)


class Location(BaseModel):
    lat: float
    lng: float


class Property(BaseModel):
    address: str
    propertyType: Optional[str] = None
    bedrooms: Optional[int] = None
    imageInfo: Optional[ImageInfo] = None
    hasFloorPlan: bool
    transactions: List[Transaction]
    location: Location
    detailUrl: str


class SearchLocation(BaseModel):
    displayName: str
    searchName: str
    locationType: str
    locationId: int


class DisclaimerDate(BaseModel):
    earliestTransaction: Optional[datetime] = None
    mostRecentTransaction: Optional[datetime] = None
    lastLoadDate: Optional[datetime] = None

    @field_validator('earliestTransaction',
                     'mostRecentTransaction', 'lastLoadDate', mode='before')
    def validate_disclaimer_dates(cls, value):
        return parse_date(value)


class DisclaimerDates(BaseModel):
    disclaimerDatesMap: Dict[str, DisclaimerDate]


class Blurb(BaseModel):
    text: List[str]
    numberOfProperties: int
    numberOfTransactions: int
    earliestTransactionDate: Optional[datetime] = None
    latestTransactionDate: Optional[datetime] = None

    @field_validator('earliestTransactionDate',
                     'latestTransactionDate', mode='before')
    def validate_blurb_dates(cls, value):
        return parse_date(value)


class Pagination(BaseModel):
    current: int
    first: int
    last: int
    total: int
    sortBy: Optional[str] = None


class SoldPropertiesResponse(BaseModel):
    count: int
    metaTagDescription: str
    properties: List[Property]
    searchLocation: SearchLocation
    disclaimerDates: DisclaimerDates
    blurb: Optional[Blurb] = None
    pagination: Pagination
    localInfo: Optional[dict] = None
