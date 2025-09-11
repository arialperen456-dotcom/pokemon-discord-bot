
import random
import discord
from discord.ext import commands
import asyncio
from config import token # config.py dosyanızda token değişkeni olmalı
from logic import Pokemon

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'Giriş yapıldı:  {bot.user.name}')

class Wizard(Pokemon):
    pass
class Fighter(Pokemon):
    pass
@bot.command()
async def go(ctx):
    author = ctx.author.name
    if author not in Pokemon.pokemons:
        chance = random.randint(1, 3)
        if chance == 1:
            pokemon = Pokemon(author)
        elif chance == 2:
            pokemon = Wizard(author)
        else:
            pokemon = Fighter(author)
        pokemon = Pokemon(author)
        await pokemon.get_data() # Verileri çekmek için get_data'yı çağır
        await ctx.send(await pokemon.info())
        image_url = await pokemon.show_img()
        if image_url:
            embed = discord.Embed(title=f"{pokemon.name.capitalize()} görünüyor!")
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Pokémonun görüntüsü yüklenemedi!")
    else:
        # Kullanıcı zaten pokemon oluşturmuş, seçenek sun
        msg = await ctx.send(
            f"{ctx.author.mention}, zaten bir Pokémonun var! Yeni bir tane oluşturmak için eski Pokémonunu silmek ister misin?\n"
            "✅ - Evet, eski Pokémonu sil ve yenisini oluştur\n"
            "❌ - Hayır, eski Pokémonu tut"
        )
        # Reaksiyonları ekle
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == msg.id

        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send(f"{ctx.author.mention}, zaman aşımına uğradı. İşlem iptal edildi.")
            return

        if str(reaction.emoji) == "✅":
            # Eski pokemonu sil ve yenisini oluştur
            del Pokemon.pokemons[author]
            pokemon = Pokemon(author)
            await pokemon.get_data() # Yeni pokemonun verilerini çek
            await ctx.send("Eski Pokémon silindi, yeni Pokémon oluşturuldu!")
            await ctx.send(await pokemon.info())
            image_url = await pokemon.show_img()
            if image_url:
                embed = discord.Embed(title=f"{pokemon.name.capitalize()} görünüyor!")
                embed.set_image(url=image_url)
                await ctx.send(embed=embed)
            else:
                await ctx.send("Pokémonun görüntüsü yüklenemedi!")
        else:
            # Hayır seçildi
            await ctx.send("Eski Pokémonun korunuyor, yeni Pokémon oluşturulmadı.")

@bot.command()
async def attack(ctx):
    target = ctx.message.mentions[0] if ctx.message.mentions else None
    if target:
        if target.name in Pokemon.pokemons and ctx.author.name in Pokemon.pokemons:
            enemy = Pokemon.pokemons[target.name]
            attacker = Pokemon.pokemons[ctx.author.name]
            result = await attacker.attack(enemy)
            await ctx.send(result)
        else:
            await ctx.send("Savaşmak için her iki katılımcının da Pokemon sahibi olması gerekir!")
    else:
        await ctx.send("Saldırmak istediğiniz kullanıcıyı etiketleyerek belirtin.")

