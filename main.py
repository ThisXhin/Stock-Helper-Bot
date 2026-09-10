import discord
import os
import difflib

# ---------- ENABLE READING MESSAGES ----------
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# ---------- YOUR FULL FURNITURE LIST ----------
ALL_ITEMS = [
    "Aquarium (L)",
    "Autumn Tree (R)",
    "Bamboo I (U)",
    "Bamboo II (U)",
    "Bamboo Fence",
    "Bench (U)",
    "Black Drawer (R)",
    "Black Frame Bed (R)",
    "Black Nightstand (U)",
    "Black Table Chair (U)",
    "Brown Drawer (R)",
    "Brown Frame Bed (R)",
    "Brown Nightstand (U)",
    "Campfire (D)",
    "Ceiling Light (E)",
    "Cherry Tree (E)",
    "Cherry Blossoms (R)",
    "Dirt Tile Path",
    "Fabric Sack Stack (U)",
    "Fairy Statue (D)",
    "Fireflies (E)",
    "Fire Flowers (E)",
    "Flower Swing (L)",
    "Flower Wagon (L)",
    "Fern",
    "Garden Arch (L)",
    "Garden Lantern (U)",
    "Glass Table (R)",
    "Glowing Mushroom Lantern Staff (L)",
    "Gray Drawer (R)",
    "Gray Sofa (R)",
    "Green Bush",
    "Hanging Sakura (E)",
    "Japanese Torii Gate (L)",
    "Japanese Toro Stone Lantern (R)",
    "Japanese Tree (E)",
    "Japanese Wooden Lantern (E)",
    "Kitchen 1 (L)",
    "Kitchen 2 (L)",
    "Lamp (R)",
    "Large Decorated Flower Pot",
    "Large Sofa Gray (E)",
    "Large Sofa White (E)",
    "Large Wooden Chair (U)",
    "Light String (R)",
    "Log",
    "Moss Flowers (U)",
    "Mushroom (U)",
    "Old Style Lamp (R)",
    "Peach Flowers (R)",
    "Pebble Tile Path",
    "Piano 1 (E)",
    "Piano 2 (E)",
    "Pink Flower (U)",
    "Quantum Flowers (M)",
    "Red Japanese Tree (L)",
    "Rope Fence",
    "Round Glass Table (R)",
    "Round Wood Table (R)",
    "Simple Wooden Chair",
    "Shoji Screen (R)",
    "Short Cobblestone Florin Display Pot (M)",
    "Short Florin Display Pot",
    "Short Limestone Florin Display Pot (L)",
    "Short Pavement Florin Display Pot (M)",
    "Short Shrine Florin Display Pot (D)",
    "Shower 1 (E)",
    "Shower 2 (E)",
    "Shrub",
    "Sink 1 (R)",
    "Sink 2 (R)",
    "Small Autumn Tree (U)",
    "Small Black Frame Bed (R)",
    "Small Brown Frame Bed (R)",
    "Small Gray Drawer (U)",
    "Small Green Tree (U)",
    "Small Sofa Gray (R)",
    "Small Sofa White (R)",
    "Small White Drawer (U)",
    "Small White Bed Frame (R)",
    "Stone Seat (U)",
    "Stool",
    "Stylized Rock I",
    "Stylized Rock II",
    "Stylized Rock III (U)",
    "Stylized Rock IV (U)",
    "Stylized Water Fountain (L)",
    "Stylized Well (Clean Blue) (E)",
    "Stylized Well (Decaying Red) (E)",
    "Stylized Well (Mossy Green) (E)",
    "Table Lamp (U)",
    "Tall Cobblestone Florin Display Pot (M)",
    "Tall Florin Display Pot",
    "Tall Limestone Florin Display Pot (L)",
    "Tall Pavement Florin Display Pot (M)",
    "Tall Shrine Florin Display Pot (D)",
    "Teapots (U)",
    "Tent (R)",
    "Toilet 1 (R)",
    "Toilet 2 (R)",
    "Traditional Japanese Lantern (R)",
    "Tree (R)",
    "Tree House (D)",
    "Tree Stump",
    "Vintage Piano (D)",
    "White Cobble Path",
    "White Drawer (R)",
    "White Frame Bed (R)",
    "White Sofa (R)",
    "Windchime (U)",
    "Wisteria Tree (D)",
    "Wooden Fence",
    "Wooden Log Stump",
    "Wood Table (R)",
    "Wood Table Chair (U)",
    "Uh Table (R)"
]

