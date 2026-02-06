"""
🏨 RITUMBHARA RESORT AI CONCIERGE
Beautiful, Fast, Intelligent - Single File Streamlit App
Enhanced RAG System with Complete Resort Knowledge
"""

import streamlit as st
import json
import re
from datetime import datetime
from typing import List, Dict, Tuple
import hashlib

# ============================================================================
# CONFIGURATION & SETUP
# ============================================================================

st.set_page_config(
    page_title="Ritumbhara Resort - AI Concierge",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# STUNNING CUSTOM CSS - LUXURY RESORT THEME
# ============================================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700&display=swap');

:root{
  --bg: #f6f8f9;            /* page background */
  --panel: #ffffff;         /* card/panel backgrounds */
  --muted: #f1f4f5;         /* subtle surfaces */
  --text: #1f2933;          /* primary text (dark) */
  --accent: #0b6b4f;        /* primary accent (green) */
  --accent-2: #b88c2f;      /* secondary accent (muted gold) */
  --shadow: 0 6px 20px rgba(31,41,51,0.06);
  --radius: 12px;
  --glass: rgba(255,255,255,0.6);
}

/* Apply readable base font */
html, body, [class^="css"], .main {
  font-family: 'Lato', system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
  color: var(--text);
  background: linear-gradient(180deg, var(--bg) 0%, #ffffff 100%);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Hide Streamlit chrome safely */
#MainMenu, footer, header { visibility: hidden; height: 0; }

/* --------- Page containers --------- */
.main {
  padding: 1.25rem;
  box-sizing: border-box;
}

/* Hero / Header: compact, professional */
.hero-header{
  background: linear-gradient(90deg, rgba(11,107,79,0.07), rgba(184,140,47,0.03));
  border-radius: calc(var(--radius) + 4px);
  padding: clamp(1rem, 2.5vw, 2rem);
  margin-bottom: 1.25rem;
  box-shadow: var(--shadow);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.375rem;
}

.hero-title {
  font-weight: 700;
  letter-spacing: -0.02em;
  margin: 0;
  color: var(--text);
  /* responsive size */
  font-size: clamp(1.4rem, 3.5vw, 2.25rem);
  text-align: center;
}

.hero-subtitle {
  color: var(--accent);
  font-weight: 400;
  margin: 0;
  font-size: clamp(0.9rem, 1.4vw, 1.05rem);
  text-align: center;
}

/* --------- Panels / Cards --------- */
.card, .info-card, .feature-card, .source-card {
  background: var(--panel);
  border-radius: var(--radius);
  padding: 1rem;
  margin-bottom: 0.9rem;
  box-shadow: var(--shadow);
  border: 1px solid rgba(31,41,51,0.04);
  box-sizing: border-box;
}

/* info card heading */
.info-card-title, .feature-title {
  font-weight: 700;
  margin-bottom: 0.4rem;
  color: var(--text);
}

.info-card-content {
  color: rgba(31,41,51,0.9);
  line-height: 1.5;
  font-size: 0.95rem;
}

/* feature card accent */
.feature-card {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  border-left: 4px solid var(--accent);
}

/* feature icon */
.feature-icon { font-size: 1.6rem; }

/* source badge */
.source-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px; height: 28px;
  font-weight: 700;
  border-radius: 50%;
  background: var(--accent);
  color: #fff;
  margin-right: 0.6rem;
  font-size: 0.85rem;
}

/* --------- Chat / Messages (improved contrast) --------- */
/* container for messages: neutral, readable */
.chat-container {
  background: var(--muted);
  border-radius: calc(var(--radius) - 2px);
  padding: 1rem;
  min-height: 360px;
  box-shadow: var(--shadow);
  box-sizing: border-box;
}

/* Generic message bubble */
.stChatMessage {
  border-radius: 12px !important;
  padding: 0.9rem !important;
  margin: 0.65rem 0 !important;
  box-shadow: 0 2px 8px rgba(16,24,32,0.03) !important;
  color: var(--text) !important;
  font-size: 0.95rem !important;
  border: 1px solid rgba(31,41,51,0.04) !important;
  background: var(--panel) !important;
  max-width: 92%;
  word-break: break-word;
}

/* User messages — light background, strong text */
.stChatMessage[data-testid*="user"] {
  background: linear-gradient(180deg, #ffffff 0%, #fbfdff 100%) !important;
  color: var(--text) !important;
  align-self: flex-end;
  border-left: 4px solid rgba(11,107,79,0.08) !important;
}

/* Assistant messages — slightly tinted accent with white text for contrast */
.stChatMessage[data-testid*="assistant"] {
  background: linear-gradient(180deg, rgba(11,107,79,0.95), rgba(11,107,79,0.92)) !important;
  color: #ffffff !important;
  border-left: 4px solid rgba(184,140,47,0.12) !important;
  align-self: flex-start;
}

/* Make sure any links in messages are readable */
.stChatMessage a { color: #e7f7ef !important; text-decoration: underline; }

/* Chat input area — visible divider and comfortable padding */
.stChatInputContainer, .stTextInput, textarea, input[type="text"] {
  background: #fff;
  border-radius: 10px;
  padding: 0.6rem;
  border: 1px solid rgba(31,41,51,0.06);
  box-shadow: none;
  font-size: 0.95rem;
  color: var(--text);
  width: 100%;
  box-sizing: border-box;
}

.stChatInputContainer {
  border-top: 1px solid rgba(31,41,51,0.04);
  padding-top: 0.75rem;
}

/* Placeholder color */
.stTextInput::placeholder, textarea::placeholder { color: rgba(31,41,51,0.45); }

/* --------- Buttons (accessible) --------- */
.stButton>button {
  background: linear-gradient(180deg, var(--accent) 0%, var(--accent-2) 100%);
  color: #fff;
  border: none;
  border-radius: 999px;
  padding: 0.6rem 1.1rem;
  font-weight: 700;
  cursor: pointer;
  transition: transform .12s ease, box-shadow .12s ease;
  box-shadow: 0 6px 18px rgba(11,107,79,0.12);
  width: auto;
  white-space: nowrap;
}

.stButton>button:hover { transform: translateY(-2px); box-shadow: 0 12px 30px rgba(11,107,79,0.12); }
.stButton>button:focus { outline: 3px solid rgba(11,107,79,0.12); outline-offset: 2px; }

/* --------- Sidebar --------- */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0b6b4f 0%, #0b6b4f 100%);
  padding: 1.25rem;
  color: #fff;
  min-width: 220px;
  box-sizing: border-box;
}

[data-testid="stSidebar"] h2, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
  color: #fff !important;
}

/* --------- Stats box --------- */
.stats-box {
  background: linear-gradient(90deg, rgba(11,107,79,0.92), rgba(11,107,79,0.85));
  color: #fff;
  padding: 0.9rem;
  border-radius: 10px;
  text-align: center;
}
.stats-number { font-weight: 700; font-size: 1.6rem; font-family: 'Lato', sans-serif; }

/* --------- Scrollbar (subtle) --------- */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, rgba(11,107,79,0.75), rgba(11,107,79,0.95));
  border-radius: 8px;
}

