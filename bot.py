
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

@bot.event
async def on_ready():
    print(f"✅ A bot elindult: {bot.user}")
    print("🚀 A bot sikeresen csatlakozott!")

@bot.command()
async def ping(ctx):
    await ctx.send(
        f"🏓 Pong! {round(bot.latency * 1000)} ms"
    )

@bot.command()
async def hello(ctx):
    await ctx.send(
        f"Szia, {ctx.author.mention}! 👋"
    )

@bot.command()
async def help(ctx):
    await ctx.send(
        "**🤖 Bot parancsai**\n"
        "`!ping` – Válaszidő\n"
        "`!hello` – Köszönés\n"
        "`!help` – Súgó"
    )
@bot.event
async def on_member_join(member):
    # A rang neve, amit automatikusan megkap (pontosan úgy írd le, ahogy a Discordon elnevezted!)
    role_name = "Játékosok" 
    
    # Megkeresi a rangot a szerveren
    role = discord.utils.get(member.guild.roles, name=role_name)
    
    if role:
        try:
            await member.add_roles(role)
            print(f"Sikeresen megadtam a(z) {role_name} rangot neki: {member.name}")
        except Exception as e:
            print(f"Hiba történt a rang adása közben: {e}")
    else:
        print(f"Nem találom a(z) {role_name} nevű rangot a szerveren!")
@bot.event
async def on_member_join(member):
    # 1. Automatikus rangosztás (amit már beállítottunk)
    role_name = "Játékosok"  # Itt a pontos rangnév a Discordról
    role = discord.utils.get(member.guild.roles, name=role_name)
    
    if role:
        try:
            await member.add_roles(role)
            print(f"Sikeresen megadtam a(z) {role_name} rangot neki: {member.name}")
        except Exception as e:
            print(f"Hiba történt a rang adása közben: {e}")
    else:
        print(f"Nem találom a(z) {role_name} nevű rangot a szerveren!")

    # 2. Üdvözlő üzenet küldése egy adott csatornába
    # Cseréld ki az "udvozles" szót arra a csatornanyomtatványra (névre), ahová írnia kell!
    channel_name = "👋belépő" 
    channel = discord.utils.get(member.guild.text_channels, name=channel_name)
    
    if channel:
        await channel.send(f"Köszönt téged a Blackhawk Military, {member.mention}! Örülünk, hogy csatlakoztál! 🎉")
    else:
        print(f"Nem találom a(z) {channel_name} nevű csatornát az üzenethez!")
import discord
from discord.ext import commands

# Intents beállítása
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bejelentkezve mint: {bot.user.name}")
    
    # A te csatorna ID-d:
    CSATORNA_ID = 1566066775374696448  
    
    target_channel = bot.get_channel(CSATORNA_ID)
    if not target_channel:
        try:
            target_channel = await bot.fetch_channel(CSATORNA_ID)
        except Exception as e:
            print(f"Nem találom a csatornát: {e}")
            return

    # Megnézzük, hogy van-e már kint szabályzat (utolsó 5 üzenet vizsgálata, hogy ne küldje be duplán)
    messages = [message async for message in target_channel.history(limit=5)]
    has_rules = any(msg.author == bot.user and msg.embeds and "SZABÁLYZAT" in msg.embeds[0].title for msg in messages)

    if has_rules:
        print("A frissített szabályzat automatikusan beküldve a csatornába!")
        return

    # Teljes Embed létrehozása az összes szabállyal
    embed = discord.Embed(
        title="🛑 SZABÁLYZAT / RULES",
        description="Üdvözlünk a szerveren!",
        color=discord.Color.red()
    )

    embed.add_field(
        name="1️⃣ Alapvető viselkedés és tisztelet",
        value="• **Légy tisztelettudó:** Tiszteld a többi tagot. A zaklatás, a megfélemlítés és a gyűlöletbeszéd szigorúan tilos.\n• **Kultúrált kommunikáció:** Kerüld a túlzott trágárságot, a provokációt és a mások provokálását.",
        inline=False
    )
    
    embed.add_field(
        name="2️⃣ Spam és reklám",
        value="• **Tilos a spam:** Ne küldj feleslegesen ismétlődő üzeneteket vagy felesleges emojikat.\n• **Tiltott a reklám:** Más Discord szerverek, csatornák vagy külső linkek engedélyezetlen hirdetése tilos.",
        inline=False
    )

    embed.add_field(
        name="3️⃣ Tartalomra vonatkozó szabályok",
        value="• **NSFW/18+ tartalom tilos:** Semmilyen formában nem megengedett a korhatáros, erőszakos vagy szexuális jellegű tartalom.\n• **Fájlok és linkek:** Olyan külső linkeket ne ossz meg, amelyek vírusosak vagy adathalász oldalakra vezetnek.",
        inline=False
    )

    embed.add_field(
        name="4️⃣ Moderáció és következmények",
        value="• **A stáb döntése:** A moderátorok és az adminisztrátorok utasításait kötelező betartani.\n• **⚠️ A szabályok nem ismerete nem mentesít a büntetés alól!** (Figyelmeztetés, némítás, kick vagy ban járhat a szegésért).",
        inline=False
    )

    embed.set_footer(text="Köszönjük, hogy betartod a szabályokat, és jó szórakozást kívánunk!")

    # Beküldés a megadott csatornába
    await target_channel.send(embed=embed)
    print("A szabályzat automatikusan beküldve a csatornába!")