# ---------- SHORTCUTS FOR ITEMS ----------
# Add shortcuts here for items!
ITEM_MAP = {
    # Examples – edit these to items:
    "a": "Aquarium (L)",
    "at": "Autumn Tree (R)",
    "b1": "Bamboo I (U)",      # so `!s b1` pings Bamboo I
    "b2": "Bamboo II (U)",
    "bf": "Bamboo Fence",
    "be": "Bench (U)",
    "bd": "Black Drawer (R)",
    "blfb": "Black Frame Bed (R)",
    "bln": "Black Nightstand (U)",
    "btc": "Black Table Chair (U)",
    "br": "Brown Drawer (R)",
    "brfb": "Brown Frame Bed (R)",
    "brn": "Brown Nightstand (U)",
    "c": "Campfire (D)",
    "cl": "Ceiling Light (E)",
    "ct": "Cherry Tree (E)",
    "cb": "Cherry Blossoms (R)",
    "dtp": "Dirt Tile Path",
    "fss": "Fabric Sack Stack (U)",
    "fst": "Fairy Statue (D)",
    "fi": "Fireflies (E)",
    "ff": "Fire Flowers (E)",
    "fsw": "Flower Swing (L)",
    "fw": "Flower Wagon (L)",
    "fe": "Fern",
    "ga": "Garden Arch (L)",
    "gl": "Garden Lantern (U)",
    "gt": "Glass Table (R)",
    "gmls": "Glowing Mushroom Lantern Staff (L)",
    "gd": "Gray Drawer (R)",
    "gs": "Gray Sofa (R)",
    "gb": "Green Bush",
    "hs": "Hanging Sakura (E)",
    "jtg": "Japanese Torii Gate (L)",
    "jtsl": "Japanese Toro Stone Lantern (R)",
    "jt": "Japanese Tree (E)",
    "jwl": "Japanese Wooden Lantern (E)",
    "k1": "Kitchen 1 (L)",
    "k2": "Kitchen 2 (L)",
    "l": "Lamp (R)",
    "ldfp": "Large Decorated Flower Pot",
    "lsg": "Large Sofa Gray (E)",
    "lsw": "Large Sofa White (E)",
    "lwc": "Large Wooden Chair (U)",
    "ls": "Light String (R)",
    "lo": "Log",
    "mf": "Moss Flowers (U)",
    "mu": "Mushroom (U)",
    "osl": "Old Style Lamp (R)",
    "pef": "Peach Flowers (R)",
    "ptp": "Pebble Tile Path",
    "p1": "Piano 1 (E)",
    "p2": "Piano 2 (E)",
    "pif": "Pink Flower (U)",
    "qf": "Quantum Flowers (M)",
    "rjt": "Red Japanese Tree (L)",
    "rf": "Rope Fence",
    "rgt": "Round Glass Table (R)",
    "rwt": "Round Wood Table (R)",
    "swc": "Simple Wooden Chair",
    "shs": "Shoji Screen (R)",
    "scfdp": "Short Cobblestone Florin Display Pot (M)",
    "sdp": "Short Florin Display Pot",
    "slfdp": "Short Limestone Florin Display Pot (L)",
    "spfdp": "Short Pavement Florin Display Pot (M)",
    "ssfdp": "Short Shrine Florin Display Pot (D)",
    "sh1": "Shower 1 (E)",
    "sh2": "Shower 2 (E)",
    "sh": "Shrub",
    "si1": "Sink 1 (R)",
    "si2": "Sink 2 (R)",
    "sat": "Small Autumn Tree (U)",
    "sblfb": "Small Black Frame Bed (R)",
    "sbrfb": "Small Brown Frame Bed (R)",
    "sgd": "Small Gray Drawer (U)",
    "sgt": "Small Green Tree (U)",
    "ssg": "Small Sofa Gray (R)",
    "ssw": "Small Sofa White (R)",
    "swd": "Small White Drawer (U)",
    "swbf": "Small White Bed Frame (R)",
    "sts": "Stone Seat (U)",
    "s": "Stool",
    "sr1": "Stylized Rock I",
    "sr2": "Stylized Rock II",
    "sr3": "Stylized Rock III (U)",
    "sr4": "Stylized Rock IV (U)",
    "swf": "Stylized Water Fountain (L)",
    "swcb": "Stylized Well (Clean Blue) (E)",
    "swdr": "Stylized Well (Decaying Red) (E)",
    "swmg": "Stylized Well (Mossy Green) (E)",
    "tl": "Table Lamp (U)",
    "tcfdp": "Tall Cobblestone Florin Display Pot (M)",
    "tfdp": "Tall Florin Display Pot",
    "tlfdp": "Tall Limestone Florin Display Pot (L)",
    "tpfdp": "Tall Pavement Florin Display Pot (M)",
    "tsfdp": "Tall Shrine Florin Display Pot (D)",
    "tea": "Teapots (U)",
    "te": "Tent (R)",
    "t1": "Toilet 1 (R)",
    "t2": "Toilet 2 (R)",
    "tjl": "Traditional Japanese Lantern (R)",
    "tr": "Tree (R)",          # `!s tr` pings Tree
    "th": "Tree House (D)",
    "ts": "Tree Stump",
    "vp": "Vintage Piano (D)",
    "wcp": "White Cobble Path",
    "wd": "White Drawer (R)",
    "wfb": "White Frame Bed (R)",
    "ws": "White Sofa (R)",
    "wc": "Windchime (U)",
    "wtr": "Wisteria Tree (D)",
    "wf": "Wooden Fence",
    "wls": "Wooden Log Stump",
    "wta": "Wood Table (R)",
    "wtc": "Wood Table Chair (U)",
    "ut": "Uh Table (R)",
    # Add more as needed!
}

