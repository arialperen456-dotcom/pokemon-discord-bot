import aiohttp
import random
import asyncio

def rastgele_sayi(min_val, max_val):
    return random.randint(min_val, max_val)

class Pokemon:
    pokemons = {}  # Trainer → Pokemon instance

    def __new__(cls, pokemon_trainer):
        if pokemon_trainer in cls.pokemons:
            return cls.pokemons[pokemon_trainer]
        instance = super().__new__(cls)
        cls.pokemons[pokemon_trainer] = instance
        return instance

    def __init__(self, pokemon_trainer):
        if not hasattr(self, "initialized"):
            self.pokemon_trainer = pokemon_trainer
            # %5 ihtimalle nadir Pokémon seç
            if random.random() < 0.05:
                self.pokemon_number = random.randint(1, 150)  # Nadir Pokémon aralığı
                self.is_rare = True
            else:
                self.pokemon_number = random.randint(151, 1000)
                self.is_rare = False
            self.name = None
            self.image_url = None
            self.level = random.randint(1, 10)
            self.experience = 0
            self.types = []
            self.abilities = []
            self.stats = {}
            # Yeni eklenen özellikler:
            self.power = random.randint(30, 100)  # Güç (power)
            self.hp = random.randint(100, 400)    # Sağlık (hp)
            self.initialized = True

    async def get_data(self):
        """Pokémon’un adı, sprite URL’si, türleri, yetenekleri ve istatistiklerini API’den çeker"""
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    self.name = data['forms'][0]['name']
                    self.image_url = data['sprites']['front_default']
                    self.types = [t['type']['name'] for t in data['types']]
                    self.abilities = [a['ability']['name'] for a in data['abilities']]
                    self.stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
                else:
                    # API'den veri çekilemezse varsayılan değerler
                    self.name = "Bilinmeyen Pokemon"
                    self.image_url = None
                    self.types = ["Bilinmiyor"]
                    self.abilities = ["Bilinmiyor"]
                    self.stats = {"special-attack": 0, "special-defense": 0, "speed": 0}

    def add_experience(self, amount):
        if getattr(self, "is_rare", False):
            amount *= 2  # Nadir Pokémonlar 2 kat deneyim kazanır
        self.experience += amount
        while self.experience >= self.level * 10:
            self.experience -= self.level * 10
            self.level += 1

    async def info(self):
        # Eğer isim çekilmemişse, get_data'yı çağır
        if not self.name or self.name == "Bilinmeyen Pokemon": # Bilinmeyen Pokemon ise de tekrar çekmeyi dene
            await self.get_data()

        types_str = ", ".join(self.types).capitalize() if self.types else "Bilinmiyor"
        abilities_str = ", ".join(self.abilities).capitalize() if self.abilities else "Bilinmiyor"
        stats_str = ", ".join(f"{k}: {v}" for k, v in self.stats.items()) if self.stats else "Bilinmiyor"
        rare_str = "⭐ Nadir Pokémon! ⭐" if getattr(self, "is_rare", False) else ""
        return (f"{rare_str}\nPokémonunuzun ismi: **{self.name.capitalize()}**, Seviye: **{self.level}**\n"
                f"Türler: {types_str}\n"
                f"Yetenekler: {abilities_str}\n"
                f"İstatistikler: {stats_str}\n"
                f"Sağlık (HP): {self.hp}\n"
                f"Güç (Power): {self.power}")

    async def show_img(self):
        # Eğer resim URL'si çekilmemişse, get_data'yı çağır
        if not self.image_url:
            await self.get_data()
        return self.image_url

    async def attack(self, enemy):
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return (f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ne saldırdı\n"
                    f"@{enemy.pokemon_trainer}'nin sağlık durumu {enemy.hp}")
        else:
            enemy.hp = 0
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ni yendi!"

# Alt sınıflar

class Wizard(Pokemon):
    async def attack(self, enemy):
        # Eğer düşman Wizard ise, kalkan ihtimali kontrolü
        if isinstance(enemy, Wizard):
            sans = rastgele_sayi(1, 5)
            if sans == 1:
                return "Sihirbaz Pokémon, savaşta bir kalkan kullandı! Saldırı etkisiz kaldı."
        # Normal saldırı
        return await super().attack(enemy)

class Fighter(Pokemon):
    async def attack(self, enemy):
        super_guc = rastgele_sayi(5, 15)
        self.power += super_guc
        sonuc = await super().attack(enemy)
        self.power -= super_guc
        return sonuc + f"\nDövüşçü Pokémon süper saldırı kullandı. Eklenen güç: {super_guc}"

# Test için main fonksiyonu

if __name__ == "__main__":
    async def main():
        wizard = Wizard("username1")
        fighter = Fighter("username2")
        print(await wizard.info())
        print("#" * 10)
        print(await fighter.info())
        print("#" * 10)
        print(await wizard.attack(fighter))
        print(await fighter.attack(wizard))


