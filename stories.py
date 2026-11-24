"""The news of Monday 23 November 2026, as data.

Every item was checked against a dated report from 23 November 2026 (any time zone).
Labels say how sure the page is:
  CONFIRMED  several outlets, or official market/seismic data
  OFFICIAL   a government, agency or company statement
  REPORTED   carried by a news wire or outlet
  CLAIM      one side's account, not independently confirmed
  ONGOING    a new development (toll, update) in an earlier event
"""

DAY = "Monday 23 November 2026"

KICKER = ("Huang back at Nvidia, Wall Street soars \u00b7 EU drafts 22nd Russia sanctions package "
          "\u00b7 Kyiv claims a Russian warship sunk in Libya")

# region keys -> display name, colour
REGIONS = {
    "NAM": ("N. AMERICA", (37, 99, 196)),
    "LAT": ("LATIN AM. & CARIB.", (150, 70, 170)),
    "EUR": ("EUROPE", (30, 120, 150)),
    "MEA": ("MIDDLE EAST", (196, 72, 52)),
    "AFR": ("AFRICA", (44, 140, 72)),
    "ASI": ("ASIA", (214, 120, 20)),
    "OCE": ("OCEANIA", (0, 150, 160)),
    "SCI": ("SCIENCE", (90, 96, 110)),
}

LABELS = {
    "CONFIRMED": (32, 128, 70),
    "OFFICIAL": (36, 84, 168),
    "REPORTED": (84, 92, 108),
    "CLAIM": (214, 110, 16),
    "ONGOING": (128, 64, 160),
}

# Hour-by-hour (UTC)
TIMELINE = [
    ("02:40", "M6.5 quake off Vanuatu"),
    ("06:30", "Kospi shuts \u22123.3%"),
    ("07:15", "Drone attack, C\u00facuta"),
    ("08:57", "India\u2013Nepal $1.62bn"),
    ("14:24", "Nvidia recalls Huang"),
    ("15:35", "EU 22nd package"),
    ("21:00", "S&P 500 +4.73% close"),
]

# Big illustrated cards: (no, place, region, field, headline, context, sources, label, scene, lon, lat)
CARDS = [
    (1, "SANTA CLARA, USA", "NAM", "TECH",
     "Nvidia brings back Jensen Huang as CEO",
     "Board vote is unanimous, 11 days after he quit; shares close up 31.48%, best day since 2003.",
     "Reuters \u00b7 CNN \u00b7 WSJ", "CONFIRMED", "chip", -122.0, 37.4),
    (2, "NEW YORK", "NAM", "MARKETS",
     "Wall Street roars back on AI relief",
     "S&P 500 +4.73%, Nasdaq +6.51%, Dow +1,448 points; Wall St's best day since April 2025.",
     "CNN \u00b7 Reuters", "CONFIRMED", "bull", -74.0, 40.7),
    (3, "BRUSSELS", "EUR", "SANCTIONS",
     "EU proposes a 22nd Russia sanctions package",
     "60 banks off SWIFT, crypto curbs, 70+ shadow-fleet ships; all 27 states must agree.",
     "European Commission", "OFFICIAL", "eu", 4.4, 50.8),
    (4, "BENGHAZI, LIBYA", "AFR", "WAR",
     "Kyiv says its sea drones sank a Russian warship",
     "Zelensky claims corvette Merkury, hit on Sunday, sank in port; Tripoli condemns the claim.",
     "Zelensky \u00b7 Reuters \u00b7 CNN", "CLAIM", "ship", 20.1, 32.1),
    (5, "SEOUL", "ASI", "MARKETS",
     "Kospi slides 3.3% in AI-stock rout",
     "Closes at 4,708.54; program trading paused 5 minutes; Samsung \u22123.1%, SK hynix \u22122.5%.",
     "JoongAng Daily \u00b7 Yonhap", "CONFIRMED", "down", 127.0, 37.5),
    (6, "BRUSSELS", "EUR", "SECURITY",
     "NATO envoys meet in emergency talks for Poland",
     "Called after three Russian missiles came down in Poland on Friday; not under Article 4.",
     "AP \u00b7 NPR", "REPORTED", "nato", 4.4, 50.8),
    (7, "JABALIA, GAZA", "MEA", "CONFLICT",
     "Israeli strike kills a UNRWA worker in Gaza",
     "Adel Al-Helo was hit near the water well he ran; at least 3 killed in Gaza strikes.",
     "UNRWA \u00b7 Reuters", "REPORTED", "well", 34.5, 31.5),
    (8, "NEW DELHI", "ASI", "AID",
     "India pledges $1.62bn to flood-hit Nepal",
     "$377m in grants plus $1.24bn energy credit, unveiled on PM Balendra Shah's visit.",
     "Reuters", "OFFICIAL", "himalaya", 77.2, 28.6),
    (9, "JAKARTA", "ASI", "POLITICS",
     "Prabowo names two vice-president picks",
     "Sugiono and Andi Amran Sulaiman go to the MPR, which votes on 11 December.",
     "Reuters", "OFFICIAL", "dome", 106.8, -6.2),
    (10, "C\u00daCUTA, COLOMBIA", "LAT", "SECURITY",
     "Drone bombs hit a police base in C\u00facuta",
     "3 civilians hurt, among them a baby; 60+ homes damaged in a first big urban drone attack.",
     "AP \u00b7 Colombia Reports", "CONFIRMED", "drone", -72.5, 7.9),
    (11, "BRIDGETOWN, BARBADOS", "LAT", "TECH",
     "Guterres urges global AI risk rules within a year",
     "Speaks at a special AI safety summit hosted by Prime Minister Mia Mottley.",
     "UN News", "OFFICIAL", "podium", -59.6, 13.1),
]