# ---------- HELP COMMAND ----------
@client.event
async def on_message(message):
    if message.author.bot:
        return

    # Normalize: strip whitespace, lowercase
    content = message.content.strip()
    content_lower = content.lower()

    # ---- HELP COMMAND (forgiving: ignores trailing punctuation/spaces) ----
    help_check = content_lower.rstrip(".!?,;:")
    if help_check in ("!s help", "?stockping help"):
        prefix = "!s" if help_check.startswith("!s") else "?stockping"
        ping_note = "🔇 No @everyone" if prefix == "!s" else "📢 Pings @everyone"
        
        lines = [f"📦 **Stock Shortcuts** ({ping_note}):"]
        if ITEM_MAP:
            for shortcut, full_name in sorted(ITEM_MAP.items()):
                lines.append(f"`{prefix} {shortcut}` → {full_name}")
        lines.append(f"\n💡 **Or type the item name!**")
        lines.append(f"Example: `{prefix} bamboo`")
        await message.channel.send("\n".join(lines))
        return

    # ---- STOCK COMMAND ----
    if content_lower.startswith("!s "):
        raw = content[3:].strip()
        should_ping = False
    elif content_lower.startswith("?stockping "):
        raw = content[len("?stockping "):].strip()
        should_ping = True
    else:
        return  # Not a command, ignore

    if not raw:
        await message.channel.send("Please type an item! Example: `!s bamboo`")
        return

    # Split by commas OR spaces
    codes = [x.strip().lower() for x in raw.replace(",", " ").split() if x.strip()]

    resolved_items = []
    unknown_terms = []
    ambiguous_terms = {}

    for code in codes:
        if code in ITEM_MAP:
            resolved_items.append(ITEM_MAP[code])
            continue
        matches = [item for item in ALL_ITEMS if code in item.lower()]
        if len(matches) == 1:
            resolved_items.append(matches[0])
        elif len(matches) > 1:
            ambiguous_terms[code] = matches
        else:
            unknown_terms.append(code)

    if ambiguous_terms:
        for term, matches in ambiguous_terms.items():
            match_list = "\n".join([f"{i+1}. {m}" for i, m in enumerate(matches[:10])])
            await message.channel.send(
                f"🔍 Multiple matches for `{term}`:\n{match_list}\n"
                f"Please be more specific."
            )
        return

    if unknown_terms:
        suggestions = []
        for term in unknown_terms:
            close = difflib.get_close_matches(term, ALL_ITEMS, n=3, cutoff=0.6)
            if close:
                suggestions.append(f"`{term}` → Did you mean `{close[0]}`?")
            else:
                suggestions.append(f"`{term}` → No match found.")
        await message.channel.send("❌ Unknown items:\n" + "\n".join(suggestions))
        return

    if resolved_items:
        formatted = ", ".join(resolved_items)
        if should_ping:
            await message.channel.send(f"@everyone **{formatted}** is now in stock!")
        else:
            await message.channel.send(f"**{formatted}** is now in stock!")
            await message.channel.send(reply)
        else:
            await message.channel.send("No valid items found. Try `!s help` or `?stockping help`.")

# ---------- RUN THE BOT ----------
client.run(os.getenv("DISCORD_TOKEN"))