# 🛡️ V-Tunnel

**DNS, Proxy & VPN Management Tool**

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/this-is-the-leo)
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/Here_is_leo)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ilya-farahani-2160103b0)

---

## 📖 About The Project

**V-Tunnel** is a complete **Telegram Mini App** for managing and accessing lists of:

- **🌐 Public DNS Servers** (IPv4 & IPv6)
- **🔗 MTProto Proxies** (for Telegram)
- **🔒 V2Ray Configs** (VPN)

The project consists of a **Telegram bot** built with Python that serves the Mini App, along with a fully responsive web interface. All servers and configs are collected from public sources and are provided **free of charge** for **testing and development** purposes.

---

## 📁 Project Structure

```
📁 V-Tunnel/
├── 📄 bot.py                 # Telegram Bot (main Python code)
├── 📄 requirements.txt       # Python dependencies
├── 📄 .env                   # Environment variables (bot token)
├── 📁 mini-app/
│   ├── 📄 index.html         # Home page (dashboard)
│   ├── 📄 About.html         # About page
│   ├── 📄 DNS.html           # Public DNS list
│   ├── 📄 Proxy.html         # MTProto proxies list
│   └── 📄 VPN.html           # V2Ray configs list
└── 📁 assets/
    └── 📄 README.md          # Project documentation
```

---

## 🤖 Telegram Bot

The **Telegram bot** (`bot.py`) serves as the entry point for the Mini App.

### Bot Features
- **Start command** with welcome message
- **Inline button** to open the Mini App
- **Location detection** via Telegram WebApp SDK
- **Clean and professional interface**

### Bot Setup

1. Create a bot on Telegram via [@BotFather](https://t.me/BotFather)
2. Copy the bot token
3. Create a `.env` file with your token:
```env
BOT_TOKEN=your_bot_token_here
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the bot:
```bash
python bot.py
```

---

## 🎨 Mini App Interface

The web interface (`mini-app/` folder) is fully responsive and built with:

- **Glassmorphism Design** with dark, professional theme
- **Bilingual Support** (Persian & English)
- **Filter & Search** functionality
- **One-click Copy** for links and configs
- **Telegram WebApp Integration**

### 📱 Pages

| Page | File | Description | Count |
|---|---|---|---|
| **Home** | `index.html` | Dashboard with navigation buttons | — |
| **About** | `About.html` | Project information and developer intro | — |
| **DNS** | `DNS.html` | Public DNS list with IPv4/IPv6 filter | 100+ |
| **Proxy** | `Proxy.html` | MTProto proxies with secret type filter | 100+ |
| **VPN** | `VPN.html` | V2Ray configs with country filter | 250+ |

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/this-is-the-leo/V-Tunnel.git
cd V-Tunnel
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
Create a `.env` file in the root directory:
```env
BOT_TOKEN=your_telegram_bot_token
```

### 4. Run the Bot
```bash
python bot.py
```

### 5. Open the Mini App
- Send `/start` to your bot on Telegram
- Click the **"Open App"** button

---

## 🔧 Technologies

| Technology | Purpose |
|---|---|
| **Python** | Telegram bot backend |
| **python-telegram-bot** | Telegram Bot API wrapper |
| **HTML5 / CSS3** | Mini App structure & styling |
| **JavaScript (Vanilla)** | Logic, filtering, search & i18n |
| **Telegram WebApp SDK** | Telegram integration |
| **Fonts** | Vazirmatn (Persian) & Segoe UI (English) |

---

## ✨ Features

### 🌟 General Features
- **Glassmorphism Design** with dark, professional theme
- **Bilingual Support** (Persian & English) with live switching
- **Real-time Server Count** display
- **Filter & Search** functionality across all lists
- **Sorting** by various parameters
- **One-click Copy** for links and configs
- **Fully Responsive** across all devices
- **Telegram WebApp Integration** (location detection)

### 🗂️ Main Sections

| Section | Features |
|---|---|
| **DNS** | Filter by IPv4/IPv6, search by address/provider, sort by address/provider |
| **Proxy** | Filter by secret type, search by IP/port/secret, sort by IP/port |
| **VPN** | Filter by country, search in configs, sort by country/name |

---

## 🔑 Keyboard Shortcuts

| Key | Action |
|---|---|
| `Enter` / `Space` | Select / Copy item |
| `Tab` | Navigate between items |
| `Escape` | Close warning banners |

---

## 🌍 Bilingual Support

The project supports **Persian** and **English** languages.

- **Switch Language:** Click on language buttons in the header
- **Storage:** Selected language is saved in `localStorage`

---

## 📱 Responsiveness

| Screen Size | Changes |
|---|---|
| **> 768px** | Full display (3 columns on home page) |
| **480px - 768px** | Optimized with smaller sizes |
| **< 480px** | Single-column with mobile-friendly sizes |

---

## ⚠️ Disclaimer

> **Note:** This project is intended **only for testing and development** purposes.

- 🔴 Servers may become **unavailable or disabled** at any time
- 🔴 Responsibility for using these configs lies with the **user**
- 🔴 Using these servers for **illegal activities** is prohibited

---

## 📦 Requirements

```
python-telegram-bot==21.5
python-dotenv==1.0.1
```

---

## 🤝 Contributing

If you have ideas for improvement, I'd love to hear them:

1. **Fork** the repository
2. Create a new **Branch**
3. **Commit** your changes
4. Submit a **Pull Request**

---

## 📞 Contact

| Platform | Link |
|---|---|
| **GitHub** | [@this-is-the-leo](https://github.com/this-is-the-leo) |
| **Telegram** | [@Here_is_leo](https://t.me/Here_is_leo) |
| **LinkedIn** | [Ilya Farahani](https://www.linkedin.com/in/ilya-farahani-2160103b0) |

---

## 📄 License

This project is released under the **MIT License**.

```
MIT License

Copyright (c) 2025 Leo (Ilya Farahani)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## ⭐ Don't Forget to Star!

If you like this project, please give it a **⭐ star**!

---

**Developed with ❤️ by Leo**

---

---

---

# 🛡️ وی-تونل

**ابزار مدیریت DNS، پروکسی و VPN**

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/this-is-the-leo)
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/Here_is_leo)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ilya-farahani-2160103b0)

