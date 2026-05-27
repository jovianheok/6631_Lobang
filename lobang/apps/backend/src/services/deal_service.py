# Currently: creates mock deal data -> returns it
# To edit after MVP: queries DB -> ranks deals -> filters deals

def get_mock_deals():
    return [
        {
            "id": 101,
            "title": "2-for-1 lunch set",
            "merchant_name": "Bistro 88",
            "distance_km": 0.8,
            "score": 0.91,
            "status": "active",
            "verification_status": "verified",
            "end_time": "2026-05-21T14:00:00Z",
            "reason": ["Nearby", "Matches your budget", "Recently verified"],
        },
        {
            "id": 102,
            "title": "15% off dinner menu",
            "merchant_name": "Sakura House",
            "distance_km": 2.3,
            "score": 0.82,
            "status": "active",
            "verification_status": "verified",
            "end_time": "2026-05-22T18:00:00Z",
            "reason": ["Good cuisine match", "Still active", "Within radius"],
        },
    ]