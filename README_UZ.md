# Majnuntol APK Quriqchi bot

1. Python 3.11 yoki yangirog‘ini o‘rnating.
2. `.env.example` faylidan nusxa oling va nusxasini `.env` deb nomlang.
3. `.env` faylida `BOT_TOKEN=` dan keyin BotFather tokeningizni yozing. Tokenni hech kimga yubormang.
4. PowerShellni shu papkada ochib bajaring:

```powershell
py -m venv .venv
.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt
.\\.venv\\Scripts\\python.exe bot.py
```

Terminal ochiq turganida bot ishlaydi. `Ctrl+C` to‘xtatadi.

Eslatma: bot `/start` bosgan Telegram akkauntlarini bir marta sanaydi; bu APK yuklab olinganini tasdiqlamaydi. 24/7 ishlashi uchun serverga joylash kerak.