/* --------- Small utility / accessibility improvements --------- */
/* ensure focus visibility for keyboard users */
button:focus, a:focus, input:focus, textarea:focus { box-shadow: 0 0 0 3px rgba(11,107,79,0.08); }

@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; transition: none !important; }
}

/* =========================
   RESPONSIVE MEDIA QUERIES
   ========================= */

/* Very small phones — <= 360px */
@media (max-width: 360px) {
  .main { padding: 0.5rem; }
  .hero-header { padding: 0.8rem; border-radius: 10px; }
  .hero-title { font-size: 1.1rem; }
  .hero-subtitle { font-size: 0.85rem; }
  .card, .info-card, .feature-card, .source-card { padding: 0.7rem; border-radius: 8px; }
  .feature-icon { font-size: 1.25rem; }
  .chat-container { min-height: 260px; padding: 0.6rem; }
  .stChatMessage { font-size: 0.88rem !important; padding: 0.6rem !important; }
  .stButton>button { padding: 0.55rem 0.8rem; font-size: 0.92rem; width: 100%; }
  [data-testid="stSidebar"] { padding: 0.9rem; min-width: 180px; }
}

/* Small phones — <= 480px */
@media (max-width: 480px) {
  .hero-title { font-size: 1.2rem; }
  .info-card-content { font-size: 0.9rem; }
  .feature-card { gap: 0.5rem; }
  .feature-icon { font-size: 1.4rem; }
  .chat-container { min-height: 300px; }
  .stChatMessage { max-width: 94%; }
  .stButton>button { width: 100%; display: block; }
}

/* Narrow phones & phablets — <= 600px */
@media (max-width: 600px) {
  .hero-header { padding: 1rem; }
  .card, .info-card, .feature-card, .source-card { padding: 0.85rem; }
  .feature-card { flex-direction: column; align-items: flex-start; }
  .feature-title { font-size: 1rem; }
  .source-number { width: 26px; height: 26px; font-size: 0.8rem; }
  .stChatMessage { font-size: 0.92rem !important; }
  .stats-number { font-size: 1.3rem; }
  [data-testid="stSidebar"] { display: block; width: 100%; min-width: unset; position: relative; }
}

/* Tablets — <= 768px */
@media (max-width: 768px) {
  .main { padding: 0.9rem; }
  .hero-title { font-size: 1.5rem; }
  .hero-subtitle { font-size: 0.98rem; }
  .card, .info-card, .feature-card { padding: 0.95rem; }
  .chat-container { min-height: 320px; }
  .stChatMessage { max-width: 88%; }
  .stButton>button { font-size: 0.98rem; padding: 0.55rem 0.9rem; width: 100%; }
  .feature-card { gap: 0.6rem; }
}

/* Small laptops — <= 1024px */
@media (max-width: 1024px) {
  .main { padding: 1rem; }
  .hero-title { font-size: clamp(1.6rem, 2.4vw, 1.9rem); }
  .card, .info-card, .feature-card { padding: 1rem; }
  .chat-container { min-height: 340px; }
  [data-testid="stSidebar"] { min-width: 200px; }
}

/* Laptops / Desktops — <= 1280px */
@media (max-width: 1280px) {
  .hero-title { font-size: clamp(1.8rem, 2.2vw, 2.05rem); }
  .card { padding: 1rem; }
  .chat-container { min-height: 360px; }
}

/* Large desktops — up to very large screens */
@media (min-width: 1281px) {
  .main { max-width: 1300px; margin: 0 auto; }
  .hero-title { font-size: clamp(2.0rem, 1.6vw, 2.5rem); }
  .chat-container { min-height: 420px; }
}

/* Extremely wide displays */
@media (min-width: 1600px) {
  .main { max-width: 1500px; padding: 2rem; }
  .hero-title { font-size: clamp(2.2rem, 1.2vw, 3rem); }
  .card { padding: 1.25rem; }
}

</style>

