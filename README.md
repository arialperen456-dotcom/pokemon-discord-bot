# 🎮 Pokémon Discord Bot  

![Pokemon Logo](https://raw.githubusercontent.com/PokeAPI/media/master/logo/pokeapi_256.png)

## 📌 Proje Açıklaması
Bu proje, **Discord üzerinde Pokémon eğlenceleri yaşamanızı sağlayan bir bot** geliştirmeyi amaçlar.  
Bot sayesinde kullanıcılar Pokémon yakalayabilir, besleyebilir, seviye atlatabilir ve detaylı istatistiklerini görebilirler.  

---

## 🚀 Özellikler
- 🐾 **!go** → Yeni bir Pokémon oluşturur.  
- 🍖 **!feed** → Pokémon'unuzu besler, HP yükselir ve EXP kazanır.  
- ℹ️ **!info** → Pokémon’un tür, yetenek ve istatistiklerini gösterir.  
- ⭐ **Nadir Pokémon şansı** (%5 ihtimalle özel Pokémon).  
- 📊 **EXP bar** → Seviye atlamaya kalan süreyi ilerleme çubuğu şeklinde gösterir.  

---

## 📸 Kullanım Örnekleri
> Örnek ekran görüntülerini buraya ekleyebilirsin (Discord’dan aldığın bot çıktılarının ekran görüntüsü).

Kullanıcı: !go
Bot: Yeni bir Pokémon oluşturuldu! 🐉

Kodu kopyala
Kullanıcı: !feed
Bot: Pikachu beslenildi! HP arttı ⚡
Seviye: 3
EXP: [███-------] 7/30

yaml
Kodu kopyala

---

## 🛠️ Kurulum
1. Bu depoyu klonlayın:
   ```bash
   git clone https://github.com/<kullanıcı-adınız>/pokemon-discord-bot.git
Gerekli kütüphaneleri yükleyin:

bash
Kodu kopyala
pip install -r requirements.txt
Discord bot tokeninizi config.py içine ekleyin:

python
Kodu kopyala
token = "YOUR_BOT_TOKEN"
Botu çalıştırın:

bash
Kodu kopyala
python main.py
👨‍💻 Geliştirici Notları
Python 3.10+ sürümünde çalışmaktadır.

Discord.py kütüphanesi kullanılmaktadır.

Veriler PokeAPI üzerinden çekilmektedir.

🌟 Katkıda Bulunma
Katkılarınızı memnuniyetle karşılıyoruz!

Depoyu fork’layın 🍴

Yeni branch açın 🌿

PR gönderin 🚀

📜 Lisans
Bu proje MIT lisansı ile yayınlanmaktadır.