import discord
from discord.ext import commands
from discord.ui import Button, View
import asyncio

# 1. Intentek beállítása (fontos a message_content is!)
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 2. A pontos rangok listája, akik láthatják és kezelhetik a ticketet
ALLOWED_ROLE_NAMES = [
    "Helper",
    "[1] Admin",
    "[2] Admin",
    "[3] Admin",
    "[4] Admin",
    "🔰 Admin",
    "💎 Super Admin",
    "🛡 Admin Controller",
    "Server Manager"
]

# Gomb a ticket bezárásához
class CloseTicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Ticket Bezárása", style=discord.ButtonStyle.red, custom_id="close_ticket")
    async def close_button(self, interaction: discord.Interaction, button: Button):
        user_roles = [role.name for role in interaction.user.roles]
        has_staff_role = any(role_name in ALLOWED_ROLE_NAMES for role_name in user_roles)
        is_admin = interaction.user.guild_permissions.administrator
        is_author = interaction.channel.name in interaction.user.name.lower()

        if has_staff_role or is_admin or is_author:
            await interaction.response.send_message("A ticket 5 másodperc múlva törlődik...")
            await asyncio.sleep(5)
            await interaction.channel.delete()
        else:
            await interaction.response.send_message("Ehhez nincsen jogosultságod!", ephemeral=True)

# Gomb a ticket nyitásához
class CreateTicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="📩 Ticket Nyitása", style=discord.ButtonStyle.green, custom_id="create_ticket")
    async def create_button(self, interaction: discord.Interaction, button: Button):
        guild = interaction.guild
        user = interaction.user

        channel_name = f"ticket-{user.name}".lower()
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if existing_channel:
            await interaction.response.send_message(f"Már van nyitott ticketed: {existing_channel.mention}", ephemeral=True)
            return

        # Alap jogosultságok: Senki sem látja, csak a user és a bot
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        # Hozzáadjuk a listában szereplő rangokat, hogy lássák a szobát
        for role in guild.roles:
            if role.name in ALLOWED_ROLE_NAMES:
                overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        ticket_channel = await guild.create_text_channel(name=channel_name, overwrites=overwrites)
        
        await interaction.response.send_message(f"Ticket sikeresen megnyitva: {ticket_channel.mention}", ephemeral=True)

        embed = discord.Embed(
            title=f"Üdvözlünk, {user.name}!",
            description="Kérlek írd le a problémádat, és egy staff tag hamarosan válaszol.\nHa végeztetek, kattints a lenti gombra.",
            color=discord.Color.blue()
        )
        await ticket_channel.send(embed=embed, view=CloseTicketView())

@bot.event
async def on_ready():
    print(f'Bejelentkezve mint {bot.user} (ID: {bot.user.id})')
    print('A bot készen áll a ticketek kezelésére!')

# Parancs a nyitó felület elküldéséhez
@bot.command()
@commands.has_permissions(administrator=True)
async def setup_ticket(ctx):
    await ctx.message.delete()
    embed = discord.Embed(
        title="Készíts Ticketet!",
        description="Ha segítségre van szükséged, kattints az alábbi gombra egy privát beszélgetés nyitásához.",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed, view=CreateTicketView())
class CreateTicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="📩 Ticket Nyitása", style=discord.ButtonStyle.green, custom_id="create_ticket")
    async def create_button(self, interaction: discord.Interaction, button: Button):
        # 1. Azonnal jelezzük a Discordnak, hogy megkaptuk a gombnyomást (ez megakadályozza az "időben nem reagált" hibát)
        await interaction.response.defer(ephemeral=True)

        guild = interaction.guild
        user = interaction.user

        channel_name = f"ticket-{user.name}".lower()
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if existing_channel:
            await interaction.followup.send(f"Már van nyitott ticketed: {existing_channel.mention}", ephemeral=True)
            return

        # Alap jogosultságok: Senki sem látja, csak a user és a bot
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        # Hozzáadjuk a listában szereplő rangokat, hogy lássák a szobát
        for role in guild.roles:
            if role.name in ALLOWED_ROLE_NAMES:
                overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        # Új csatorna létrehozása
        ticket_channel = await guild.create_text_channel(name=channel_name, overwrites=overwrites)
        
        # Üzenet küldése a felhasználónak, hogy elkészült
        await interaction.followup.send(f"Ticket sikeresen megnyitva: {ticket_channel.mention}", ephemeral=True)

        embed = discord.Embed(
            title=f"Üdvözlünk, {user.name}!",
            description="Kérlek írd le a problémádat, és egy staff tag hamarosan válaszol.\nHa végeztetek, kattints a lenti gombra.",
            color=discord.Color.blue()
        )
        await ticket_channel.send(embed=embed, view=CloseTicketView())
bot.run("DISCORD_TOKEN")