""", unsafe_allow_html=True)

# ============================================================================
# COMPREHENSIVE RESORT KNOWLEDGE BASE
# ============================================================================

RITUMBHARA_KNOWLEDGE = {
    "basic_info": {
        "name": "Ritumbhara Resort",
        "tagline": "Where Luxury Meets Nature",
        "location": "Dhai Pedhi Ka Tiraya, Sariska Road, Alwar, Rajasthan, India",
        "pin_code": "301001",
        "email": "shivamlohiya@ritumbhararesort.com",
        "phone": "+91 9829523881",
        "website": "https://www.ritumbhararesort.com",
        "booking_url": "https://bookings.asiatech.in",
        "membership_url": "https://connect.ritumbhararesort.com",
        "established": "2020",
        "type": "Luxury Resort & Destination Wedding Venue"
    },
    
    "accommodations": {
        "overview": "Ritumbhara Resort offers 9 luxurious rooms designed for comfort and elegance, perfect for families, couples, and business travelers.",
        "room_types": [
            {
                "name": "Deluxe Rooms",
                "count": 6,
                "features": ["King-size bed", "Air conditioning", "LED TV with cable", "Mini fridge", "Tea/coffee maker", "Private balcony", "Attached bathroom with hot water", "Free WiFi", "Room service"],
                "ideal_for": "Couples and solo travelers",
                "size": "350 sq ft"
            },
            {
                "name": "Luxury Cottages",
                "count": 3,
                "features": ["Private cottage experience", "Living area with sofa", "King/Twin beds", "Premium bathroom amenities", "Garden view", "Extra space for families", "Work desk", "Wardrobe", "All deluxe amenities included"],
                "ideal_for": "Families and extended stays",
                "size": "500 sq ft"
            }
        ],
        "check_in": "2:00 PM",
        "check_out": "11:00 AM",
        "early_checkin": "Available on request (subject to availability)",
        "late_checkout": "Available with extra charges"
    },
    
    "amenities": {
        "recreational": [
            {
                "name": "Swimming Pool",
                "description": "Large outdoor swimming pool with crystal-clear water, surrounded by lush greenery. Perfect for relaxation and family fun.",
                "timings": "6:00 AM - 8:00 PM",
                "features": ["Separate kids section", "Pool loungers", "Umbrellas", "Changing rooms", "Lifeguard on duty"]
            },
            {
                "name": "Spa & Wellness Center",
                "description": "Rejuvenate your body and mind with our traditional and modern spa treatments.",
                "services": ["Swedish massage", "Deep tissue massage", "Aromatherapy", "Facial treatments", "Body scrubs", "Couple spa packages"],
                "timings": "10:00 AM - 8:00 PM"
            },
            {
                "name": "Outdoor Sports",
                "description": "Stay active during your stay with various outdoor activities.",
                "activities": ["Badminton court", "Volleyball court", "Children's play area", "Jogging track", "Yoga sessions (morning)"]
            }
        ],
        
        "dining": {
            "restaurant": {
                "name": "The Green Leaf Restaurant",
                "description": "Multi-cuisine restaurant serving authentic Rajasthani, North Indian, South Indian, and Continental dishes.",
                "cuisines": ["Rajasthani", "North Indian", "South Indian", "Continental", "Chinese"],
                "specialties": ["Dal Baati Churma", "Laal Maas", "Gatte ki Sabzi", "Fresh Tandoor items", "Live cooking stations"],
                "timings": {
                    "breakfast": "7:30 AM - 10:30 AM",
                    "lunch": "12:30 PM - 3:30 PM",
                    "dinner": "7:30 PM - 11:00 PM"
                },
                "seating": "Indoor and outdoor seating available"
            },
            "room_service": "24/7 room service available for in-room dining"
        },
        
        "facilities": [
            "Free WiFi throughout the property",
            "Ample parking space for 50+ vehicles",
            "24/7 security and CCTV surveillance",
            "Power backup",
            "Laundry and dry cleaning services",
            "Travel desk for tour arrangements",
            "Doctor on call",
            "Wheelchair accessibility",
            "Pet-friendly (prior intimation required)"
        ]
    },
    
    "events_and_weddings": {
        "banquet_hall": {
            "name": "Royal Banquet Hall",
            "capacity": {
                "theatre_style": 300,
                "cluster_seating": 200,
                "u_shape": 100
            },
            "size": "5000 sq ft",
            "features": ["Fully air-conditioned", "State-of-the-art sound system", "LED projector and screen", "Stage setup", "Professional lighting", "Green rooms", "Valet parking"],
            "ideal_for": "Corporate events, conferences, seminars, product launches"
        },
        
        "lawn_area": {
            "name": "Emerald Lawn",
            "capacity": 500,
            "size": "15,000 sq ft",
            "features": ["Lush green open space", "Gazebo for ceremonies", "Decorative lighting options", "Outdoor catering setup", "Bar counter facility", "Ample parking"],
            "ideal_for": "Weddings, receptions, outdoor parties, cultural events"
        },
        
        "wedding_services": [
            "Customized wedding planning and coordination",
            "Decoration services (floral, traditional, theme-based)",
            "Bridal room setup",
            "Guest accommodation packages",
            "Photography and videography coordination",
            "Entertainment arrangements (DJ, live band, folk artists)",
            "Mehendi and sangeet setup",
            "Catering services with customizable menus",
            "Valet parking and guest management",
            "Destination wedding packages"
        ],
        
        "corporate_services": [
            "Conference room setup",
            "Audio-visual equipment",
            "High-speed internet",
            "Stationery and writing pads",
            "Tea/coffee breaks",
            "Business center facilities",
            "Team building activities"
        ]
    },
    
    "nearby_attractions": [
        {
            "name": "Sariska Tiger Reserve",
            "distance": "35 km (45 min drive)",
            "description": "Famous wildlife sanctuary home to Bengal tigers, leopards, and diverse flora and fauna. Safari tours available.",
            "activities": ["Jungle safari", "Wildlife photography", "Bird watching", "Nature trails"]
        },
        {
            "name": "Siliserh Lake",
            "distance": "18.4 km (25 min drive)",
            "description": "Scenic lake with a beautiful palace, perfect for boating and picnics.",
            "activities": ["Boating", "Picnic", "Photography", "Palace visit"]
        },
        {
            "name": "Bala Fort (Alwar Fort)",
            "distance": "15 km (20 min drive)",
            "description": "Historic fort with panoramic views of the city. Rich in Rajput architecture and history.",
            "timings": "9:00 AM - 5:00 PM"
        },
        {
            "name": "Moosi Maharani Ki Chhatri",
            "distance": "9 km (15 min drive)",
            "description": "Stunning cenotaphs showcasing intricate architecture and beautiful gardens.",
            "best_time": "Morning and evening for photography"
        },
        {
            "name": "City Palace Alwar",
            "distance": "12 km (18 min drive)",
            "description": "Magnificent palace with museum displaying royal artifacts, weapons, and paintings."
        },
        {
            "name": "Pandupol Hanuman Temple",
            "distance": "28 km (40 min drive)",
            "description": "Ancient temple located in the Sariska hills, known for religious significance and natural beauty."
        }
    ],
    
    "packages_and_offers": [
        {
            "name": "Weekend Getaway Package",
            "duration": "2 Days / 1 Night",
            "includes": ["Deluxe room accommodation", "Breakfast and dinner", "Welcome drink", "Swimming pool access", "Early check-in (subject to availability)"],
            "ideal_for": "Couples and families"
        },
        {
            "name": "Destination Wedding Package",
            "includes": ["Venue booking (lawn + banquet)", "Guest rooms at special rates", "Decoration coordination", "Catering services", "Event planning support", "Photography area setup"],
            "note": "Customizable based on guest count and requirements"
        },
        {
            "name": "Corporate Retreat Package",
            "includes": ["Conference room with AV equipment", "Team accommodation", "All meals", "Team building activities", "Outdoor sports facilities", "WiFi and business support"],
            "ideal_for": "Corporate teams and organizations"
        }
    ],
    
    "booking_and_policies": {
        "how_to_book": [
            "Online: Visit https://bookings.asiatech.in",
            "Phone: Call +91 9829523881",
            "Email: Send inquiry to shivamlohiya@ritumbhararesort.com",
            "Walk-in: Visit the resort directly (subject to availability)"
        ],
        "payment_methods": ["Cash", "Credit/Debit Cards", "UPI", "Net Banking", "Payment Gateway (online)"],
        "cancellation_policy": {
            "before_7_days": "Full refund minus processing fee",
            "3_to_7_days": "50% refund",
            "less_than_3_days": "No refund",
            "note": "Cancellation policies may vary for events and group bookings"
        },
        "id_proof": "Valid government ID required at check-in (Aadhar, PAN, Passport, Driving License)"
    },
    
    "special_features": [
        "Eco-friendly practices with rainwater harvesting",
        "Solar-powered water heating",
        "Organic garden for fresh vegetables",
        "Traditional Rajasthani cultural performances (on request)",
        "Bonfire and barbecue nights",
        "Customized birthday and anniversary celebrations",
        "Kids-friendly with play area and games",
        "Pet-friendly accommodations"
    ],
    
    "testimonials": [
        {
            "guest": "Priya & Rahul",
            "rating": 5,
            "comment": "Perfect destination wedding venue! The staff was incredibly supportive, food was delicious, and our guests loved the accommodations."
        },
        {
            "guest": "Amit Sharma",
            "rating": 5,
            "comment": "Great place for a weekend getaway. The pool is amazing, rooms are clean, and the location is peaceful yet accessible."
        },
        {
            "guest": "Corporate Team - Tech Solutions Inc",
            "rating": 5,
            "comment": "Excellent venue for our annual retreat. Conference facilities were top-notch, and the team enjoyed the outdoor activities."
        }
    ],
    
    "faq": [
        {
            "question": "Is the resort suitable for destination weddings?",
            "answer": "Yes! Ritumbhara Resort specializes in destination weddings with a beautiful lawn that can accommodate 500+ guests, banquet hall, customized decoration, catering services, and guest accommodations. We offer complete wedding planning support."
        },
        {
            "question": "How far is the resort from Alwar city?",
            "answer": "The resort is located on Sariska Road, approximately 12-15 km from Alwar city center. It takes about 20 minutes by car."
        },
        {
            "question": "Are pets allowed?",
            "answer": "Yes, we are pet-friendly! Please inform us in advance when making your reservation so we can make necessary arrangements."
        },
        {
            "question": "Is swimming pool accessible year-round?",
            "answer": "Yes, the swimming pool is operational throughout the year from 6:00 AM to 8:00 PM, weather permitting."
        },
        {
            "question": "Do you provide airport/railway transfer?",
            "answer": "Yes, we can arrange pick-up and drop services from Alwar Railway Station or Delhi/Jaipur airports at additional charges. Please contact us in advance."
        },
        {
            "question": "What are the check-in and check-out times?",
            "answer": "Check-in is at 2:00 PM and check-out is at 11:00 AM. Early check-in and late check-out can be arranged subject to availability and additional charges."
        },
        {
            "question": "Is WiFi available?",
            "answer": "Yes, complimentary high-speed WiFi is available throughout the resort including rooms, restaurant, and common areas."
        }
    ]
}

# ============================================================================
# ENHANCED RAG SYSTEM - SMART RETRIEVAL & RANKING
# ============================================================================

def create_knowledge_chunks() -> List[Dict]:
    """Convert knowledge base into searchable chunks with metadata"""
    chunks = []
    chunk_id = 0
    
    # Basic Information
    basic = RITUMBHARA_KNOWLEDGE["basic_info"]
    chunks.append({
        "id": chunk_id,
        "text": f"Ritumbhara Resort is located at {basic['location']}. Contact: {basic['phone']}, Email: {basic['email']}. Book online at {basic['booking_url']}. It's a {basic['type']} established in {basic['established']}.",
        "category": "basic_info",
        "keywords": ["contact", "location", "address", "phone", "email", "booking", "book", "where", "how to reach"]
    })
    chunk_id += 1
    
    # Accommodations
    for room in RITUMBHARA_KNOWLEDGE["accommodations"]["room_types"]:
        chunks.append({
            "id": chunk_id,
            "text": f"{room['name']}: {room['count']} rooms available. Size: {room['size']}. Features: {', '.join(room['features'])}. Ideal for {room['ideal_for']}.",
            "category": "accommodations",
            "keywords": ["room", "accommodation", "stay", "cottage", "deluxe", "features", "amenities", "bed", "sleep"]
        })
        chunk_id += 1
    
    chunks.append({
        "id": chunk_id,
        "text": f"Check-in time: {RITUMBHARA_KNOWLEDGE['accommodations']['check_in']}, Check-out: {RITUMBHARA_KNOWLEDGE['accommodations']['check_out']}. Early check-in: {RITUMBHARA_KNOWLEDGE['accommodations']['early_checkin']}. Late checkout: {RITUMBHARA_KNOWLEDGE['accommodations']['late_checkout']}.",
        "category": "accommodations",
        "keywords": ["check-in", "checkout", "check in", "check out", "time", "early", "late", "timing"]
    })
    chunk_id += 1
    
    # Recreational Amenities
    for amenity in RITUMBHARA_KNOWLEDGE["amenities"]["recreational"]:
        features_text = ""
        if "features" in amenity:
            features_text = f" Features: {', '.join(amenity['features'])}."
        elif "services" in amenity:
            features_text = f" Services: {', '.join(amenity['services'])}."
        elif "activities" in amenity:
            features_text = f" Activities: {', '.join(amenity['activities'])}."
        
        timing_text = f" Timings: {amenity['timings']}" if "timings" in amenity else ""
        
        chunks.append({
            "id": chunk_id,
            "text": f"{amenity['name']}: {amenity['description']}{features_text}{timing_text}",
            "category": "amenities",
            "keywords": ["pool", "swimming", "spa", "wellness", "massage", "sports", "activities", "recreation", "fitness", "yoga"]
        })
        chunk_id += 1
    
    # Dining
    dining = RITUMBHARA_KNOWLEDGE["amenities"]["dining"]["restaurant"]
    chunks.append({
        "id": chunk_id,
        "text": f"{dining['name']}: {dining['description']} Cuisines: {', '.join(dining['cuisines'])}. Specialties: {', '.join(dining['specialties'])}. Breakfast: {dining['timings']['breakfast']}, Lunch: {dining['timings']['lunch']}, Dinner: {dining['timings']['dinner']}. {dining['seating']}",
        "category": "dining",
        "keywords": ["food", "restaurant", "dining", "eat", "meal", "breakfast", "lunch", "dinner", "cuisine", "menu"]
    })
    chunk_id += 1
    
    chunks.append({
        "id": chunk_id,
        "text": f"24/7 room service available for in-room dining. Order food anytime during your stay.",
        "category": "dining",
        "keywords": ["room service", "in-room dining", "order food", "24/7", "delivery"]
    })
    chunk_id += 1
    
    # Facilities
    chunks.append({
        "id": chunk_id,
        "text": f"General Facilities: {', '.join(RITUMBHARA_KNOWLEDGE['amenities']['facilities'])}",
        "category": "facilities",
        "keywords": ["wifi", "parking", "security", "laundry", "doctor", "wheelchair", "pet", "facilities"]
    })
    chunk_id += 1
    
    # Events - Banquet
    banquet = RITUMBHARA_KNOWLEDGE["events_and_weddings"]["banquet_hall"]
    chunks.append({
        "id": chunk_id,
        "text": f"{banquet['name']}: {banquet['size']} hall. Capacity: Theatre {banquet['capacity']['theatre_style']}, Cluster {banquet['capacity']['cluster_seating']}, U-shape {banquet['capacity']['u_shape']} people. Features: {', '.join(banquet['features'])}. Ideal for {banquet['ideal_for']}.",
        "category": "events",
        "keywords": ["banquet", "hall", "conference", "meeting", "seminar", "corporate", "event", "capacity"]
    })
    chunk_id += 1
    
    # Events - Lawn
    lawn = RITUMBHARA_KNOWLEDGE["events_and_weddings"]["lawn_area"]
    chunks.append({
        "id": chunk_id,
        "text": f"{lawn['name']}: {lawn['size']} outdoor lawn. Capacity: {lawn['capacity']} people. Features: {', '.join(lawn['features'])}. Ideal for {lawn['ideal_for']}.",
        "category": "events",
        "keywords": ["lawn", "outdoor", "wedding", "reception", "party", "event", "garden"]
    })
    chunk_id += 1
    
    # Wedding Services
    chunks.append({
        "id": chunk_id,
        "text": f"Wedding Services: {', '.join(RITUMBHARA_KNOWLEDGE['events_and_weddings']['wedding_services'])}",
        "category": "weddings",
        "keywords": ["wedding", "marriage", "bride", "groom", "destination wedding", "ceremony", "celebration"]
    })
    chunk_id += 1
    
    # Corporate Services
    chunks.append({
        "id": chunk_id,
        "text": f"Corporate Services: {', '.join(RITUMBHARA_KNOWLEDGE['events_and_weddings']['corporate_services'])}",
        "category": "corporate",
        "keywords": ["corporate", "business", "conference", "meeting", "team", "office"]
    })
    chunk_id += 1
    
    # Nearby Attractions
    for attraction in RITUMBHARA_KNOWLEDGE["nearby_attractions"]:
        activities_text = f" Activities: {', '.join(attraction['activities'])}" if "activities" in attraction else ""
        timings_text = f" Timings: {attraction['timings']}" if "timings" in attraction else ""
        best_time_text = f" Best time: {attraction['best_time']}" if "best_time" in attraction else ""
        
        chunks.append({
            "id": chunk_id,
            "text": f"{attraction['name']}: {attraction['distance']}. {attraction['description']}{activities_text}{timings_text}{best_time_text}",
            "category": "attractions",
            "keywords": ["nearby", "attraction", "visit", "sightseeing", "places", "tourist", "sariska", "fort", "lake", "temple"]
        })
        chunk_id += 1
    
    # Packages
    for package in RITUMBHARA_KNOWLEDGE["packages_and_offers"]:
        duration_text = f" Duration: {package['duration']}" if "duration" in package else ""
        ideal_text = f" Ideal for: {package['ideal_for']}" if "ideal_for" in package else ""
        note_text = f" Note: {package['note']}" if "note" in package else ""
        
        chunks.append({
            "id": chunk_id,
            "text": f"{package['name']}{duration_text}. Includes: {', '.join(package['includes'])}.{ideal_text}{note_text}",
            "category": "packages",
            "keywords": ["package", "offer", "deal", "weekend", "getaway", "corporate", "retreat"]
        })
        chunk_id += 1
    
    # Booking
    chunks.append({
        "id": chunk_id,
        "text": f"How to Book: {', '.join(RITUMBHARA_KNOWLEDGE['booking_and_policies']['how_to_book'])}. Payment methods: {', '.join(RITUMBHARA_KNOWLEDGE['booking_and_policies']['payment_methods'])}.",
        "category": "booking",
        "keywords": ["book", "booking", "reservation", "payment", "online", "how to book"]
    })
    chunk_id += 1
    
    # Cancellation
    cancel = RITUMBHARA_KNOWLEDGE["booking_and_policies"]["cancellation_policy"]
    chunks.append({
        "id": chunk_id,
        "text": f"Cancellation Policy: Before 7 days - {cancel['before_7_days']}, 3-7 days - {cancel['3_to_7_days']}, Less than 3 days - {cancel['less_than_3_days']}. {cancel['note']}",
        "category": "policies",
        "keywords": ["cancel", "cancellation", "refund", "policy"]
    })
    chunk_id += 1
    
    # FAQs
    for faq in RITUMBHARA_KNOWLEDGE["faq"]:
        chunks.append({
            "id": chunk_id,
            "text": f"Q: {faq['question']} A: {faq['answer']}",
            "category": "faq",
            "keywords": faq['question'].lower().split()
        })
        chunk_id += 1
    
    return chunks

def simple_tokenize(text: str) -> List[str]:
    """Simple tokenization for matching"""
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    return text.split()

def calculate_relevance_score(query: str, chunk: Dict) -> float:
    """Calculate relevance score using keyword matching and TF-IDF-like approach"""
    query_tokens = set(simple_tokenize(query))
    chunk_text_tokens = set(simple_tokenize(chunk["text"]))
    chunk_keywords = set(chunk["keywords"])
    
    # Exact keyword matches (highest weight)
    keyword_matches = len(query_tokens.intersection(chunk_keywords))
    
    # Text content matches
    text_matches = len(query_tokens.intersection(chunk_text_tokens))
    
    # Calculate score
    score = (keyword_matches * 3.0) + (text_matches * 1.0)
    
    # Boost for category-specific queries
    category_boosts = {
        "booking": ["book", "reservation", "reserve", "available"],
        "accommodations": ["room", "stay", "accommodation", "cottage"],
        "dining": ["food", "restaurant", "eat", "meal"],
        "weddings": ["wedding", "marriage", "bride", "groom"],
        "events": ["event", "conference", "meeting", "banquet"],
        "attractions": ["nearby", "visit", "sightseeing", "places"]
    }
    
    for category, boost_words in category_boosts.items():
        if chunk["category"] == category:
            if any(word in query.lower() for word in boost_words):
                score *= 1.5
    
    return score

def retrieve_relevant_chunks(query: str, top_k: int = 5) -> List[Dict]:
    """Retrieve most relevant chunks using enhanced ranking"""
    all_chunks = st.session_state.knowledge_chunks
    
    # Calculate scores
    scored_chunks = []
    for chunk in all_chunks:
        score = calculate_relevance_score(query, chunk)
        if score > 0:  # Only include chunks with some relevance
            scored_chunks.append((score, chunk))
    
    # Sort by score
    scored_chunks.sort(reverse=True, key=lambda x: x[0])
    
    # Return top_k
    return [chunk for score, chunk in scored_chunks[:top_k]]

def generate_smart_response(query: str, relevant_chunks: List[Dict]) -> str:
    """Generate intelligent response based on query type and context"""
    
    if not relevant_chunks:
        return f"""I'd be happy to help you! However, I couldn't find specific information about that in my knowledge base.

