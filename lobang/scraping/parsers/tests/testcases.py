TEST_CASES = [
{
    "deal name": "vietnamese_salt_coffee_spots",
    "text": """
5 Vietnamese Salt Coffee Spots in SG 🥤

🔹 Sip on a good cup of Vietnamese salt coffee at these spots:
1️⃣ Bee Hoe Coffee
2️⃣ Crunch & Cups
3️⃣ Joo Chiat Banh Mi Ca Phe
4️⃣ Le Cafe Vie5
5️⃣ Ton Coffee

@sgfooddeals #shoutout
""",
    "expected": {
        "is_food_deal": False,
    },
},
{
    "deal name": "gastrobeats_food_guide",
    "text": """
GastroBeats 2026 Food Guide 🍩

🔹 Discover this year's culinary highlights at GastroBeats featuring everything from Mentaiko Fried Carrot Cake to Quesa Birria Tacos
📅 Now till 28 Jun
⏰ 4PM - 11PM
📍 Bayfront Events Space

Find out more: tco.sg/dus7YTwFf

@sgfooddeals #article
""",
    "expected": {
        "is_food_deal": False,
    },
},
{
    "deal name": "gelato_messina_free_scoop",
    "text": """
Gelato Messina: Free Extra Gelato Scoop 🍦

🔹 Enjoy free extra scoop with your gelato purchase
🔹 Cool down with flavours like Boysenberry, Coffee, Giandua & more
📅 Now till 11 Jun
⏰ From 4PM
📍 1 Club Street, S069400

Find out more: tco.sg/MfR1Jdg7J

@sgfooddeals #deals
""",
    "expected": {
        "is_food_deal": True,
        "title": "Gelato Messina: Free Extra Gelato Scoop",
        "merchant_name": "Gelato Messina",
    },
},
{
    "deal name": "sg_friend_up",
    "text": """
SG Friend Up: New Friend Circle Starts Here 👋

✅ Make new friends, expand your social circle & look out for chill, organised meetups
✅ Chat & connect with like-minded people in your age range
✅ Introduce yourself & keep an eye out for upcoming events

Join here: tco.sg/uXryR0XHL

@sgstudentpromos #shoutout
""",
    "expected": {
        "is_food_deal": False,
    },
},
{
    "deal name": "butter_giveaway",
    "text": """
[GIVEAWAY] Win Handcrafted Artisanal Flavored Butters 🧈

🔹 7 lucky winners stand to win a signature set of artisanal butters from borderlessbutter
🔹 Elevate your meals with their Chunky Miso Shiitake Butter & XO Mala Butter
🔹 Prizes must be self-collected within a week
🔹 To participate, simply:
1️⃣ Follow @renodealssg & borderlessbutter on IG
2️⃣ Comment below & tell us how you would enjoy your butter
📅 Giveaway ends 15 Jun, 11.59PM

Find out more: tco.sg/butterxcollab

@sgfooddeals exclusive
""",
    "expected": {
        "is_food_deal": False,
    },
},
{
    "deal name": "dragon_boat_rice_dumplings",
    "text": """
Places to get Rice Dumplings for Dragon Boat Festival 🐉

🔹 Get your fill of sweet & savoury rice dumplings for the upcoming Dragon Boat Festival celebrations:
1️⃣ Di Tanjong Katong
2️⃣ Hoo Kee Bak Chang
3️⃣ Kim Choo Kueh Chang
4️⃣ Soup Restaurant
5️⃣ Wah Lok

@sgfooddeals #shoutout
""",
    "expected": {
        "is_food_deal": False,
    },
},
{
    "deal name": "burger_king_smoky_maple_mayo",
    "text": """
Burger King: New Smoky Maple Mayo Burgers & Pocket Cameras 🍔

🔹 Try BK’s latest Smoky Maple Mayo range, available in Double Beef, Spicy Chicken King & Double Chick-N-Crisp options
🔹 Savour the sweet & smoky maple mayo that adds a rich, indulgent twist to every bite
🔹 Redeem an exclusive Burger King x Coca-Cola Mini Digicam when you purchase the Smoky Maple Mayo Combo for 1, while stocks last
🔹 Valid for dine-in, takeaway & delivery orders
📅 Now till 27 Jul
📍 All outlets except airport transit

Order here: tco.sg/bkjunxsgfd

@sgfooddeals
""",
    "expected": {
        "is_food_deal": True,
        "title": "Burger King: New Smoky Maple Mayo Burgers & Pocket Cameras",
        "merchant_name": "Burger King",
    },
},
{
    "deal name": "starbucks_1for1_venti",
    "text": """
Starbucks: 1-for-1 on any Venti drink 🥤

🔹 Sign up for a free Starbucks Rewards membership on the app & enjoy 1-for-1 on any Venti handcrafted drink
🔹 Choose from coffee, refreshers, frappuccinos & more
🔹 Available for in-store purchases only
📅 Now till 11 Jun
⏰ 2PM - 8PM
📍 All outlets

More info: tco.sg/mxtMUfZEQ

@sgfooddeals #deals
""",
    "expected": {
        "is_food_deal": True,
        "title": "Starbucks: 1-for-1 on any Venti drink",
        "merchant_name": "Starbucks",
    },
},
{
    "deal name": "yu_xia_ge_prawn_noodle",
    "text": """
Yu Xia Ge: $1.80 Prawn Noodle 🍤

🔹 Enjoy a hearty bowl of prawn noodles with flavourful broth & generous toppings for only $1.80 (U.P. $10.80)
🔹 Valid for dine-in only
🔹 Limited time only
📅 Mon - Sun
📍 1100 Serangoon Rd, 328195

More info: tco.sg/CanMGCuXj

@sgfooddeals #deals
""",
    "expected": {
        "is_food_deal": True,
        "title": "Yu Xia Ge: $1.80 Prawn Noodle",
        "merchant_name": "Yu Xia Ge",
    },
},
{
    "deal name": "ghost_kakigori_sakura_special",
    "text": """
Ghost Kakigori: 1-for-1 Sakura Special 🌸

🔹 Enjoy 1-for-1 on selected Sakura Kakigori Sets & Sakura Matcha Sets
🔹 Choose from flavours like Flamed Strawberry Brulee, Mango Sago Koori, Dubai Pistachio Kunafa & more
🔹 While stocks last
📅 Now till 14 Jun
📍 All outlets

Find out more: tco.sg/7pm9y0hvG

@sgfooddeals #deals
""",
    "expected": {
        "is_food_deal": True,
        "title": "Ghost Kakigori: 1-for-1 Sakura Special",
        "merchant_name": "Ghost Kakigori",
    },
},
{
    "deal name": "olle_korean_bbq_buffet",
    "text": """
Olle: Korean BBQ & Shabu Shabu Lunch Buffet from $20 🍖

🔹 Enjoy an all-you-can-eat Korean BBQ & shabu shabu lunch buffet from just $20
🔹 Expect free flow cheese, sliced meats, Samyang noodles, Dubai Chewy Cookie & more
📅 Mon - Fri
⏰ 11AM - 3PM
📍 16 Cheong Chin Nam Road, 599740

More info: tco.sg/8V9k4o2qg

@sgfooddeals #deals
""",
    "expected": {
        "is_food_deal": True,
        "title": "Olle: Korean BBQ & Shabu Shabu Lunch Buffet from $20",
        "merchant_name": "Olle",
    },
},
{
    "deal name": "jinjja_chicken_wings",
    "text": """
JINJJA Chicken: $0.90 JINJJA Wings 🍗

🔹 Enjoy Jinjja Wings for just $0.90 each
🔹 Min. purchase of 12 wings is required
📅 Now till 30 Jun
📍 All outlets

More info: tco.sg/LsyhQyMbw

@sgfooddeals #deals
""",
    "expected": {
        "is_food_deal": True,
        "title": "JINJJA Chicken: $0.90 JINJJA Wings",
        "merchant_name": "JINJJA Chicken",
    },
},
{
    "deal name": "nanyang_fried_chicken_rice_cutlet",
    "text": """
Nanyang Fried Chicken Rice: $2 Cutlet Meal 🍛

🔹 Enjoy Nanyang Fried Chicken Rice’s signature Cutlet Meal for just $2 to celebrate their 2nd Anniversary
🔹 Limited to 2 plates per customer
🔹 While stocks last
📅 13 Jun (Sat)
⏰ From 11AM
📍 531A Upper Cross St, #02-09

More info: tco.sg/bis5Ewhu6

@sgfooddeals #deals
""",
    "expected": {
        "is_food_deal": True,
        "title": "Nanyang Fried Chicken Rice: $2 Cutlet Meal",
        "merchant_name": "Nanyang Fried Chicken Rice",
    },
},
{
    "deal name": "ban_tianyao_grilled_fish_buffet",
    "text": """
Ban Tianyao: $19.90 Unlimited Grilled Fish Buffet 🐠

🔹 Feast on an unlimited grilled fish buffet with 6 different fish varieties from just $19.90++
🔹 Pair your meal with a choice of 8 soup bases & over 100 hotpot ingredients like pork slices, fresh seafood & more
📅 Mon - Sun
📍 All outlets

Find out more: tco.sg/06TS9KpOT

@sgfooddeals #deals
""",
    "expected": {
        "is_food_deal": True,
        "title": "Ban Tianyao: $19.90 Unlimited Grilled Fish Buffet",
        "merchant_name": "Ban Tianyao",
    },
},
{
    "deal name": "keong_saik_burnt_cheesecake",
    "text": """
Keong Saik Bakery: $0.90 Burnt Cheesecake 🍰

🔹 Enjoy Burnt Cheesecake at just $0.90 per slice
🔹 Limited to 2 pieces per customer
🔹 Available for the first 100 customers at each outlet only
📅 14 Jun (Sun)
📍 All outlets

More info: tco.sg/W6nz4D2TP

@sgfooddeals #deals
""",
    "expected": {
        "is_food_deal": True,
        "title": "Keong Saik Bakery: $0.90 Burnt Cheesecake",
        "merchant_name": "Keong Saik Bakery",
    },
},
{
    "deal name": "warabimochi_kamakura_free_icecream",
    "text": """
Warabimochi Kamakura: Free Ice Cream🍦

🔹 Enjoy a free ice cream with any purchase from the store
🔹 Simply present this post in-store to redeem
🔹 While stocks lasts
📅 Now till 30 Jun
📍 All outlets

T&Cs apply.

Find out more: tco.sg/UqI2PCnsx

@sgfooddeals #deals
""",
    "expected": {
        "is_food_deal": True,
        "title": "Warabimochi Kamakura: Free Ice Cream",
        "merchant_name": "Warabimochi Kamakura",
    },
},
{
    "deal name": "best_buffet_deals_june",
    "text": """
5 Best Buffet Deals This Jun 🍽

🔹 Enjoy the best buffet deals with 1-for-1 offers & unbeatable prices:
1️⃣ Carlton City: 1-for-1 Hong Kong Buffet
2️⃣ Hotel Grand Pacific: 1-for-1 Buffet
3️⃣ Permata Singapore: 1-for-1 Halal Buffet
4️⃣ The Dining Room: 1-for-1 Buffet
5️⃣ The Landmark: 1-for-1 Halal Buffet

@sgfooddeals #deals
""",
    "expected": {
        "is_food_deal": True,
        "title": "5 Best Buffet Deals This Jun",
        "merchant_name": None,
    },
},
{
    "deal name": "sg_home_reno_channel",
    "text": """
Introducing SG Home Reno Deals Telegram Channel 🏘

🔘 Here's everything you need for your dream home in one place with furniture & decor deals starting at $1, home-improvement workshops & more

Find out more: tco.sg/4wiGu0AnZ

@sgadulting101 #shoutout
""",
    "expected": {
        "is_food_deal": False,
    },
},
{
    "deal name": "poke_theory_half_price",
    "text": """
Poke Theory: 50% off Poke Bowls 🐟

🔹 Enjoy a poke bowl loaded with fresh ingredients & premium proteins at 50% off
🔹 Simply sign up for a free Poke Theory membership to redeem on your first order
🔹 Limited time only
📍 All outlets

Find out more: tco.sg/CgEkLMuEu

@sgfooddeals #deals
""",
    "expected": {
        "is_food_deal": True,
        "title": "Poke Theory: 50% off Poke Bowls",
        "merchant_name": "Poke Theory",
    },
},
{
    "deal name": "pizza_hut_large_pizza",
    "text": """
Pizza Hut: $10 Large Pizzas for Takeaways 🍕

🔹 Pizza Hut brings back its all-time favourite $10 Large Pizza (U.P. $35.05)
🔹 Choose between BBQ Chunky Chic, Very Beefy or Chic Ham N Shroom
📅 16, 17, 23 & 24 Jun (Tue & Wed)
📍 All outlets

Order here: tco.sg/MBeTzELC0

@sgfooddeals #deals
""",
    "expected": {
        "is_food_deal": True,
        "title": "Pizza Hut: $10 Large Pizzas for Takeaways",
        "merchant_name": "Pizza Hut",
    },
}
]