# One-line stories: (no, region, headline, where/source, label, lon, lat)
BRIEFS = [
    (12, "ASI", "Kang Kum-sil named first woman to lead S. Korea's spy agency", "Seoul \u00b7 Yonhap", "OFFICIAL", 127.0, 37.5),
    (13, "ASI", "Cikande factory-fire toll confirmed at 24; ~30 missing", "Banten, Indonesia \u00b7 Reuters", "ONGOING", 106.3, -6.2),
    (14, "ASI", "UN publishes Tajikistan's notice to quit the ICC", "Dushanbe \u00b7 UN", "OFFICIAL", 68.8, 38.6),
    (15, "ASI", "Tata Steel \u22129%, APL Apollo \u221219% after $1.67bn stake deal", "Mumbai \u00b7 BusinessLine", "REPORTED", 72.9, 19.1),
    (16, "ASI", "Bali downpours: 20 floods and landslides, 2 missing", "Bali \u00b7 BPBD", "ONGOING", 115.2, -8.4),
    (17, "OCE", "Australia's Chalmers warns 4.9% jobless rate will top 5%", "Canberra \u00b7 Treasurer", "OFFICIAL", 149.1, -35.3),
    (18, "OCE", "M6.5 deep quake near Vanuatu; no tsunami threat", "Vanuatu \u00b7 USGS", "CONFIRMED", 168.3, -17.7),
    (19, "MEA", "IRGC says three tankers hit mines and caught fire in Hormuz", "Strait of Hormuz \u00b7 Fars", "CLAIM", 56.3, 26.4),
    (20, "MEA", "Iran's army says it downed a US LUCAS drone over the Gulf", "Persian Gulf \u00b7 Fars", "CLAIM", 54.5, 26.0),
    (21, "MEA", "Houthis say Saudi strikes killed 17 telecom workers", "Hodeidah, Yemen \u00b7 AFP", "CLAIM", 42.9, 14.8),
    (22, "MEA", "US weighs training Syrian troops to clear mines", "Damascus \u00b7 Reuters", "REPORTED", 36.3, 33.5),
    (23, "NAM", "US sanctions 24+ firms in Iran's shadow-banking web", "Washington \u00b7 US Treasury", "OFFICIAL", -77.0, 38.9),
    (24, "AFR", "Germany's Steinmeier starts 4-day Africa trip in Abidjan", "C\u00f4te d'Ivoire \u00b7 wires", "REPORTED", -4.0, 5.3),
    (25, "AFR", "Guinea's regulator bans Burkina Faso broadcaster RTB", "Conakry \u00b7 HAC", "REPORTED", -13.7, 9.6),
    (26, "AFR", "WHO confirms 87 attacks on health care in DR Congo", "Ituri, DRC \u00b7 UN News", "ONGOING", 29.0, 1.6),
    (27, "AFR", "African health chiefs meet on cutting aid dependence", "Addis Ababa \u00b7 AllAfrica", "REPORTED", 38.7, 9.0),
    (28, "EUR", "Pas-de-Calais floods: ~850 homes hit, ~800 evacuated", "France \u00b7 Interior Ministry", "ONGOING", 2.3, 50.5),
    (29, "EUR", "STOXX 600 +1.9%, its best day in six months, chips lead", "Frankfurt \u00b7 Reuters", "REPORTED", 8.7, 50.1),
    (30, "EUR", "Premier League: Brentford 4\u20130 Everton, Monday night", "London \u00b7 match reports", "REPORTED", -0.3, 51.5),
    (31, "NAM", "Florida: St Johns River sets record crest, hundreds of homes flood", "Geneva, FL \u00b7 NWS", "ONGOING", -81.0, 28.6),
    (32, "NAM", "Toronto's TSX +2.69% to 34,081 in the AI rebound", "Toronto \u00b7 market data", "REPORTED", -79.4, 43.7),
    (33, "NAM", "NFL Monday night: Broncos 38\u201324 Raiders", "Denver \u00b7 NFL", "REPORTED", -105.0, 39.7),
    (34, "SCI", "Webb: Cas A star's layers merged hours before it blew", "ApJ Letters \u00b7 NASA", "REPORTED", None, None),
]

NUMBERS = [
    ("+31.48%", "Nvidia's one-day jump, its best since 2003"),
    ("$952bn", "market value Nvidia added in a day"),
    ("\u22123.31%", "Kospi close; program trades paused"),
    ("60 banks", "Russian lenders the EU wants off SWIFT"),
    ("$1.62bn", "India's package for flood-hit Nepal"),
]

LEFT_OUT = [
    ("COP31 ends without a deal", "Sun 22 Nov"),
    ("Dymer strike", "Sun 22 Nov"),
    ("Russian missiles land in Poland", "Fri 20 Nov"),
    ("Benghazi strike itself (Kyiv's claim came Mon)", "Sun 22 Nov"),
    ("Cikande fire breaks out", "Sat 21 Nov"),
    ("Huang quits Nvidia", "Thu 12 Nov"),
]