**For immediate assistance:**
📞 **Call:** +91 9829523881
✉️ **Email:** shivamlohiya@ritumbhararesort.com
🌐 **Book Online:** https://bookings.asiatech.in

Could you please rephrase your question or ask about:
• Room accommodations and amenities
• Dining and restaurant services
• Wedding and event planning
• Nearby attractions and sightseeing
• Booking and packages"""
    
    query_lower = query.lower()
    
    # Detect query intent
    intent = detect_intent(query_lower)
    
    # Generate response based on intent
    if intent == "booking":
        return generate_booking_response(relevant_chunks)
    elif intent == "pricing":
        return generate_pricing_response(relevant_chunks)
    elif intent == "wedding":
        return generate_wedding_response(relevant_chunks)
    elif intent == "rooms":
        return generate_rooms_response(relevant_chunks)
    elif intent == "dining":
        return generate_dining_response(relevant_chunks)
    elif intent == "attractions":
        return generate_attractions_response(relevant_chunks)
    elif intent == "events":
        return generate_events_response(relevant_chunks)
    else:
        return generate_general_response(query, relevant_chunks)

def detect_intent(query: str) -> str:
    """Detect user intent from query"""
    if any(word in query for word in ["book", "booking", "reservation", "reserve", "available", "availability"]):
        return "booking"
    elif any(word in query for word in ["price", "cost", "rate", "charge", "fee", "expensive", "cheap", "tariff"]):
        return "pricing"
    elif any(word in query for word in ["wedding", "marriage", "shaadi", "bride", "groom", "ceremony"]):
        return "wedding"
    elif any(word in query for word in ["room", "accommodation", "stay", "cottage", "suite"]):
        return "rooms"
    elif any(word in query for word in ["food", "restaurant", "dining", "eat", "meal", "breakfast", "lunch", "dinner"]):
        return "dining"
    elif any(word in query for word in ["nearby", "visit", "attraction", "sightseeing", "places", "tourist"]):
        return "attractions"
    elif any(word in query for word in ["event", "conference", "meeting", "corporate", "banquet", "seminar"]):
        return "events"
    else:
        return "general"

def generate_booking_response(chunks: List[Dict]) -> str:
    """Generate booking-specific response"""
    response = f"""## 📅 **Ready to Book Your Stay?**

