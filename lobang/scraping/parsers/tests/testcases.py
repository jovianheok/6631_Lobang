TEST_CASES = [
# Food deals
{   "text": """Gelato Messina: Free Extra Gelato Scoop 🍦

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

{   "text": """Burger King: New Smoky Maple Mayo Burgers & Pocket Cameras 🍔

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

{    "text": """Starbucks: 1-for-1 on any Venti drink 🥤

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

{    "text": """Yu Xia Ge: $1.80 Prawn Noodle 🍤

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

{    "text": """Ghost Kakigori: 1-for-1 Sakura Special 🌸

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


# Non food deals
{    "text": """5 Vietnamese Salt Coffee Spots in SG 🥤

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

{    "text": """GastroBeats 2026 Food Guide 🍩

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

{    "text": """SG Friend Up: New Friend Circle Starts Here 👋

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

{    "text": """[GIVEAWAY] Win Handcrafted Artisanal Flavored Butters 🧈

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

{    "text": """Places to get Rice Dumplings for Dragon Boat Festival 🐉

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

]