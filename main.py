import discord
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

STOCK_ROLE_NAME = "Stock Ping"
STOCK_CHANNEL_ID = 1545233041293578421


class HelpPaginator(discord.ui.View):
    def __init__(self, pages, author_id):
        super().__init__(timeout=180)
        self.pages = pages
        self.current = 0
        self.author_id = author_id
        self.update_buttons()

    def update_buttons(self):
        self.prev_button.disabled = self.current == 0
        self.next_button.disabled = self.current >= len(self.pages) - 1
        self.page_label.label = "Page " + str(self.current + 1) + "/" + str(len(self.pages))

    async def interaction_check(self, interaction):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("Only the person who ran the command can use these buttons.", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.secondary)
    async def prev_button(self, interaction, button):
        self.current -= 1
        self.update_buttons()
        await interaction.response.edit_message(content=self.pages[self.current], view=self)

    @discord.ui.button(label="Page 1/1", style=discord.ButtonStyle.primary, disabled=True)
    async def page_label(self, interaction, button):
        pass

    @discord.ui.button(label="Next", style=discord.ButtonStyle.secondary)
    async def next_button(self, interaction, button):
        self.current += 1
        self.update_buttons()
        await interaction.response.edit_message(content=self.pages[self.current], view=self)


ALL_ITEMS = [
    "Aquarium (L)", "Autumn Tree (R)", "Bamboo I (U)", "Bamboo II (U)",
    "Bamboo Fence", "Bench (U)", "Black Drawer (R)", "Black Frame Bed (R)",
    "Black Nightstand (U)", "Black Table Chair (U)", "Brown Drawer (R)",
    "Brown Frame Bed (R)", "Brown Nightstand (U)", "Campfire (D)",
    "Ceiling Light (E)", "Cherry Tree (E)", "Cherry Blossoms (R)",
    "Dirt Tile Path", "Fabric Sack Stack (U)", "Fairy Statue (D)",
    "Fireflies (E)", "Fire Flowers (E)", "Flower Swing (L)", "Flower Wagon (L)",
    "Fern", "Garden Arch (L)", "Garden Lantern (U)", "Glass Table (R)",
    "Glowing Mushroom Lantern Staff (L)", "Gray Drawer (R)", "Gray Sofa (R)",
    "Green Bush", "Hanging Sakura (E)", "Japanese Torii Gate (L)",
    "Japanese Toro Stone Lantern (R)", "Japanese Tree (E)",
    "Japanese Wooden Lantern (E)", "Kitchen 1 (L)", "Kitchen 2 (L)",
    "Lamp (R)", "Large Decorated Flower Pot", "Large Sofa Gray (E)",
    "Large Sofa White (E)", "Large Wooden Chair (U)", "Light String (R)",
    "Log", "Moss Flowers (U)", "Mushroom (U)", "Old Style Lamp (R)",
    "Peach Flowers (R)", "Pebble Tile Path", "Piano 1 (E)", "Piano 2 (E)",
    "Pink Flower (U)", "Quantum Flowers (M)", "Red Japanese Tree (L)",
    "Rope Fence", "Round Glass Table (R)", "Round Wood Table (R)",
    "Simple Wooden Chair", "Shoji Screen (R)",
    "Short Cobblestone Florin Display Pot (M)", "Short Florin Display Pot",
    "Short Limestone Florin Display Pot (L)",
    "Short Pavement Florin Display Pot (M)",
    "Short Shrine Florin Display Pot (D)", "Shower 1 (E)", "Shower 2 (E)",
    "Shrub", "Sink 1 (R)", "Sink 2 (R)", "Small Autumn Tree (U)",
    "Small Black Frame Bed (R)", "Small Brown Frame Bed (R)",
    "Small Gray Drawer (U)", "Small Green Tree (U)", "Small Sofa Gray (R)",
    "Small Sofa White (R)", "Small White Drawer (U)", "Small White Bed Frame (R)",
    "Stone Seat (U)", "Stool", "Stylized Rock I", "Stylized Rock II",
    "Stylized Rock III (U)", "Stylized Rock IV (U)",
    "Stylized Water Fountain (L)", "Stylized Well (Clean Blue) (E)",
    "Stylized Well (Decaying Red) (E)", "Stylized Well (Mossy Green) (E)",
    "Table Lamp (U)", "Tall Cobblestone Florin Display Pot (M)",
    "Tall Florin Display Pot", "Tall Limestone Florin Display Pot (L)",
    "Tall Pavement Florin Display Pot (M)", "Tall Shrine Florin Display Pot (D)",
    "Teapots (U)", "Tent (R)", "Toilet 1 (R)", "Toilet 2 (R)",
    "Traditional Japanese Lantern (R)", "Tree (R)", "Tree House (D)",
    "Tree Stump", "Vintage Piano (D)", "White Cobble Path", "White Drawer (R)",
    "White Frame Bed (R)", "White Sofa (R)", "Windchime (U)",
    "Wisteria Tree (D)", "Wooden Fence", "Wooden Log Stump",
    "Wood Table (R)", "Wood Table Chair (U)", "Uh Table (R)"
]

