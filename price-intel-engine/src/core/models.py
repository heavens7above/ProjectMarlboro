from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class SearchQuery(BaseModel):
    term: str
    location_lat: Optional[float] = None
    location_long: Optional[float] = None
    pincode: Optional[str] = None

class Product(BaseModel):
    platform: str
    name: str
    price: float
    mrp: Optional[float] = None
    availability: bool = True
    location: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    product_id: Optional[str] = None
    image_url: Optional[str] = None
    weight: Optional[str] = None
