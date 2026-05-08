"""
Gap finder API routes.

This module contains API endpoints for recipe suggestions
and inventory gap analysis.
"""

from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter()

# In-memory store for gap finder suggestions (will be replaced with database service)
gap_finder_db = [
    {"id":"g1","suggestion":"Masala Omelette","missing":"Onion, Green Chilli","have":["Eggs","Milk","Cheddar Cheese"],"confidence":94,"meals":3,"category":"breakfast","cuisine":"Indian","recipe":"Beat eggs with salt, turmeric, red chilli. Add onion, green chilli. Cook in butter till set.","image_query":"masala omelette indian"},
    {"id":"g2","suggestion":"Palak Paneer","missing":"Paneer, Garlic, Cream","have":["Baby Spinach","Onion"],"confidence":87,"meals":2,"category":"dinner","cuisine":"Indian","recipe":"Blanch spinach, blend. Sauté onion-garlic, add spices, spinach, paneer. Finish with cream.","image_query":"palak paneer restaurant"},
    {"id":"g3","suggestion":"Mango Lassi","missing":"Mango Pulp, Sugar","have":["Amul Greek Yogurt","Milk"],"confidence":96,"meals":2,"category":"beverages","cuisine":"Indian","recipe":"Blend yogurt, milk, mango pulp, sugar, cardamom. Serve chilled.","image_query":"mango lassi drink"},
    {"id":"g4","suggestion":"Rice Kheer","missing":"Sugar, Cardamom, Saffron","have":["Basmati Rice","Amul Whole Milk"],"confidence":85,"meals":6,"category":"desserts","cuisine":"Indian","recipe":"Boil milk, add soaked rice. Cook 45 min, add sugar, cardamom, saffron.","image_query":"rice kheer dessert"},
    {"id":"g5","suggestion":"Dahi Chawal","missing":"Cumin, Salt","have":["Basmati Rice","Amul Greek Yogurt"],"confidence":99,"meals":2,"category":"lunch","cuisine":"Indian","recipe":"Mix cooled rice with beaten yogurt. Season with roasted cumin and salt.","image_query":"dahi chawal curd rice"},
]

@router.get("/")
async def get_gap_finder():
    """Get recipe suggestions based on available inventory."""
    return {"suggestions": gap_finder_db}