---

## 📖 درباره پروژه

**وی-تونل** یک **Telegram Mini App** کامل برای مدیریت و دسترسی به لیست‌های زیر است:

- **🌐 DNS های عمومی** (IPv4 و IPv6)
- **🔗 پروکسی‌های MTProto** (مخصوص تلگرام)
- **🔒 کانفیگ‌های V2Ray** (VPN)

این پروژه از یک **ربات تلگرام** ساخته‌شده با پایتون تشکیل شده است که Mini App را سرو می‌دهد، همراه با یک رابط وب کاملاً واکنش‌گرا. تمامی سرورها و کانفیگ‌ها از منابع عمومی جمع‌آوری شده‌اند و به صورت **رایگان** برای اهداف **آزمایش و توسعه** ارائه می‌شوند.

---

## 📁 ساختار پروژه

```
📁 V-Tunnel/
├── 📄 bot.py                 # ربات تلگرام (کد اصلی پایتون)
├── 📄 requirements.txt       # نیازمندی‌های پایتون
├── 📄 .env                   # متغیرهای محیطی (توکن ربات)
├── 📁 mini-app/
│   ├── 📄 index.html         # صفحه اصلی (داشبورد)
│   ├── 📄 About.html         # صفحه درباره
│   ├── 📄 DNS.html           # لیست DNS های عمومی
│   ├── 📄 Proxy.html         # لیست پروکسی‌های MTProto
│   └── 📄 VPN.html           # لیست کانفیگ‌های V2Ray
└── 📁 assets/
    └── 📄 README.md          # مستندات پروژه
```

---

## 🤖 ربات تلگرام

**ربات تلگرام** (`bot.py`) به‌عنوان نقطه ورود Mini App عمل می‌کند.

### ویژگی‌های ربات
- **دستور شروع** با پیام خوش‌آمدگویی
- **دکمه شیشه‌ای** برای باز کردن Mini App
- **تشخیص موقعیت مکانی** از طریق Telegram WebApp SDK
- **رابط کاربری تمیز و حرفه‌ای**

### راه‌اندازی ربات

