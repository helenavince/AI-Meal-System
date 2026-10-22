"""
Hostel Ladies Mess Food Menu (Days 1 to 31)
Calendar-day driven meal schedule for Breakfast, Lunch, and Dinner.
Extracted from the official monthly mess timetable.
"""

from typing import List, Dict, Any, Optional
import datetime

MONTHLY_MESS_MENU: Dict[int, Dict[str, Any]] = {
    1: {
        "dayNumber": 1,
        "weekday": "Thursday",
        "breakfast": {
            "timing_label": "7:00 AM - 8:45 AM",
            "main_items": "Bread + Jam + Butter, Karuveppilai Podi Uthappam & Potato Kuruma",
            "dishes": ["Bread + Jam + Butter", "Karuveppilai Podi Uthappam", "Potato Kuruma", "Coriander Chutney", "Tea / Coffee / Milk"]
        },
        "lunch": {
            "timing_label": "12:15 PM - 1:30 PM",
            "main_items": "Rice, Tomato Bath, Sambar Sadham & Rasam",
            "dishes": ["Steamed Rice", "Tomato Bath", "Sambar Sadham", "Rasam", "Onion Raita", "Vadagam", "Butter Milk"]
        },
        "dinner": {
            "timing_label": "7:00 PM - 8:45 PM",
            "main_items": "Chapati, Tomato Thokku & Black Sundal Pulao",
            "dishes": ["Chapati", "Tomato Thokku", "Black Sundal Pulao", "Curd Rice", "Ragi / Aval Sweet", "Egg Masala / Pepper Fry"]
        }
    },
    2: {
        "dayNumber": 2,
        "weekday": "Friday",
        "breakfast": {
            "timing_label": "7:00 AM - 8:45 AM",
            "main_items": "Idly, Sambar, Karuppati Pongal & Meduvadai",
            "dishes": ["Idly", "Sambar", "Karuppati Pongal", "Meduvadai", "Coconut Chutney", "Tea / Coffee / Milk"]
        },
        "lunch": {
            "timing_label": "12:15 PM - 1:30 PM",
            "main_items": "Rice, Vathal Puli Kulambu, Kollu Rasam & Snake Gourd Poriyal",
            "dishes": ["Steamed Rice", "Vathal Puli Kulambu", "Kollu Rasam", "Snake Gourd Poriyal", "Appalam", "Curd"]
        },
        "dinner": {
            "timing_label": "7:00 PM - 8:45 PM",
            "main_items": "Parotta, Soya Kuruma & Vegetable Biryani",
            "dishes": ["Parotta", "Soya Kuruma", "Vegetable Biryani (Yellow)", "Curd Rice", "Coconut Chutney", "Banana"]
        }
    },
    3: {
        "dayNumber": 3,
        "weekday": "Saturday",
        "breakfast": {
            "timing_label": "7:00 AM - 8:45 AM",
            "main_items": "Onion Dosa, Kuruma & Aval Upma",
            "dishes": ["Onion Dosa", "Kuruma", "Aval Upma", "Kara Chutney", "Tea / Coffee / Milk"]
        },
        "lunch": {
            "timing_label": "12:15 PM - 1:30 PM",
            "main_items": "Rice, Drumstick Sambar, Rasam & Paruppu Vadai",
            "dishes": ["Steamed Rice", "Drumstick Sambar", "Rasam", "Payasam + Poriyal", "Paruppu Vadai", "Butter Milk"]
        },
        "dinner": {
            "timing_label": "7:00 PM - 8:45 PM",
            "main_items": "Idly, Sambar & Noodles",
            "dishes": ["Idly", "Sambar", "Noodles (Normal)", "Curd Rice", "Coconut Chutney", "Rose Milk / Chukku Milk"]
        }
    },
    4: {
        "dayNumber": 4,
        "weekday": "Sunday",
        "breakfast": {
            "timing_label": "7:00 AM - 8:45 AM",
            "main_items": "Bread + Jam + Butter & Semiya Upma",
            "dishes": ["Bread + Jam + Butter", "Semiya Upma", "Coconut Chutney", "Tea / Coffee / Milk"]
        },
        "lunch": {
            "timing_label": "12:15 PM - 1:30 PM",
            "main_items": "Soya Biryani, White Rice & Coconut Milk Rasam",
            "dishes": ["Soya Biryani", "Onion Raita", "White Rice", "Coconut Milk Rasam", "Egg Gravy", "Butter Milk"]
        },
        "dinner": {
            "timing_label": "7:00 PM - 8:45 PM",
            "main_items": "Tomato Utthappam, Sambar & Kollu Sadam",
            "dishes": ["Tomato Utthappam", "Sambar", "Kollu Sadam", "Curd Rice", "Onion Thuvaiyal", "Banana"]
        }
    },
    5: {
        "dayNumber": 5,
        "weekday": "Monday",
        "breakfast": {
            "timing_label": "7:00 AM - 8:45 AM",
            "main_items": "Podi Dosa, Plain Kuruma & Rava Kitchadi",
            "dishes": ["Podi Dosa", "Plain Kuruma", "Rava Kitchadi", "Tomato Chutney", "Tea / Coffee / Milk"]
        },
        "lunch": {
            "timing_label": "12:15 PM - 1:30 PM",
            "main_items": "Rice, Arachu Vecha Kulambu & Dhall Rasam",
            "dishes": ["Steamed Rice", "Arachu Vecha Kulambu", "Dhall Rasam", "Yam Poriyal", "Kambu Koozh + Vathal", "Butter Milk"]
        },
        "dinner": {
            "timing_label": "7:00 PM - 8:45 PM",
            "main_items": "Idly, Tiffin Sambar & Lemon Sadham",
            "dishes": ["Idly", "Tiffin Sambar", "Lemon Sadham", "Curd Rice", "Coconut Chutney", "Banana"]
        }
    },
    6: {
        "dayNumber": 6,
        "weekday": "Tuesday",
        "breakfast": {
            "timing_label": "7:00 AM - 8:45 AM",
            "main_items": "Seeragasamba Ven Pongal, Veg Semiya & Meduvadai",
            "dishes": ["Seeragasamba Ven Pongal", "Veg Semiya", "Sambar", "Meduvadai", "Coconut Chutney", "Tea / Coffee / Milk"]
        },
        "lunch": {
            "timing_label": "12:15 PM - 1:30 PM",
            "main_items": "Rice, Dhall Fry & Rasam",
            "dishes": ["Steamed Rice", "Dhall Fry", "Rasam", "Potato Peas Poriyal", "Appalam", "Butter Milk"]
        },
        "dinner": {
            "timing_label": "7:00 PM - 8:45 PM",
            "main_items": "Chapati, Green Peas Masala & Kuskha",
            "dishes": ["Chapati", "Fruit Jam", "Green Peas Masala", "Kuskha", "Curd Rice", "Boiled Egg"]
        }
    },
    7: {
        "dayNumber": 7,
        "weekday": "Wednesday",
        "breakfast": {
            "timing_label": "7:00 AM - 8:45 AM",
            "main_items": "Idly, Tomato Kulambu & Wheat Rava Kitchadi",
            "dishes": ["Idly", "Tomato Kulambu", "Wheat Rava Kitchadi", "Coconut / Curry Leaves Chutney", "Tea / Coffee / Milk"]
        },
        "lunch": {
            "timing_label": "12:15 PM - 1:30 PM",
            "main_items": "Rice, Chettinad Kara Kulambu & Rasam",
            "dishes": ["Steamed Rice", "Chettinad Kara Kulambu", "Rasam", "Yellow Pumpkin Poriyal", "Payasam", "Butter Milk"]
        },
        "dinner": {
            "timing_label": "7:00 PM - 8:45 PM",
            "main_items": "Uthappam, Pacha Payaru Sadham & Sambar",
            "dishes": ["Uthappam", "Pacha Payaru Sadham", "Sambar", "Curd Rice", "Kaara Chutney", "Badham / Ragi Malt"]
        }
    },
    8: {
        "dayNumber": 8,
        "weekday": "Thursday",
        "breakfast": {
            "timing_label": "7:00 AM - 8:45 AM",
            "main_items": "Bread + Jam + Butter, Ghee Podi Utthappam & Nilgiri Kuruma",
            "dishes": ["Bread + Jam + Butter", "Ghee Podi Utthappam", "Nilgiri Kuruma", "Groundnut Chutney", "Tea / Coffee / Milk"]
        },
        "lunch": {
            "timing_label": "12:15 PM - 1:30 PM",
            "main_items": "Rice, Kushka & Sambar Sadham",
            "dishes": ["Steamed Rice", "Kushka", "Sambar Sadham", "Rasam", "Vadagam", "Butter Milk"]
        },
        "dinner": {
            "timing_label": "7:00 PM - 8:45 PM",
            "main_items": "Chapati, Soya Kuruma (Chettinad) & Veg Pulao",
            "dishes": ["Chapati", "Soya Kuruma (Chettinad Style)", "Veg Pulao", "Curd Rice", "Avul Sweet", "Egg Pepper Fry / Masala"]
        }
    },
    9: {
        "dayNumber": 9,
        "weekday": "Friday",
        "breakfast": {
            "timing_label": "7:00 AM - 8:45 AM",
            "main_items": "Ragi Idly, Sweet Pongal & Meduvadai",
            "dishes": ["Ragi Idly", "Sweet Pongal", "Sambar", "Meduvadai", "Coconut Chutney", "Tea / Coffee / Milk"]
        },
        "lunch": {
            "timing_label": "12:15 PM - 1:30 PM",
            "main_items": "Rice, Kollu Paruppu, Kollu Rasam & Raw Banana Poriyal",
            "dishes": ["Steamed Rice", "Kollu Paruppu", "Kollu Rasam", "Raw Banana Poriyal", "Appalam", "Curd"]
        },
        "dinner": {
            "timing_label": "7:00 PM - 8:45 PM",
            "main_items": "Parotta, Channa Masala & Mint Rice",
            "dishes": ["Parotta", "Channa Masala", "Mint Rice", "Curd Rice", "Coconut Chutney", "Banana"]
        }
    },
    10: {
        "dayNumber": 10,
        "weekday": "Saturday",
        "breakfast": {
            "timing_label": "7:00 AM - 8:45 AM",
            "main_items": "Kal Dosa, White Kuruma & Ragi Semiya",
            "dishes": ["Kal Dosa", "White Kuruma", "Ragi Semiya", "Coconut Chutney", "Tea / Coffee / Milk"]
        },
        "lunch": {
            "timing_label": "12:15 PM - 1:30 PM",
            "main_items": "Rice, Sambar, Dhall Rasam & Paruppu Vadai",
            "dishes": ["Steamed Rice", "Sambar", "Dhall Rasam", "Payasam + Poriyal", "Paruppu Vadai", "Butter Milk"]
        },
        "dinner": {
            "timing_label": "7:00 PM - 8:45 PM",
            "main_items": "Idly, Sambar & Coconut Rice",
            "dishes": ["Idly", "Sambar", "Coconut Rice", "Curd Rice", "Coconut Chutney", "Lemon Juice / Rasna"]
        }
    },
    11: {
        "dayNumber": 11,
        "weekday": "Sunday",
        "breakfast": {
            "timing_label": "7:00 AM - 8:45 AM",
            "main_items": "Bread + Jam + Butter & Thinai Pongal",
            "dishes": ["Bread + Jam + Butter", "Thinai Pongal", "Sambar", "Coconut Chutney", "Tea / Coffee / Milk"]
        },
        "lunch": {
            "timing_label": "12:15 PM - 1:30 PM",
            "main_items": "Mushroom Biryani, White Rice & Egg Gravy",
            "dishes": ["Mushroom Biryani", "Onion Raita", "White Rice", "Pacha Puli Rasam", "Egg Gravy", "Butter Milk"]
        },
        "dinner": {
            "timing_label": "7:00 PM - 8:45 PM",
            "main_items": "Uthappam, Potato Kuruma & Rice Noodles",
            "dishes": ["Uthappam", "Potato Kuruma", "Noodles (Rice)", "Tomato Sauce", "Curd Rice & Banana", "Veg Chutney"]
        }
    },
    12: {
        "dayNumber": 12,
        "weekday": "Monday",
        "breakfast": {
            "timing_label": "7:00 AM - 8:45 AM",
            "main_items": "Idly, Sambar, Ukkarai Sweet & Avul Upma",
            "dishes": ["Idly", "Sambar", "Ukkarai Sweet", "Avul Upma", "Kara Chutney", "Tea / Coffee / Milk"]
        },
        "lunch": {
            "timing_label": "12:15 PM - 1:30 PM",
            "main_items": "Rice, Mochai Puli Kulambu & Erichery",
            "dishes": ["Steamed Rice", "Mochai Puli Kulambu", "Rasam", "Erichery", "Kambu Koozh + Vathal", "Butter Milk"]
        },
        "dinner": {
            "timing_label": "7:00 PM - 8:45 PM",
            "main_items": "Onion Dosa, Pasiparuppu Sambar & Malli Sadham",
            "dishes": ["Onion Dosa", "Pasiparuppu Sambar", "Malli Sadham", "Curd Rice", "Coconut Chutney", "Banana"]
        }
    },
    13: {
        "dayNumber": 13,
        "weekday": "Tuesday",
        "breakfast": {
            "timing_label": "7:00 AM - 8:45 AM",
            "main_items": "Ghee Podi Uthappam, Tomato Semiya & Meduvadai",
            "dishes": ["Ghee Podi Uthappam", "Sambar", "Tomato Semiya", "Meduvadai", "Coconut Chutney", "Tea / Coffee / Milk"]
        },
        "lunch": {
            "timing_label": "12:15 PM - 1:30 PM",
            "main_items": "Rice, Pacha Payaru Kadasal & Carrot Poriyal",
            "dishes": ["Steamed Rice", "Pacha Payaru Kadasal", "Rasam", "Carrot Poriyal", "Appalam", "Butter Milk"]
        },
        "dinner": {
            "timing_label": "7:00 PM - 8:45 PM",
            "main_items": "Chapathi, Aloo Mutter & Jeera Rice",
            "dishes": ["Chapathi", "Aloo Mutter", "Jeera Rice", "Curd Rice & Boiled Egg", "Fruit Jam"]
        }
    },
    14: {
        "dayNumber": 14,
        "weekday": "Wednesday",
        "breakfast": {
            "timing_label": "7:00 AM - 8:45 AM",
            "main_items": "Variety Dosa, Rava Upma & Onion Chutney",
            "dishes": ["Variety Dosa", "Rava Upma", "Sambar", "Onion Chutney", "Tea / Coffee / Milk"]
        },
        "lunch": {
            "timing_label": "12:15 PM - 1:30 PM",
            "main_items": "Rice, Thattapayaru Kulambu & Payasam",
            "dishes": ["Steamed Rice", "Thattapayaru Kulambu", "Dhall Rasam", "Payasam", "Cabbage Poriyal", "Butter Milk"]
        },
        "dinner": {
            "timing_label": "7:00 PM - 8:45 PM",
            "main_items": "Idly, Potato Kuruma & Noodles",
            "dishes": ["Idly", "Potato Kuruma", "Noodles", "Curd Rice", "Coconut Chutney", "Badam Milk / Ragi Malt", "Tomato Sauce"]
        }
    },
    15: {
        "dayNumber": 15,
        "weekday": "Thursday",
        "breakfast": {
            "timing_label": "7:00 AM - 8:45 AM",
            "main_items": "Bread + Jam + Butter & Masala Uthappam",
            "dishes": ["Bread + Jam + Butter", "Masala Uthappam", "Sambar", "Groundnut Chutney", "Tea / Coffee / Milk"]
        },
        "lunch": {
            "timing_label": "12:15 PM - 1:30 PM",
            "main_items": "Rice, Tomato Rice & Sambar Sadham",
            "dishes": ["Steamed Rice", "Tomato Rice", "Sambar Sadham", "Rasam", "Vadagam", "Onion Raita", "Butter Milk"]
        },
        "dinner": {
            "timing_label": "7:00 PM - 8:45 PM",
            "main_items": "Chapati, Channa Masala & Soya Biryani",
            "dishes": ["Chapati", "Channa Masala", "Soya Biryani", "Curd Rice", "Egg Masala / Egg Pepper Fry", "Veg Salad"]
        }
    },
    16: {
        "dayNumber": 16,
        "weekday": "Friday",
        "breakfast": {
            "timing_label": "7:00 AM - 8:45 AM",
            "main_items": "Idly, Drumstick Sambar, Sweet Pongal & Medhu Vadai",
            "dishes": ["Idly", "Drumstick Sambar", "Sweet Pongal (Brown Sugar)", "Medhu Vadai", "Coconut Chutney", "Tea / Coffee / Milk"]
        },
        "lunch": {
            "timing_label": "12:15 PM - 1:30 PM",
            "main_items": "Rice, Mor Kulambu, Dhall Rasam & Potato Varuval",
            "dishes": ["Steamed Rice", "Mor Kulambu", "Dhall Rasam", "Potato Varuval", "Appalam", "Curd"]
        },
        "dinner": {
            "timing_label": "7:00 PM - 8:45 PM",
            "main_items": "Parotta, Plain Salna & Malli Biriyani",
            "dishes": ["Parotta", "Plain Salna", "Malli Biriyani", "Curd Rice", "Coconut Chutney", "Banana"]
        }
    },
    17: {
        "dayNumber": 17,
        "weekday": "Saturday",
        "breakfast": {
            "timing_label": "7:00 AM - 8:45 AM",
            "main_items": "Dosa, Potato Masala & Ragi Semiya",
            "dishes": ["Dosa", "Potato Masala", "Sambar", "Ragi Semiya", "Onion Thuvaiyal", "Tea / Coffee / Milk"]
        },
        "lunch": {
            "timing_label": "12:15 PM - 1:30 PM",
            "main_items": "Rice, Kadhamba Sambar, Rasam & Paruppu Vadai",
            "dishes": ["Steamed Rice", "Kadhamba Sambar", "Rasam", "Payasam + Poriyal", "Paruppu Vadai", "Butter Milk"]
        },
        "dinner": {
            "timing_label": "7:00 PM - 8:45 PM",
            "main_items": "Idly, Kuruma & Veg Rice",
            "dishes": ["Idly", "Kuruma", "Veg Rice", "Kara Chutney", "Curd Rice", "Rose Milk / Chukku Milk"]
        }
    },
    18: {
        "dayNumber": 18,
        "weekday": "Sunday",
        "breakfast": {
            "timing_label": "7:00 AM - 8:45 AM",
            "main_items": "Bread + Jam + Butter & Semiya Upma",
            "dishes": ["Bread + Jam + Butter", "Semiya Upma", "Coconut Chutney", "Tea / Coffee / Milk"]
        },
        "lunch": {
            "timing_label": "12:15 PM - 1:30 PM",
            "main_items": "Vegetable Biryani, White Rice & Egg Gravy",
            "dishes": ["Vegetable Biryani", "Onion Raita", "White Rice", "Pacha Puli Rasam", "Egg Gravy", "Butter Milk"]
        },
        "dinner": {
            "timing_label": "7:00 PM - 8:45 PM",
            "main_items": "Onion Dosa, Carrot Sadam & Sambar",
            "dishes": ["Onion Dosa", "Carrot Sadam", "Sambar", "Curd Rice", "Banana + Tomato Sauce", "Coriander Chutney"]
        }
    },
    19: {
        "dayNumber": 19,
        "weekday": "Monday",
        "breakfast": {
            "timing_label": "7:00 AM - 8:45 AM",
            "main_items": "Idly, Rava Kitchadi, Onion Kuruma & Idly Podi",
            "dishes": ["Idly", "Rava Kitchadi", "Onion Kuruma", "Kara Chutney", "Idly Podi with Gingelly Oil", "Tea / Coffee / Milk"]
        },
        "lunch": {
            "timing_label": "12:15 PM - 1:30 PM",
            "main_items": "Rice, Arachuvecha Kulambu & Bottle Gourd Kootu",
            "dishes": ["Steamed Rice", "Arachuvecha (Onion + Drumstick) Kulambu", "Rasam", "Bottle Gourd Kootu", "Kambu Koozh + Vathal", "Butter Milk"]
        },
        "dinner": {
            "timing_label": "7:00 PM - 8:45 PM",
            "main_items": "Veg Uthappam, Karuveppilai Sadam & Sambar",
            "dishes": ["Veg Uthappam", "Sambar", "Karuveppilai Sadam", "Coconut Chutney", "Curd Rice", "Banana"]
        }
    },
    20: {
        "dayNumber": 20,
        "weekday": "Tuesday",
        "breakfast": {
            "timing_label": "7:00 AM - 8:45 AM",
            "main_items": "Seeragasambakurunai Pongal, Malli Semiya & Medhu Vadai",
            "dishes": ["Seeragasambakurunai Pongal", "Malli Semiya", "Sambar", "Medhu Vadai", "Coconut Chutney", "Tea / Coffee / Milk"]
        },
        "lunch": {
            "timing_label": "12:15 PM - 1:30 PM",
            "main_items": "Rice, Drumstick Sambar & Banana Stem Poriyal",
            "dishes": ["Steamed Rice", "Drumstick Sambar", "Banana Stem Poriyal", "Rasam", "Appalam", "Butter Milk"]
        },
        "dinner": {
            "timing_label": "7:00 PM - 8:45 PM",
            "main_items": "Chapathi, Pattani Paal Curry Kuruma & Empty Biriyani",
            "dishes": ["Chapathi", "Pattani Paal Curry Kuruma", "Empty Biriyani", "Boiled Egg", "Curd Rice", "Onion Raitha"]
        }
    },
    21: {
        "dayNumber": 21,
        "weekday": "Wednesday",
        "breakfast": {
            "timing_label": "7:00 AM - 8:45 AM",
            "main_items": "Idly, Tomato Kulambu & Wheat Rava Upma",
            "dishes": ["Idly", "Tomato Kulambu", "Wheat Rava Upma + Curd", "Mint Chutney", "Tea / Coffee / Milk"]
        },
        "lunch": {
            "timing_label": "12:15 PM - 1:30 PM",
            "main_items": "Rice, Vathal Puli Kulambu & Kathamba Poriyal",
            "dishes": ["Steamed Rice", "Vathal Puli Kulambu", "Rasam", "Kathamba Poriyal", "Payasam", "Butter Milk"]
        },
        "dinner": {
            "timing_label": "7:00 PM - 8:45 PM",
            "main_items": "Set Dosa, Vada Curry & Arisi Paruppu Sadham",
            "dishes": ["Set Dosa", "Vada Curry", "Arisi Paruppu Sadham", "Curd Rice", "Veg Chutney", "Lemon Juice / Rasna"]
        }
    },
    22: {
        "dayNumber": 22,
        "weekday": "Thursday",
        "breakfast": {
            "timing_label": "7:00 AM - 8:45 AM",
            "main_items": "Bread + Jam + Butter, Onion Mini Uttappam & Pasiparuppu Sambar",
            "dishes": ["Bread + Jam + Butter", "Onion Mini Uttappam", "Pasiparuppu Sambar", "Kaara Chutney", "Tea / Coffee / Milk"]
        },
        "lunch": {
            "timing_label": "12:15 PM - 1:30 PM",
            "main_items": "Rice, Malli Biryani, Curd Rice & Rasam",
            "dishes": ["Steamed Rice", "Malli Biryani", "Curd Rice", "Onion Raitha", "Rasam", "Vadagam + Butter Milk"]
        },
        "dinner": {
            "timing_label": "7:00 PM - 8:45 PM",
            "main_items": "Chapathi + Jam, Mixed Veg Curry & Ghee Rice",
            "dishes": ["Chapathi + Jam", "Mixed Veg Curry", "Ghee Rice", "Curd Rice", "Egg Pepper Fry / Masala"]
        }
    },
    23: {
        "dayNumber": 23,
        "weekday": "Friday",
        "breakfast": {
            "timing_label": "7:00 AM - 8:45 AM",
            "main_items": "Idly, Drumstick Sambar, Sweet Pongal & Medhu Vadai",
            "dishes": ["Idly", "Drumstick Sambar", "Sweet Pongal (Brown Sugar)", "Medhu Vadai", "Coconut Chutney", "Tea / Coffee / Milk"]
        },
        "lunch": {
            "timing_label": "12:15 PM - 1:30 PM",
            "main_items": "Rice, Thattapayaru Kulambu & Sundal Poriyal",
            "dishes": ["Steamed Rice", "Thattapayaru Kulambu", "Dhall Rasam", "Sundal Poriyal", "Appalam", "Curd"]
        },
        "dinner": {
            "timing_label": "7:00 PM - 8:45 PM",
            "main_items": "Parotta, Channa Kuruma & Tomato Rice",
            "dishes": ["Parotta", "Channa Kuruma", "Tomato Rice", "Curd Rice", "Coconut Chutney", "Banana"]
        }
    },
    24: {
        "dayNumber": 24,
        "weekday": "Saturday",
        "breakfast": {
            "timing_label": "7:00 AM - 8:45 AM",
            "main_items": "Dosa, Potato Masala & Avul Upma",
            "dishes": ["Dosa", "Potato Masala", "Sambar", "Avul Upma", "Tomato Chutney", "Tea / Coffee / Milk"]
        },
        "lunch": {
            "timing_label": "12:15 PM - 1:30 PM",
            "main_items": "Rice, Kadhamba Sambar, Rasam & Paruppu Vadai",
            "dishes": ["Steamed Rice", "Kadhamba Sambar", "Rasam", "Payasam + Poriyal", "Paruppu Vadai", "Butter Milk"]
        },
        "dinner": {
            "timing_label": "7:00 PM - 8:45 PM",
            "main_items": "Arisi Paruppu Sadham, Egg Rice & Veg Rice",
            "dishes": ["Arisi Paruppu Sadham", "Egg Rice", "Veg Rice + Tomato Sauce", "Curd Rice", "Vadagam", "Rose Milk / Chukku Paal"]
        }
    },
    25: {
        "dayNumber": 25,
        "weekday": "Sunday",
        "breakfast": {
            "timing_label": "7:00 AM - 8:45 AM",
            "main_items": "Bread + Jam + Butter, Ven Pongal & Sambar",
            "dishes": ["Bread + Jam + Butter", "Ven Pongal", "Sambar", "Coconut Chutney", "Tea / Coffee / Milk"]
        },
        "lunch": {
            "timing_label": "12:15 PM - 1:30 PM",
            "main_items": "Rice, Vegetable Biryani & Coconut Milk Rasam",
            "dishes": ["Steamed Rice", "Vegetable Biryani", "Coconut Milk Rasam", "Egg Gravy", "Onion Raita", "Butter Milk"]
        },
        "dinner": {
            "timing_label": "7:00 PM - 8:45 PM",
            "main_items": "Podi Dosa, Noodles & Kuruma",
            "dishes": ["Podi Dosa", "Noodles", "Kuruma", "Curd Rice", "Veg Chutney", "Tomato Sauce + Banana"]
        }
    },
    26: {
        "dayNumber": 26,
        "weekday": "Monday",
        "breakfast": {
            "timing_label": "7:00 AM - 8:45 AM",
            "main_items": "Idly, Lapsi Sweet, Potato Kuruma & Bread Upma",
            "dishes": ["Idly", "Lapsi Sweet", "Potato Kuruma", "Bread Upma", "Groundnut Chutney", "Tea / Coffee / Milk"]
        },
        "lunch": {
            "timing_label": "12:15 PM - 1:30 PM",
            "main_items": "Rice, Sundal Kulambu, Milagu Rasam & Yellow Pumpkin Poriyal",
            "dishes": ["Steamed Rice", "Sundal Kulambu", "Milagu Rasam", "Yellow Pumpkin Poriyal", "Kambu Koozh + Vathal", "Butter Milk"]
        },
        "dinner": {
            "timing_label": "7:00 PM - 8:45 PM",
            "main_items": "Beetroot Dosa, Pasiparuppu Sambar & Peas Pulao",
            "dishes": ["Beetroot Dosa", "Pasiparuppu Sambar", "Peas Pulao", "Curd Rice", "Veg Chutney", "Banana"]
        }
    },
    27: {
        "dayNumber": 27,
        "weekday": "Tuesday",
        "breakfast": {
            "timing_label": "7:00 AM - 8:45 AM",
            "main_items": "Ghee Podi Uthappam, Semiya Upma & Medhu Vadai",
            "dishes": ["Ghee Podi Uthappam", "Sambar", "Semiya Upma", "Medhu Vadai", "Coconut Chutney", "Tea / Coffee / Milk"]
        },
        "lunch": {
            "timing_label": "12:15 PM - 1:30 PM",
            "main_items": "Rice, Dhall Fry, Rasam & Carrot Peas Poriyal",
            "dishes": ["Steamed Rice", "Dhall Fry", "Rasam", "Carrot Peas Poriyal", "Appalam", "Butter Milk"]
        },
        "dinner": {
            "timing_label": "7:00 PM - 8:45 PM",
            "main_items": "Chappathi, Fruit Jam, Veg Kuruma & Puli Sadham",
            "dishes": ["Chappathi", "Fruit Jam", "Veg Kuruma (Hotel Style)", "Puli Sadham", "Curd Rice", "Boiled Egg"]
        }
    },
    28: {
        "dayNumber": 28,
        "weekday": "Wednesday",
        "breakfast": {
            "timing_label": "7:00 AM - 8:45 AM",
            "main_items": "Roast, Kumbakonam Kadappa & Wheat Rava Kitchadi",
            "dishes": ["Roast", "Kumbakonam Kadappa", "Wheat Rava Kitchadi", "Tomato Chutney", "Tea / Coffee / Milk"]
        },
        "lunch": {
            "timing_label": "12:15 PM - 1:30 PM",
            "main_items": "Rice, Pacha Payaru, Tomato Rasam & Beetroot Poriyal",
            "dishes": ["Steamed Rice", "Pacha Payaru", "Tomato Rasam", "Beetroot Poriyal", "Payasam", "Butter Milk"]
        },
        "dinner": {
            "timing_label": "7:00 PM - 8:45 PM",
            "main_items": "Idly, Sambar & Thatta Payaru Sadham",
            "dishes": ["Idly", "Sambar", "Thatta Payaru Sadham", "Curd Rice", "Kara Chutney", "Lemon Juice / Rasna"]
        }
    },
    29: {
        "dayNumber": 29,
        "weekday": "Thursday",
        "breakfast": {
            "timing_label": "7:00 AM - 8:45 AM",
            "main_items": "Bread + Jam + Butter, Karuveppilai Podi Uthappam & Potato Kuruma",
            "dishes": ["Bread + Jam + Butter", "Karuveppilai Podi Uthappam", "Potato Kuruma", "Coriander Chutney", "Tea / Coffee / Milk"]
        },
        "lunch": {
            "timing_label": "12:15 PM - 1:30 PM",
            "main_items": "Rice, Tomato Bath, Sambar Sadham & Rasam",
            "dishes": ["Steamed Rice", "Tomato Bath", "Sambar Sadham", "Rasam", "Onion Raita", "Vadagam", "Butter Milk"]
        },
        "dinner": {
            "timing_label": "7:00 PM - 8:45 PM",
            "main_items": "Chapati, Tomato Thokku & Chick Peas Pulao",
            "dishes": ["Chapati", "Tomato Thokku", "Chick Peas Pulao", "Curd Rice", "Ragi / Aval Sweet", "Egg Masala / Pepper Fry"]
        }
    },
    30: {
        "dayNumber": 30,
        "weekday": "Friday",
        "breakfast": {
            "timing_label": "7:00 AM - 8:45 AM",
            "main_items": "Idly, Sambar, Karuppati Pongal & Meduvadai",
            "dishes": ["Idly", "Sambar", "Karuppati Pongal", "Meduvadai", "Coconut Chutney", "Tea / Coffee / Milk"]
        },
        "lunch": {
            "timing_label": "12:15 PM - 1:30 PM",
            "main_items": "Rice, Vathal Puli Kulambu, Kollu Rasam & Snake Gourd Poriyal",
            "dishes": ["Steamed Rice", "Vathal Puli Kulambu", "Kollu Rasam", "Snake Gourd Poriyal", "Appalam", "Curd"]
        },
        "dinner": {
            "timing_label": "7:00 PM - 8:45 PM",
            "main_items": "Parotta, Soya Kuruma & Vegetable Biryani",
            "dishes": ["Parotta", "Soya Kuruma", "Vegetable Biryani (Yellow)", "Curd Rice", "Coconut Chutney", "Banana"]
        }
    },
    31: {
        "dayNumber": 31,
        "weekday": "Saturday",
        "breakfast": {
            "timing_label": "7:00 AM - 8:45 AM",
            "main_items": "Onion Dosa, Kuruma & Aval Upma",
            "dishes": ["Onion Dosa", "Kuruma", "Aval Upma", "Kara Chutney", "Tea / Coffee / Milk"]
        },
        "lunch": {
            "timing_label": "12:15 PM - 1:30 PM",
            "main_items": "Rice, Drumstick Sambar, Rasam & Paruppu Vadai",
            "dishes": ["Steamed Rice", "Drumstick Sambar", "Rasam", "Payasam + Poriyal", "Paruppu Vadai", "Butter Milk"]
        },
        "dinner": {
            "timing_label": "7:00 PM - 8:45 PM",
            "main_items": "Idly, Sambar & Noodles",
            "dishes": ["Idly", "Sambar", "Noodles (Rice / Normal)", "Curd Rice", "Coconut Chutney", "Rose Milk / Chukku Milk"]
        }
    }
}