ITEM_MAP = {
    "a": "Aquarium (L)", "at": "Autumn Tree (R)", "b1": "Bamboo I (U)",
    "b2": "Bamboo II (U)", "bf": "Bamboo Fence", "be": "Bench (U)",
    "bd": "Black Drawer (R)", "blfb": "Black Frame Bed (R)",
    "bln": "Black Nightstand (U)", "btc": "Black Table Chair (U)",
    "br": "Brown Drawer (R)", "brfb": "Brown Frame Bed (R)",
    "brn": "Brown Nightstand (U)", "c": "Campfire (D)",
    "cl": "Ceiling Light (E)", "ct": "Cherry Tree (E)",
    "cb": "Cherry Blossoms (R)", "dtp": "Dirt Tile Path",
    "fss": "Fabric Sack Stack (U)", "fst": "Fairy Statue (D)",
    "fi": "Fireflies (E)", "ff": "Fire Flowers (E)",
    "fsw": "Flower Swing (L)", "fw": "Flower Wagon (L)", "fe": "Fern",
    "ga": "Garden Arch (L)", "gl": "Garden Lantern (U)",
    "gt": "Glass Table (R)", "gmls": "Glowing Mushroom Lantern Staff (L)",
    "gd": "Gray Drawer (R)", "gs": "Gray Sofa (R)", "gb": "Green Bush",
    "hs": "Hanging Sakura (E)", "jtg": "Japanese Torii Gate (L)",
    "jtsl": "Japanese Toro Stone Lantern (R)", "jt": "Japanese Tree (E)",
    "jwl": "Japanese Wooden Lantern (E)", "k1": "Kitchen 1 (L)",
    "k2": "Kitchen 2 (L)", "l": "Lamp (R)",
    "ldfp": "Large Decorated Flower Pot", "lsg": "Large Sofa Gray (E)",
    "lsw": "Large Sofa White (E)", "lwc": "Large Wooden Chair (U)",
    "ls": "Light String (R)", "lo": "Log", "mf": "Moss Flowers (U)",
    "mu": "Mushroom (U)", "osl": "Old Style Lamp (R)",
    "pef": "Peach Flowers (R)", "ptp": "Pebble Tile Path",
    "p1": "Piano 1 (E)", "p2": "Piano 2 (E)", "pif": "Pink Flower (U)",
    "qf": "Quantum Flowers (M)", "rjt": "Red Japanese Tree (L)",
    "rf": "Rope Fence", "rgt": "Round Glass Table (R)",
    "rwt": "Round Wood Table (R)", "swc": "Simple Wooden Chair",
    "shs": "Shoji Screen (R)",
    "scfdp": "Short Cobblestone Florin Display Pot (M)",
    "sdp": "Short Florin Display Pot",
    "slfdp": "Short Limestone Florin Display Pot (L)",
    "spfdp": "Short Pavement Florin Display Pot (M)",
    "ssfdp": "Short Shrine Florin Display Pot (D)",
    "sh1": "Shower 1 (E)", "sh2": "Shower 2 (E)", "sh": "Shrub",
    "si1": "Sink 1 (R)", "si2": "Sink 2 (R)",
    "sat": "Small Autumn Tree (U)", "sblfb": "Small Black Frame Bed (R)",
    "sbrfb": "Small Brown Frame Bed (R)", "sgd": "Small Gray Drawer (U)",
    "sgt": "Small Green Tree (U)", "ssg": "Small Sofa Gray (R)",
    "ssw": "Small Sofa White (R)", "swd": "Small White Drawer (U)",
    "swbf": "Small White Bed Frame (R)", "sts": "Stone Seat (U)",
    "s": "Stool", "sr1": "Stylized Rock I", "sr2": "Stylized Rock II",
    "sr3": "Stylized Rock III (U)", "sr4": "Stylized Rock IV (U)",
    "swf": "Stylized Water Fountain (L)",
    "swcb": "Stylized Well (Clean Blue) (E)",
    "swdr": "Stylized Well (Decaying Red) (E)",
    "swmg": "Stylized Well (Mossy Green) (E)", "tl": "Table Lamp (U)",
    "tcfdp": "Tall Cobblestone Florin Display Pot (M)",
    "tfdp": "Tall Florin Display Pot",
    "tlfdp": "Tall Limestone Florin Display Pot (L)",
    "tpfdp": "Tall Pavement Florin Display Pot (M)",
    "tsfdp": "Tall Shrine Florin Display Pot (D)", "tea": "Teapots (U)",
    "te": "Tent (R)", "t1": "Toilet 1 (R)", "t2": "Toilet 2 (R)",
    "tjl": "Traditional Japanese Lantern (R)", "tr": "Tree (R)",
    "th": "Tree House (D)", "ts": "Tree Stump", "vp": "Vintage Piano (D)",
    "wcp": "White Cobble Path", "wd": "White Drawer (R)",
    "wfb": "White Frame Bed (R)", "ws": "White Sofa (R)",
    "wc": "Windchime (U)", "wtr": "Wisteria Tree (D)",
    "wf": "Wooden Fence", "wls": "Wooden Log Stump",
    "wta": "Wood Table (R)", "wtc": "Wood Table Chair (U)",
    "ut": "Uh Table (R)"
}


