"""
Gap finder data models and schemas.

This module defines Pydantic models for recipe suggestions
and inventory gap analysis.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class MealCategory(str, Enum):
    """Enumeration for meal categories."""
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACKS = "snacks"
    BEVERAGES = "beverages"
    DESSERTS = "desserts"

class CuisineType(str, Enum):
    """Enumeration for cuisine types."""
    INDIAN = "Indian"
    CHINESE = "Chinese"
    ITALIAN = "Italian"
    MEXICAN = "Mexican"
    AMERICAN = "American"
    THAI = "Thai"
    MEDITERRANEAN = "Mediterranean"
    FUSION = "Fusion"
    OTHER = "Other"

class GapFinderSuggestionBase(BaseModel):
    """Base model for gap finder suggestions."""
    suggestion: str = Field(..., min_length=1, max_length=255, description="Recipe/dish name")
    missing: str = Field(..., description="Missing ingredients (comma-separated)")
    have: List[str] = Field(default_factory=list, description="Available ingredients")
    confidence: int = Field(..., ge=0, le=100, description="Confidence score")
    meals: int = Field(..., ge=1, description="Number of servings/meals")
    category: MealCategory = Field(..., description="Meal category")
    cuisine: CuisineType = Field(..., description="Cuisine type")

class GapFinderSuggestionCreate(GapFinderSuggestionBase):
    """Model for creating gap finder suggestions."""
    recipe: Optional[str] = Field(None, description="Recipe instructions")
    image_query: Optional[str] = Field(None, description="Image search query")

class GapFinderSuggestion(GapFinderSuggestionBase):
    """Complete gap finder suggestion model."""
    id: str = Field(..., description="Unique suggestion ID")
    recipe: Optional[str] = Field(None, description="Recipe instructions")
    image_query: Optional[str] = Field(None, description="Image search query")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class GapFinderResponse(BaseModel):
    """Model for gap finder API responses."""
    suggestions: List[GapFinderSuggestion] = Field(default_factory=list, description="Recipe suggestions")
    total_suggestions: int = Field(default=0, description="Total number of suggestions")
    categories_covered: List[str] = Field(default_factory=list, description="Meal categories covered")

class IngredientAnalysis(BaseModel):
    """Model for ingredient availability analysis."""
    ingredient: str = Field(..., description="Ingredient name")
    available: bool = Field(..., description="Whether ingredient is available")
    quantity_available: Optional[float] = Field(None, description="Available quantity")
    days_left: Optional[int] = Field(None, description="Days until expiry")
    suggested_recipes: List[str] = Field(default_factory=list, description="Recipes using this ingredient")