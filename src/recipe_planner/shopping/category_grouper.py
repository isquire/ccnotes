"""Group ingredients by grocery store category."""

from __future__ import annotations

from recipe_planner.models.ingredient import Ingredient
from recipe_planner.models.shopping_list import ShoppingList

# Category detection keywords
CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "Produce": [
        "lettuce", "tomato", "onion", "garlic", "pepper", "carrot",
        "celery", "broccoli", "spinach", "kale", "potato", "sweet potato",
        "mushroom", "zucchini", "squash", "cucumber", "avocado", "corn",
        "green bean", "pea", "asparagus", "cabbage", "cauliflower",
        "eggplant", "leek", "scallion", "radish", "beet", "turnip",
        "apple", "banana", "lemon", "lime", "orange", "berry",
        "strawberry", "blueberry", "raspberry", "grape", "mango",
        "pineapple", "peach", "pear", "melon", "watermelon",
        "cilantro", "parsley", "basil", "mint", "dill", "chive",
        "ginger", "jalapeno", "serrano", "habanero", "shallot",
    ],
    "Meat & Seafood": [
        "chicken", "beef", "pork", "turkey", "lamb", "steak",
        "ground beef", "ground turkey", "ground pork", "sausage",
        "bacon", "ham", "prosciutto", "pancetta", "chorizo",
        "salmon", "tuna", "shrimp", "crab", "lobster", "fish",
        "cod", "tilapia", "halibut", "scallop", "mussel", "clam",
        "anchovy", "sardine",
    ],
    "Dairy": [
        "milk", "cream", "butter", "cheese", "yogurt", "sour cream",
        "cream cheese", "mozzarella", "parmesan", "cheddar", "feta",
        "ricotta", "gouda", "brie", "goat cheese", "cottage cheese",
        "heavy cream", "half and half", "whipping cream", "egg",
        "ghee", "crème fraîche",
    ],
    "Pantry": [
        "flour", "sugar", "rice", "pasta", "noodle", "bread",
        "cereal", "oat", "quinoa", "couscous", "lentil", "bean",
        "chickpea", "canned", "broth", "stock", "tomato sauce",
        "tomato paste", "coconut milk", "olive oil", "vegetable oil",
        "vinegar", "soy sauce", "honey", "maple syrup", "peanut butter",
        "jam", "jelly", "mustard", "ketchup", "mayonnaise",
        "hot sauce", "worcestershire", "baking soda", "baking powder",
        "yeast", "cornstarch", "breadcrumb", "cracker", "tortilla",
        "wrap", "pita",
    ],
    "Spices": [
        "salt", "pepper", "cumin", "paprika", "cinnamon", "nutmeg",
        "oregano", "thyme", "rosemary", "bay leaf", "chili powder",
        "cayenne", "turmeric", "coriander", "cardamom", "clove",
        "allspice", "garam masala", "curry powder", "za'atar",
        "smoked paprika", "red pepper flake", "garlic powder",
        "onion powder", "italian seasoning", "taco seasoning",
        "vanilla extract", "almond extract",
    ],
    "Frozen": [
        "frozen", "ice cream", "frozen vegetable", "frozen fruit",
        "frozen pizza", "frozen dinner",
    ],
    "Bakery": [
        "baguette", "roll", "bun", "croissant", "muffin",
        "bagel", "sourdough", "focaccia", "ciabatta", "tortilla",
    ],
}


def categorize_ingredient(ingredient: Ingredient) -> str:
    """Determine the grocery category for an ingredient."""
    # Use pre-assigned category if available
    if ingredient.category:
        return ingredient.category

    name_lower = ingredient.name.lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in name_lower:
                return category

    return "Other"


def group_ingredients(ingredients: list[Ingredient]) -> ShoppingList:
    """Group a list of ingredients into a categorized shopping list."""
    categories: dict[str, list[str]] = {}
    raw_items: list[str] = []

    for ing in ingredients:
        category = categorize_ingredient(ing)
        display = ing.display()
        categories.setdefault(category, []).append(display)
        raw_items.append(display)

    # Sort items within each category
    for cat in categories:
        categories[cat].sort()

    # Ensure standard categories appear in order
    ordered = {}
    for cat_name in ["Produce", "Meat & Seafood", "Dairy", "Pantry",
                     "Spices", "Frozen", "Bakery", "Other"]:
        if cat_name in categories:
            ordered[cat_name] = categories[cat_name]

    # Add any remaining categories
    for cat_name, items in categories.items():
        if cat_name not in ordered:
            ordered[cat_name] = items

    return ShoppingList(
        categories=ordered,
        raw_items=raw_items,
    )