@client.event
async def on_ready():
    print("Bot is online as " + str(client.user))


@client.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.strip()
    content_lower = content.lower()

    if not content_lower.startswith("!s "):
        return

    # HELP COMMAND (replies in the same channel)
    if content_lower.startswith("!s help"):
        prefix = "!s"

        shortcut_lines = []
        for shortcut, full_name in sorted(ITEM_MAP.items()):
            shortcut_lines.append("`" + prefix + " " + shortcut + "` = " + full_name)

        per_page = 15
        chunks = []
        for i in range(0, len(shortcut_lines), per_page):
            chunks.append(shortcut_lines[i:i + per_page])

        total = len(chunks)
        pages = []
        for idx, chunk in enumerate(chunks):
            header = "**STOCK SHORTCUTS**\n*Page " + str(idx + 1) + " of " + str(total) + "*\n\n"
            pages.append(header + "\n".join(chunk))

        if pages:
            pages[-1] = pages[-1] + "\n\n__**Examples:**__\n`!s b1` = " + ITEM_MAP["b1"] + "\n`!s b1, b2, t1` = multiple items"

        view = HelpPaginator(pages, message.author.id)
        await message.channel.send(pages[0], view=view)
        return

    # STOCK PING
    raw = content[3:].strip()

    if not raw:
        await message.channel.send("Type shortcuts after `!s`. Example: `!s b1 b2`")
        return

    codes = [x.strip().lower() for x in raw.replace(",", " ").split() if x.strip()]

    items = []
    unknown = []

    for code in codes:
        if code in ITEM_MAP:
            items.append(ITEM_MAP[code])
        else:
            matches = [item for item in ALL_ITEMS if code in item.lower()]
            if len(matches) == 1:
                items.append(matches[0])
            else:
                unknown.append(code)

    if not items:
        await message.channel.send("No valid items found. Try `!s help`.")
        return

    # Find the stock role
    role_mention = ""
    if message.guild:
        role = discord.utils.get(message.guild.roles, name=STOCK_ROLE_NAME)
        if role:
            role_mention = role.mention + " "
        else:
            role_mention = "@" + STOCK_ROLE_NAME + " (role not found!) "

    formatted = ", ".join(items)
    reply = role_mention + "**" + formatted + "** in stock!"

    if unknown:
        reply = reply + "\n\n_Ignored unknown: " + ", ".join(unknown) + "_"

    # Send ping to stock channel
    target_channel = client.get_channel(STOCK_CHANNEL_ID)

    if target_channel:
        await target_channel.send(reply)

        # If the command was run in a different channel, confirm here
        if target_channel.id != message.channel.id:
            await message.channel.send("✅ Posted in <#" + str(STOCK_CHANNEL_ID) + ">")
    else:
        await message.channel.send("⚠️ Stock channel not found. Check STOCK_CHANNEL_ID.\n\n" + reply)


client.run(os.getenv("DISCORD_TOKEN"))