Here's how you can reserve your room at Ritumbhara Resort:

### **Booking Methods:**
🌐 **Online Booking:** [Click here to book now](https://bookings.asiatech.in)
📞 **Call Us:** +91 9829523881
✉️ **Email:** shivamlohiya@ritumbhararesort.com
🏨 **Walk-in:** Visit us directly (subject to availability)

### **What You Need:**
• Valid government ID (Aadhar/PAN/Passport/Driving License)
• Preferred check-in date and duration
• Number of guests

"""
    
    # Add relevant details from chunks
    for chunk in chunks[:2]:
        if chunk["category"] in ["accommodations", "booking", "policies"]:
            response += f"\n💡 **Good to Know:** {chunk['text']}\n"
    
    response += f"""\n### **Payment Options:**
💳 Credit/Debit Cards | 📱 UPI | 💰 Cash | 🌐 Net Banking

**Book now and experience luxury in nature!**"""
    
    return response

def generate_pricing_response(chunks: List[Dict]) -> str:
    """Generate pricing-specific response"""
    return f"""## 💰 **Pricing Information**

For the most accurate and up-to-date pricing, we recommend:

📞 **Call our reservation team:** +91 9829523881
✉️ **Email for quote:** shivamlohiya@ritumbhararesort.com

Our rates vary based on:
• **Season** (peak/off-peak)
• **Room type** (Deluxe/Cottage)
• **Duration of stay**
• **Number of guests**
• **Special events or packages**

### **Available Packages:**
{chunks[0]['text'] if chunks else ''}

### **Special Offers:**
We frequently run promotions! Contact us to learn about:
• Weekend getaway deals
• Corporate packages
• Wedding packages
• Long-stay discounts

**💡 Tip:** Book directly for the best rates!"""

def generate_wedding_response(chunks: List[Dict]) -> str:
    """Generate wedding-specific response"""
    response = f"""## 💍 **Your Dream Wedding at Ritumbhara Resort**

Make your special day unforgettable with our comprehensive wedding services!

### **Venue Highlights:**
"""
    
    for chunk in chunks[:3]:
        if "lawn" in chunk["text"].lower() or "banquet" in chunk["text"].lower() or "wedding" in chunk["text"].lower():
            response += f"✨ {chunk['text']}\n\n"
    
    response += f"""### **Why Choose Us?**
🌿 Beautiful outdoor lawn (500+ guests)
🏛️ Elegant banquet hall (300+ guests)
🛏️ Guest accommodations available
🍽️ Customized catering menus
🎨 Professional decoration services
📸 Photography coordination
🎵 Entertainment arrangements

### **Plan Your Wedding:**
📞 **Call:** +91 9829523881
✉️ **Email:** shivamlohiya@ritumbhararesort.com

Our wedding planners will help create your perfect celebration!"""
    
    return response

def generate_rooms_response(chunks: List[Dict]) -> str:
    """Generate rooms-specific response"""
    response = f"""## 🛏️ **Luxurious Accommodations**

Choose the perfect room for your comfort:

"""
    
    for chunk in chunks[:3]:
        if chunk["category"] == "accommodations":
            response += f"### {chunk['text'].split(':')[0] if ':' in chunk['text'] else 'Room Details'}\n"
            response += f"{chunk['text']}\n\n"
    
    response += f"""### **Standard Amenities:**
✅ Air Conditioning | 📺 LED TV | 🌐 Free WiFi
☕ Tea/Coffee Maker | 🛁 Hot Water | 🧴 Toiletries
🧹 Daily Housekeeping | 📞 24/7 Room Service

**Book your perfect room today!**
📞 +91 9829523881 | 🌐 https://bookings.asiatech.in"""
    
    return response

def generate_dining_response(chunks: List[Dict]) -> str:
    """Generate dining-specific response"""
    response = f"""## 🍽️ **Culinary Delights Await**

"""
    
    for chunk in chunks[:2]:
        if chunk["category"] == "dining":
            response += f"{chunk['text']}\n\n"
    
    response += f"""### **Dining Highlights:**
🌶️ Authentic Rajasthani specialties
🍛 North & South Indian classics
🍝 Continental cuisine
🥘 Chinese favorites
🔥 Live tandoor & cooking stations

### **Perfect For:**
• Romantic dinners
• Family celebrations
• Business meals
• In-room dining comfort

**Reservations:** +91 9829523881"""
    
    return response

def generate_attractions_response(chunks: List[Dict]) -> str:
    """Generate attractions-specific response"""
    response = f"""## 🏞️ **Explore Around Ritumbhara Resort**

Discover the beauty of Alwar! Here are must-visit attractions:

"""
    
    for i, chunk in enumerate(chunks[:4], 1):
        if chunk["category"] == "attractions":
            response += f"**{i}. {chunk['text'].split(':')[0]}**\n{chunk['text'].split(':', 1)[1] if ':' in chunk['text'] else chunk['text']}\n\n"
    
    response += f"""### **Travel Assistance:**
Our travel desk can help arrange:
🚗 Transportation to attractions
📸 Photography tours
🗺️ Guided sightseeing
🎫 Entry ticket assistance

**Contact:** +91 9829523881"""
    
    return response

def generate_events_response(chunks: List[Dict]) -> str:
    """Generate events-specific response"""
    response = f"""## 🎉 **Host Your Perfect Event**

"""
    
    for chunk in chunks[:3]:
        if chunk["category"] in ["events", "corporate"]:
            response += f"**{chunk['text']}**\n\n"
    
    response += f"""### **Event Types We Host:**
• Corporate conferences & seminars
• Product launches
• Team building retreats
• Birthday parties
• Anniversary celebrations
• Cultural events
• Social gatherings

### **Why Choose Us:**
✅ Professional event planning
✅ State-of-the-art facilities
✅ Flexible venue options
✅ Catering services
✅ AV equipment
✅ Ample parking

**Plan Your Event:** 📞 +91 9829523881"""
    
    return response

def generate_general_response(query: str, chunks: List[Dict]) -> str:
    """Generate general response"""
    response = f"""Based on your query, here's what I found:\n\n"""
    
    for i, chunk in enumerate(chunks[:3], 1):
        response += f"**{i}.** {chunk['text']}\n\n"
    
    response += f"""---\n\n**Need more information?**
📞 Call: +91 9829523881
✉️ Email: shivamlohiya@ritumbhararesort.com
🌐 Book: https://bookings.asiatech.in"""
    
    return response

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "knowledge_chunks" not in st.session_state:
    st.session_state.knowledge_chunks = create_knowledge_chunks()

if "chat_count" not in st.session_state:
    st.session_state.chat_count = 0

# ============================================================================
# MAIN HEADER
# ============================================================================

st.markdown("""
<div class="hero-header">
    <h1 class="hero-title">🏨 Ritumbhara Resort</h1>
    <p class="hero-subtitle">AI CONCIERGE AT YOUR SERVICE</p>
    <p class="hero-tagline">Where Luxury Meets Nature • Alwar, Rajasthan</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("### 🎯 Quick Access")
    
    # Contact Card
    st.markdown("""
    <div class="info-card">
        <div class="info-card-title">📞 Contact Us</div>
        <div class="info-card-content">
            <strong>Phone:</strong> +91 9829523881<br>
            <strong>Email:</strong> shivamlohiya@ritumbhararesort.com<br>
            <strong>Address:</strong> Sariska Road, Alwar
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Actions
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔗 Book Now", use_container_width=True):
            st.markdown("[Click here](https://bookings.asiatech.in)")
    with col2:
        if st.button("🌟 Membership", use_container_width=True):
            st.markdown("[Join now](https://connect.ritumbhararesort.com)")
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Features
    st.markdown("### ✨ Resort Highlights")
    
    features = [
        ("🏊", "Swimming Pool", "Outdoor pool with kids section"),
        ("🍽️", "Multi-Cuisine", "Rajasthani & International"),
        ("💒", "Weddings", "500+ guest capacity"),
        ("🏢", "Events", "Corporate & conferences"),
        ("🧘", "Spa & Wellness", "Rejuvenating treatments"),
        ("🌳", "Nature", "Lush green surroundings")
    ]
    
    for icon, title, desc in features:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">{icon}</div>
            <div class="feature-title">{title}</div>
            <div style="font-size: 0.85rem; color: #666;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Stats
    st.markdown("### 📊 Quick Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="stats-box">
            <div class="stats-number">9</div>
            <div class="stats-label">Luxury Rooms</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="stats-box">
            <div class="stats-number">500+</div>
            <div class="stats-label">Event Capacity</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Export & Clear
    if st.session_state.messages:
        if st.button("💾 Export Chat", use_container_width=True):
            transcript = f"RITUMBHARA RESORT - Chat Transcript\n"
            transcript += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            transcript += "="*50 + "\n\n"
            
            for msg in st.session_state.messages:
                transcript += f"{msg['role'].upper()}:\n{msg['content']}\n\n"
                transcript += "-"*50 + "\n\n"
            
            st.download_button(
                "📥 Download Transcript",
                transcript,
                f"ritumbhara_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                "text/plain",
                use_container_width=True
            )
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_count = 0
        st.rerun()
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # Knowledge Base Info
    st.markdown(f"""
    <div style="text-align: center; color: #FFF8E7; font-size: 0.85rem;">
        💡 Knowledge Base Loaded<br>
        {len(st.session_state.knowledge_chunks)} Information Chunks<br>
        Ready to assist!
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# CHAT INTERFACE
# ============================================================================

# Welcome message
if not st.session_state.messages:
    st.markdown("""
    <div class="info-card">
        <div class="info-card-title">👋 Welcome to Ritumbhara Resort!</div>
        <div class="info-card-content">
            I'm your AI concierge, here to help you with:<br><br>
            🛏️ Room bookings and accommodations<br>
            🍽️ Dining and restaurant information<br>
            💒 Wedding and event planning<br>
            🏞️ Nearby attractions and activities<br>
            📞 Contact and booking assistance<br><br>
            <strong>Ask me anything!</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Show sources if available
        if "sources" in message and message["sources"]:
            with st.expander(f"📚 View {len(message['sources'])} Source(s)"):
                for i, source in enumerate(message["sources"], 1):
                    st.markdown(f"""
                    <div class="source-card">
                        <span class="source-number">{i}</span>
                        <strong>{source['category'].replace('_', ' ').title()}</strong><br>
                        {source['text'][:250]}{'...' if len(source['text']) > 250 else ''}
                    </div>
                    """, unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Ask me anything about Ritumbhara Resort..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.chat_count += 1
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Retrieve relevant chunks
            relevant_chunks = retrieve_relevant_chunks(prompt, top_k=5)
            
            # Generate response
            response = generate_smart_response(prompt, relevant_chunks)
            
            # Display response
            st.markdown(response)
            
            # Add to session state
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "sources": relevant_chunks
            })
            
            # Show sources
            if relevant_chunks:
                with st.expander(f"📚 View {len(relevant_chunks)} Source(s)"):
                    for i, source in enumerate(relevant_chunks, 1):
                        st.markdown(f"""
                        <div class="source-card">
                            <span class="source-number">{i}</span>
                            <strong>{source['category'].replace('_', ' ').title()}</strong><br>
                            {source['text'][:250]}{'...' if len(source['text']) > 250 else ''}
                        </div>
                        """, unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; padding: 2rem 1rem; color: #666;">
    <p style="font-family: 'Playfair Display', serif; font-size: 1.2rem; color: #1B4332; margin-bottom: 1rem;">
        🏨 <strong>Ritumbhara Resort</strong> - Where Luxury Meets Nature
    </p>
    <p style="font-size: 0.95rem; margin-bottom: 0.5rem;">
        📍 Sariska Road, Alwar, Rajasthan | 📞 +91 9829523881
    </p>
    <p style="font-size: 0.9rem; color: #888;">
        ✉️ shivamlohiya@ritumbhararesort.com | 🌐 www.ritumbhararesort.com
    </p>
    <p style="font-size: 0.85rem; color: #999; margin-top: 1rem;">
        Powered by AI • Enhanced RAG System • Built with ❤️ using Streamlit
    </p>
</div>
""", unsafe_allow_html=True)