import aiohttp
import random
import asyncio

def rastgele_sayi(min_val, max_val):
    return random.randint(min_val, max_val)

class Pokemon:
    pokemons = {}  # Trainer → Pokemon instance

    def __new__(cls, pokemon_trainer):
        if pokemon_trainer in cls.pokemons:
            return cls.pokemons[pokemon_trainer]
        instance = super().__new__(cls)
        cls.pokemons[pokemon_trainer] = instance
        return instance

    def __init__(self, pokemon_trainer):
        if not hasattr(self, "initialized"):
            self.pokemon_trainer = pokemon_trainer
            # %5 ihtimalle nadir Pokémon seç
            if random.random() < 0.05:
                self.pokemon_number = random.randint(1, 150)  # Nadir Pokémon aralığı
                self.is_rare = True
            else:
                self.pokemon_number = random.randint(151, 1000)
                self.is_rare = False
            self.name = None
            self.image_url = None
            self.level = random.randint(1, 10)
            self.experience = 0
            self.types = []
            self.abilities = []
            self.stats = {}
            # Yeni eklenen özellikler:
            self.power = random.randint(30, 100)  # Güç (power)
            self.hp = random.randint(100, 400)    # Sağlık (hp)
            self.initialized = True

    async def get_data(self):
        """Pokémon’un adı, sprite URL’si, türleri, yetenekleri ve istatistiklerini API’den çeker"""
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    self.name = data['forms'][0]['name']
                    self.image_url = data['sprites']['front_default']
                    self.types = [t['type']['name'] for t in data['types']]
                    self.abilities = [a['ability']['name'] for a in data['abilities']]
                    self.stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
                else:
                    # API'den veri çekilemezse varsayılan değerler
                    self.name = "Bilinmeyen Pokemon"
                    self.image_url = None
                    self.types = ["Bilinmiyor"]
                    self.abilities = ["Bilinmiyor"]
                    self.stats = {"special-attack": 0, "special-defense": 0, "speed": 0}

    def add_experience(self, amount):
        if getattr(self, "is_rare", False):
            amount *= 2  # Nadir Pokémonlar 2 kat deneyim kazanır
        self.experience += amount
        while self.experience >= self.level * 10:
            self.experience -= self.level * 10
            self.level += 1

    async def info(self):
        # Eğer isim çekilmemişse, get_data'yı çağır
        if not self.name or self.name == "Bilinmeyen Pokemon": # Bilinmeyen Pokemon ise de tekrar çekmeyi dene
            await self.get_data()

        types_str = ", ".join(self.types).capitalize() if self.types else "Bilinmiyor"
        abilities_str = ", ".join(self.abilities).capitalize() if self.abilities else "Bilinmiyor"
        stats_str = ", ".join(f"{k}: {v}" for k, v in self.stats.items()) if self.stats else "Bilinmiyor"
        rare_str = "⭐ Nadir Pokémon! ⭐" if getattr(self, "is_rare", False) else ""
        return (f"{rare_str}\nPokémonunuzun ismi: **{self.name.capitalize()}**, Seviye: **{self.level}**\n"
                f"Türler: {types_str}\n"
                f"Yetenekler: {abilities_str}\n"
                f"İstatistikler: {stats_str}\n"
                f"Sağlık (HP): {self.hp}\n"
                f"Güç (Power): {self.power}")

    async def show_img(self):
        # Eğer resim URL'si çekilmemişse, get_data'yı çağır
        if not self.image_url:
            await self.get_data()
        return self.image_url

    async def attack(self, enemy):
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return (f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ne saldırdı\n"
                    f"@{enemy.pokemon_trainer}'nin sağlık durumu {enemy.hp}")
        else:
            enemy.hp = 0
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ni yendi!"

# Alt sınıflar

class Wizard(Pokemon):
    async def attack(self, enemy):
        # Eğer düşman Wizard ise, kalkan ihtimali kontrolü
        if isinstance(enemy, Wizard):
            sans = rastgele_sayi(1, 5)
            if sans == 1:
                return "Sihirbaz Pokémon, savaşta bir kalkan kullandı! Saldırı etkisiz kaldı."
        # Normal saldırı
        return await super().attack(enemy)

class Fighter(Pokemon):
    async def attack(self, enemy):
        super_guc = rastgele_sayi(5, 15)
        self.power += super_guc
        sonuc = await super().attack(enemy)
        self.power -= super_guc
        return sonuc + f"\nDövüşçü Pokémon süper saldırı kullandı. Eklenen güç: {super_guc}"

# Test için main fonksiyonu

if __name__ == "__main__":
    async def main():
        wizard = Wizard("username1")
        fighter = Fighter("username2")
        print(await wizard.info())
        print("#" * 10)
        print(await fighter.info())
        print("#" * 10)
        print(await wizard.attack(fighter))
        print(await fighter.attack(wizard))


    asyncio.run(main())