@bot.command()
async def info(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        if not pokemon.name: # Eğer isim çekilmemişse, get_data'yı çağır
            await pokemon.get_data()

        types_str = ", ".join(pokemon.types).capitalize() if pokemon.types else "Bilinmiyor"
        abilities_str = ", ".join(pokemon.abilities).capitalize() if pokemon.abilities else "Bilinmiyor"

        stats = pokemon.stats
        stats_str = (
            f"Özel Saldırı: {stats.get('special-attack', 'Bilinmiyor')}, "
            f"Özel Defans: {stats.get('special-defense', 'Bilinmiyor')}, "
            f"Hız: {stats.get('speed', 'Bilinmiyor')}"
        )

        info_message = (
            f"**Pokémon ismi:** {pokemon.name.capitalize()}\n"
            f"**Pokémon türü:** {types_str}\n"
            f"**Yetenekleri:** {abilities_str}\n"
            f"**Pokémon istatistikleri:** {stats_str}\n"
            f"**Seviyesi:** {pokemon.level}\n"
            f"**Hasar:** {pokemon.damage}\n"
            f"**Can:** {pokemon.health}"
        )
        await ctx.send(info_message)
    else:
        await ctx.send("Öncelikle bir Pokémon oluşturmalısınız! (!go komutunu kullanın)")

@bot.command(name="yardim")
async def yardim(ctx):
    help_message = (
        "**Pokémon Bot Komutları:**\n"
        "`!go` - Yeni bir Pokémon oluşturur ve bilgilerini gösterir.\n"
        "`!feed` - Pokémonunuzu besler, deneyim kazandırır ve seviyesini artırır.\n"
        "`!yardim` - Bu yardım mesajını gösterir.\n"
        "`!info` - Pokemonunuz hakkında bilgi verir.\n\n"
        "İyi oyunlar! 🎮"
    )
    await ctx.send(help_message)

@bot.command()
async def feed(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        pokemon.add_experience(5)
        bonus_msg = " (Nadir Pokémon bonusu ile 2 kat deneyim kazandınız!)" if getattr(pokemon, "is_rare", False) else ""
        await ctx.send(f"{pokemon.name.capitalize()} beslenildi! Şu anki seviyesi: {pokemon.level}{bonus_msg}")
    else:
        await ctx.send("Önce bir Pokémon oluşturmalısınız! (!go komutunu kullanın)")

import random
import discord
from discord.ext import commands
import asyncio
from config import token # config.py dosyanızda token değişkeni olmalı
from logic import Pokemon

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'Giriş yapıldı:  {bot.user.name}')

class Wizard(Pokemon):
    pass
class Fighter(Pokemon):
    pass
@bot.command()
async def go(ctx):
    author = ctx.author.name
    if author not in Pokemon.pokemons:
        chance = random.randint(1, 3)
        if chance == 1:
            pokemon = Pokemon(author)
        elif chance == 2:
            pokemon = Wizard(author)
        else:
            pokemon = Fighter(author)
        pokemon = Pokemon(author)
        await pokemon.get_data() # Verileri çekmek için get_data'yı çağır
        await ctx.send(await pokemon.info())
        image_url = await pokemon.show_img()
        if image_url:
            embed = discord.Embed(title=f"{pokemon.name.capitalize()} görünüyor!")
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Pokémonun görüntüsü yüklenemedi!")
    else:
        # Kullanıcı zaten pokemon oluşturmuş, seçenek sun
        msg = await ctx.send(
            f"{ctx.author.mention}, zaten bir Pokémonun var! Yeni bir tane oluşturmak için eski Pokémonunu silmek ister misin?\n"
            "✅ - Evet, eski Pokémonu sil ve yenisini oluştur\n"
            "❌ - Hayır, eski Pokémonu tut"
        )
        # Reaksiyonları ekle
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == msg.id

        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send(f"{ctx.author.mention}, zaman aşımına uğradı. İşlem iptal edildi.")
            return

        if str(reaction.emoji) == "✅":
            # Eski pokemonu sil ve yenisini oluştur
            del Pokemon.pokemons[author]
            pokemon = Pokemon(author)
            await pokemon.get_data() # Yeni pokemonun verilerini çek
            await ctx.send("Eski Pokémon silindi, yeni Pokémon oluşturuldu!")
            await ctx.send(await pokemon.info())
            image_url = await pokemon.show_img()
            if image_url:
                embed = discord.Embed(title=f"{pokemon.name.capitalize()} görünüyor!")
                embed.set_image(url=image_url)
                await ctx.send(embed=embed)
            else:
                await ctx.send("Pokémonun görüntüsü yüklenemedi!")
        else:
            # Hayır seçildi
            await ctx.send("Eski Pokémonun korunuyor, yeni Pokémon oluşturulmadı.")

@bot.command()
async def attack(ctx):
    target = ctx.message.mentions[0] if ctx.message.mentions else None
    if target:
        if target.name in Pokemon.pokemons and ctx.author.name in Pokemon.pokemons:
            enemy = Pokemon.pokemons[target.name]
            attacker = Pokemon.pokemons[ctx.author.name]
            result = await attacker.attack(enemy)
            await ctx.send(result)
        else:
            await ctx.send("Savaşmak için her iki katılımcının da Pokemon sahibi olması gerekir!")
    else:
        await ctx.send("Saldırmak istediğiniz kullanıcıyı etiketleyerek belirtin.")

@bot.command()
async def info(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        if not pokemon.name: # Eğer isim çekilmemişse, get_data'yı çağır
            await pokemon.get_data()

        types_str = ", ".join(pokemon.types).capitalize() if pokemon.types else "Bilinmiyor"
        abilities_str = ", ".join(pokemon.abilities).capitalize() if pokemon.abilities else "Bilinmiyor"

        stats = pokemon.stats
        stats_str = (
            f"Özel Saldırı: {stats.get('special-attack', 'Bilinmiyor')}, "
            f"Özel Defans: {stats.get('special-defense', 'Bilinmiyor')}, "
            f"Hız: {stats.get('speed', 'Bilinmiyor')}"
        )

        info_message = (
            f"**Pokémon ismi:** {pokemon.name.capitalize()}\n"
            f"**Pokémon türü:** {types_str}\n"
            f"**Yetenekleri:** {abilities_str}\n"
            f"**Pokémon istatistikleri:** {stats_str}\n"
            f"**Seviyesi:** {pokemon.level}\n"
            f"**Hasar:** {pokemon.damage}\n"
            f"**Can:** {pokemon.health}"
        )
        await ctx.send(info_message)
    else:
        await ctx.send("Öncelikle bir Pokémon oluşturmalısınız! (!go komutunu kullanın)")

@bot.command(name="yardim")
async def yardim(ctx):
    help_message = (
        "**Pokémon Bot Komutları:**\n"
        "`!go` - Yeni bir Pokémon oluşturur ve bilgilerini gösterir.\n"
        "`!feed` - Pokémonunuzu besler, deneyim kazandırır ve seviyesini artırır.\n"
        "`!yardim` - Bu yardım mesajını gösterir.\n"
        "`!info` - Pokemonunuz hakkında bilgi verir.\n\n"
        "İyi oyunlar! 🎮"
    )
    await ctx.send(help_message)

@bot.command()
async def feed(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        pokemon.add_experience(5)
        bonus_msg = " (Nadir Pokémon bonusu ile 2 kat deneyim kazandınız!)" if getattr(pokemon, "is_rare", False) else ""
        await ctx.send(f"{pokemon.name.capitalize()} beslenildi! Şu anki seviyesi: {pokemon.level}{bonus_msg}")
    else:
        await ctx.send("Önce bir Pokémon oluşturmalısınız! (!go komutunu kullanın)")

bot.run(token)