def get_menu_for_date(date_input: Optional[str] = None) -> List[Dict[str, Any]]:
    """Returns Breakfast, Lunch, Dinner menus for a given YYYY-MM-DD or today's calendar day (1..31)."""
    day_num = 1
    if not date_input:
        day_num = datetime.date.today().day
    else:
        try:
            parts = date_input.split('-')
            if len(parts) == 3:
                day_num = int(parts[2])
            else:
                day_num = datetime.date.fromisoformat(date_input).day
        except Exception:
            day_num = 1

    if day_num < 1:
        day_num = 1
    if day_num > 31:
        day_num = ((day_num - 1) % 31) + 1

    schedule = MONTHLY_MESS_MENU.get(day_num, MONTHLY_MESS_MENU[1])

    return [
        {
            "id": f"menu_breakfast_d{day_num}",
            "meal_type": "Breakfast",
            "timing_label": schedule["breakfast"]["timing_label"],
            "main_items": schedule["breakfast"]["main_items"],
            "dishes": schedule["breakfast"]["dishes"]
        },
        {
            "id": f"menu_lunch_d{day_num}",
            "meal_type": "Lunch",
            "timing_label": schedule["lunch"]["timing_label"],
            "main_items": schedule["lunch"]["main_items"],
            "dishes": schedule["lunch"]["dishes"]
        },
        {
            "id": f"menu_dinner_d{day_num}",
            "meal_type": "Dinner",
            "timing_label": schedule["dinner"]["timing_label"],
            "main_items": schedule["dinner"]["main_items"],
            "dishes": schedule["dinner"]["dishes"]
        }
    ]

def get_all_monthly_menus() -> List[Dict[str, Any]]:
    return list(MONTHLY_MESS_MENU.values())