۱. یک ربات در تلگرام از طریق [@BotFather](https://t.me/BotFather) بسازید
۲. توکن ربات را کپی کنید
۳. یک فایل `.env` با توکن خود بسازید:
```env
BOT_TOKEN=توکن_ربات_خود_را_اینجا_قرار_دهید
```

۴. نیازمندی‌ها را نصب کنید:
```bash
pip install -r requirements.txt
```

۵. ربات را اجرا کنید:
```bash
python bot.py
```

---

## 🎨 رابط Mini App

رابط وب (پوشه `mini-app/`) کاملاً واکنش‌گرا و ساخته‌شده با:

- **طراحی شیشه‌ای (Glassmorphism)** با تم تیره و حرفه‌ای
- **پشتیبانی از دو زبان** فارسی و انگلیسی
- **فیلتر و جستجو**
- **کپی یک‌کلیک** لینک‌ها و کانفیگ‌ها
- **یکپارچه‌سازی با تلگرام WebApp**

### 📱 صفحات

| صفحه | فایل | توضیحات | تعداد |
|---|---|---|---|
| **خانه** | `index.html` | داشبورد با دکمه‌های ناوبری | — |
| **درباره** | `About.html` | اطلاعات پروژه و معرفی توسعه‌دهنده | — |
| **DNS** | `DNS.html` | لیست DNS های عمومی با فیلتر IPv4/IPv6 | ۱۰۰+ |
| **Proxy** | `Proxy.html` | پروکسی‌های MTProto با فیلتر نوع سکرت | ۱۰۰+ |
| **VPN** | `VPN.html` | کانفیگ‌های V2Ray با فیلتر کشور | ۲۵۰+ |

---

## 🚀 شروع سریع

### ۱. کلون کردن مخزن
```bash
git clone https://github.com/this-is-the-leo/V-Tunnel.git
cd V-Tunnel
```

### ۲. نصب نیازمندی‌ها
```bash
pip install -r requirements.txt
```

### ۳. پیکربندی محیط
یک فایل `.env` در ریشه پروژه بسازید:
```env
BOT_TOKEN=توکن_ربات_تلگرام_خود
```

### ۴. اجرای ربات
```bash
python bot.py
```

### ۵. باز کردن Mini App
- به ربات خود در تلگرام پیام `/start` بدهید
- روی دکمه **"باز کردن برنامه"** کلیک کنید

---

## 🔧 تکنولوژی‌ها

| تکنولوژی | کاربرد |
|---|---|
| **Python** | بک‌اند ربات تلگرام |
| **python-telegram-bot** | رابط Telegram Bot API |
| **HTML5 / CSS3** | ساختار و استایل Mini App |
| **JavaScript (Vanilla)** | منطق، فیلتر، جستجو و ترجمه |
| **Telegram WebApp SDK** | یکپارچه‌سازی با تلگرام |
| **Fonts** | وزیرمتن (فارسی) و Segoe UI (انگلیسی) |

---

## ✨ ویژگی‌ها

### 🌟 قابلیت‌های کلی
- **طراحی شیشه‌ای (Glassmorphism)** با تم تیره و حرفه‌ای
- **پشتیبانی از دو زبان** فارسی و انگلیسی (با قابلیت تغییر زنده)
- **نمایش تعداد سرورها** به‌صورت لحظه‌ای
- **فیلتر و جستجو** در تمامی لیست‌ها
- **مرتب‌سازی** بر اساس پارامترهای مختلف
- **کپی یک‌کلیک** لینک‌ها و کانفیگ‌ها
- **واکنش‌گرایی کامل** در تمامی دستگاه‌ها

### 🗂️ بخش‌های اصلی

| بخش | ویژگی‌ها |
|---|---|
| **DNS** | فیلتر IPv4/IPv6، جستجو در آدرس/ارائه‌دهنده، مرتب‌سازی بر اساس آدرس/ارائه‌دهنده |
| **Proxy** | فیلتر نوع سکرت، جستجو در IP/پورت/سکرت، مرتب‌سازی بر اساس IP/پورت |
| **VPN** | فیلتر کشور، جستجو در کانفیگ‌ها، مرتب‌سازی بر اساس کشور/نام |

---

## 🔑 میانبرهای کلیدی

| کلید | عملکرد |
|---|---|
| `Enter` / `Space` | انتخاب / کپی مورد |
| `Tab` | حرکت بین آیتم‌ها |
| `Escape` | بستن بنرهای هشدار |

---

## 🌍 پشتیبانی دو‌زبانه

پروژه از دو زبان **فارسی** و **انگلیسی** پشتیبانی می‌کند.

- **تغییر زبان:** با کلیک روی دکمه‌های موجود در هدر
- **ذخیره‌سازی:** زبان انتخابی در `localStorage` ذخیره می‌شود

---

## 📱 واکنش‌گرایی

| اندازه صفحه | تغییرات |
|---|---|
| **> 768px** | نمایش کامل (۳ ستونه در صفحه اصلی) |
| **480px - 768px** | نمایش بهینه با اندازه‌های کوچک‌تر |
| **< 480px** | نمایش تک‌ستونه با اندازه‌های مناسب موبایل |

---

## ⚠️ هشدارها

> **توجه:** این پروژه صرفاً برای **آزمایش و توسعه** طراحی شده است.

- 🔴 سرورها ممکن است در هر زمان **قطع یا غیرفعال** شوند
- 🔴 مسئولیت استفاده بر عهده **کاربر** می‌باشد
- 🔴 استفاده برای فعالیت‌های **غیرقانونی** ممنوع است

---

## 📦 نیازمندی‌ها

```
python-telegram-bot==21.5
python-dotenv==1.0.1
```

---

## 🤝 مشارکت

اگر ایده‌ای برای بهبود دارید، خوشحال می‌شوم بشنوم:

۱. **Fork** کنید
۲. **Branch** جدید بسازید
۳. تغییرات خود را **Commit** کنید
۴. **Pull Request** ارسال کنید

---

## 📞 ارتباط با توسعه‌دهنده

| پلتفرم | لینک |
|---|---|
| **GitHub** | [@this-is-the-leo](https://github.com/this-is-the-leo) |
| **Telegram** | [@Here_is_leo](https://t.me/Here_is_leo) |
| **LinkedIn** | [ایلیا فراهانی](https://www.linkedin.com/in/ilya-farahani-2160103b0) |

---

## 📄 مجوز

این پروژه تحت مجوز **MIT** منتشر شده است.

```
MIT License

Copyright (c) 2025 Leo (Ilya Farahani)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## ⭐ ستاره فراموش نشه!

اگر از این پروژه خوشتان آمد، حتماً به آن **⭐ ستاره** دهید!

---

**توسعه‌یافته با ❤️ توسط Leo**
