from backend.catalog import HOME_ITEMS, PARTY_ITEMS, JEWELRY_ITEMS


def home_demo(data):
    budget = data["budget"]
    chosen = [x for x in HOME_ITEMS if x["price"] <= budget * 0.55][:5]
    if not chosen:
        chosen = sorted(HOME_ITEMS, key=lambda x: x["price"])[:3]
    return {
        "planner": "home",
        "summary": f"A practical {data['style']} setup for {', '.join(data['rooms'])}, keeping the plan within ₹{budget:,.0f}.",
        "budget_allocation": [
            {"category": "Lighting", "amount": round(budget * .15)},
            {"category": "Furniture", "amount": round(budget * .45)},
            {"category": "Decor", "amount": round(budget * .20)},
            {"category": "Reserve", "amount": round(budget * .20)},
        ],
        "recommendations": chosen,
        "tips": ["Measure the room before buying furniture.", "Keep a reserve for delivery and installation.", "Mix functional lighting with one decorative piece."],
        "mode": "demo",
    }


def party_demo(data):
    budget = data["budget"]
    guests = data["guests"]
    food = min(budget * .45, guests * 250)
    remaining = budget - food
    return {
        "planner": "party",
        "summary": f"A {data['event_type']} plan for {guests} guests with a ₹{budget:,.0f} target.",
        "budget_allocation": [
            {"category": "Food", "amount": round(food)},
            {"category": "Decoration", "amount": round(budget * .15)},
            {"category": "Venue", "amount": round(budget * .25)},
            {"category": "Reserve", "amount": round(max(0, remaining - budget * .40))},
        ],
        "recommendations": PARTY_ITEMS,
        "tips": ["Confirm venue capacity before paying.", "Ask vendors for per-person pricing.", "Keep a small contingency amount."],
        "mode": "demo",
    }


def jewelry_demo(data):
    budget = data["budget"]
    chosen = [x for x in JEWELRY_ITEMS if x["price"] <= budget][:4]
    return {
        "planner": "jewelry",
        "summary": f"{data['style']} jewelry ideas for a {data['occasion']} occasion within ₹{budget:,.0f}.",
        "budget_allocation": [{"category": "Main piece", "amount": round(budget * .60)}, {"category": "Secondary piece", "amount": round(budget * .25)}, {"category": "Reserve", "amount": round(budget * .15)}],
        "recommendations": chosen,
        "tips": ["Match metal tone with the outfit's overall palette.", "Use one statement piece and keep the other accessories simpler."],
        "mode": "demo",
    }
