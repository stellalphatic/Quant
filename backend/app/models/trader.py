from pydantic import BaseModel, Field
from typing import Optional


class TraderBase(BaseModel):
    """Base trader model with common fields."""
    name: str = Field(..., description="Trader's name")
    roi: float = Field(..., description="Return on Investment percentage")
    portfolio_value: float = Field(..., description="Total portfolio value in USDT")


class TraderCreate(TraderBase):
    """Model for creating a new trader."""
    pass


class TraderResponse(TraderBase):
    """Model for trader response with ID."""
    trader_id: str = Field(..., description="Unique identifier for the trader")
    
    class Config:
        from_attributes = True


class Trader(TraderBase):
    """Full trader model including ID."""
    trader_id: Optional[str] = Field(None, description="Unique identifier for the trader")

