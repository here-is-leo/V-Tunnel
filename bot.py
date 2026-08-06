import os
import sys
import logging
import json
import asyncio
import threading
from datetime import datetime
from typing import Dict, List, Optional, Any

# Python 3.13 compatibility patches
if sys.version_info >= (3, 13):
    import types

    # imghdr patch
    imghdr_module = types.ModuleType('imghdr')

    def what(file, h=None):
        if h is None:
            if isinstance(file, (bytes, bytearray)):
                h = file
            else:
                try:
                    with open(file, 'rb') as f:
                        h = f.read(32)
                except Exception:
                    return None
        else:
            if isinstance(h, str):
                h = h.encode('utf-8')

        if not h or len(h) < 8:
            return None

        signatures = [
            (b'\x89PNG\r\n\x1a\n', 'png'),
            (b'GIF87a', 'gif'),
            (b'GIF89a', 'gif'),
            (b'BM', 'bmp'),
            (b'\xff\xd8\xff\xe0', 'jpeg'),
            (b'\xff\xd8\xff\xe1', 'jpeg'),
            (b'\xff\xd8\xff\xe2', 'jpeg'),
            (b'\xff\xd8\xff\xe3', 'jpeg'),
            (b'RIFF', 'webp'),
            (b'\x00\x00\x01\x00', 'ico'),
            (b'\x00\x00\x02\x00', 'cur'),
            (b'II\x2a\x00', 'tiff'),
            (b'MM\x00\x2a', 'tiff'),
        ]

        for sig, img_type in signatures:
            if h[:len(sig)] == sig:
                if img_type == 'webp' and len(h) >= 12:
                    if h[8:12] == b'WEBP':
                        return 'webp'
                    else:
                        continue
                return img_type

        if h[:3] in (b'P1', b'P2', b'P3', b'P4', b'P5', b'P6'):
            return 'ppm'

        return None

    imghdr_module.what = what
    sys.modules['imghdr'] = imghdr_module

    # asyncio patches
    if not hasattr(asyncio, 'all_tasks'):
        asyncio.all_tasks = asyncio.Task.all_tasks
    if not hasattr(asyncio, 'current_task'):
        asyncio.current_task = asyncio.Task.current_task

    # threading patch
    if not hasattr(threading, 'main_thread'):
        threading.main_thread = threading._MainThread

    # urllib3 patch
    try:
        import urllib3.contrib.appengine
    except (ImportError, ModuleNotFoundError):
        fake_appengine = types.ModuleType('urllib3.contrib.appengine')
        fake_appengine.AppEngineManager = None
        fake_appengine.AppEnginePlatformWarning = None
        fake_appengine.IsAppEngine = False
        fake_appengine.has_google_appengine = False
        sys.modules['urllib3.contrib.appengine'] = fake_appengine

# Main imports
try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
    from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Import error: {e}")
    print("\nSolution:")
    print("   pip uninstall python-telegram-bot httpx httpcore anyio h11 urllib3 -y")
    print("   pip install python-telegram-bot==20.8")
    sys.exit(1)

# Updater patch for Python 3.13
if sys.version_info >= (3, 13):
    try:
        import telegram.ext as _tg_ext

        class _PatchedUpdater(_tg_ext.Updater):
            def __init__(self, *args, **kwargs):
                self._Updater__polling_cleanup_cb = None
                self._Updater__polling_cleanup_lock = threading.Lock()
                self._Updater__polling_task = None
                super().__init__(*args, **kwargs)
                if not hasattr(self, '_Updater__polling_cleanup_cb'):
                    self._Updater__polling_cleanup_cb = None
                if not hasattr(self, '_Updater__polling_cleanup_lock'):
                    self._Updater__polling_cleanup_lock = threading.Lock()
                if not hasattr(self, '_Updater__polling_task'):
                    self._Updater__polling_task = None

        _tg_ext.Updater = _PatchedUpdater
        sys.modules['telegram.ext'].Updater = _PatchedUpdater
    except Exception as e:
        print(f"Updater patch warning: {e}")

load_dotenv()

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
TOKEN = os.getenv('BOT_TOKEN')
if not TOKEN:
    raise ValueError("BOT_TOKEN not set in .env file")

MINI_APP_URL = os.getenv('MINI_APP_URL', 'https://your-domain.com/mini-app/index.html')
START_TIME = datetime.now()

# Admin IDs
ADMIN_IDS = []
admin_ids_str = os.getenv('ADMIN_IDS', '')
if admin_ids_str:
    try:
        ADMIN_IDS = [int(x.strip()) for x in admin_ids_str.split(',') if x.strip()]
    except ValueError:
        pass

if not ADMIN_IDS:
    single_admin = os.getenv('ADMIN_ID', '')
    if single_admin:
        try:
            ADMIN_IDS = [int(single_admin)]
        except ValueError:
            pass

print(f"Admins: {ADMIN_IDS}")


# In-memory database
class Database:
    def __init__(self):
        self.users = {}
        self.stats = {
            'total_commands': 0,
            'total_users': 0,
            'active_users': 0,
            'daily_active': 0,
            'last_reset': datetime.now().date()
        }
        self.banned_users = set()
        self.admin_ids = ADMIN_IDS
        self.feedback_list = []

    def add_user(self, user_id: int, user_data: dict):
        if user_id not in self.users:
            self.users[user_id] = {
                'first_seen': datetime.now(),
                'last_seen': datetime.now(),
                'name': user_data.get('first_name', 'Unknown'),
                'username': user_data.get('username', ''),
                'commands': 0,
                'lang': 'fa',
                'is_premium': False
            }
            self.stats['total_users'] = len(self.users)
            self.stats['active_users'] += 1
            return True
        return False

    def update_user(self, user_id: int):
        if user_id in self.users:
            self.users[user_id]['last_seen'] = datetime.now()
            self.users[user_id]['commands'] += 1
            self.stats['total_commands'] += 1
            return True
        return False

    def is_banned(self, user_id: int) -> bool:
        return user_id in self.banned_users

    def is_admin(self, user_id: int) -> bool:
        return user_id in self.admin_ids

    def get_stats(self) -> dict:
        today = datetime.now().date()
        active_today = sum(1 for u in self.users.values()
                           if u['last_seen'].date() == today)
        self.stats['daily_active'] = active_today
        return self.stats

    def get_user_count(self) -> int:
        return len(self.users)

    def add_feedback(self, user_id: int, feedback: str):
        self.feedback_list.append({
            'user_id': user_id,
            'feedback': feedback,
            'time': datetime.now()
        })

    def get_feedbacks(self, limit: int = 20):
        return self.feedback_list[-limit:]


db = Database()

# Message templates
WELCOME_MESSAGE = """
🚀 Welcome to V-Tunnel!

Hello {first_name}!

V-Tunnel helps you manage:

🌐 DNS Servers
🔗 MTProto Proxies
🔒 V2Ray Configs

All services are free and public.

Note: This service is for testing purposes only.
"""

HELP_MESSAGE = """
📖 Help Guide

Commands:
/start - Welcome message
/help - This guide
/about - About bot
/mini - Open Mini App
/feedback - Send feedback
/support - Contact developer

How to use:
1. Click "Open V-Tunnel" button
2. Choose DNS, Proxy, or VPN
3. Click on any item to copy
"""

ABOUT_MESSAGE = """
ℹ️ About V-Tunnel

Version: 2.0.0
Developer: Leo
Status: Active

Features:
- DNS Management (100+ servers)
- MTProto Proxy Management
- V2Ray Config Management
- Modern UI
- Free & Public
- Privacy Friendly
"""

ADMIN_PANEL_TEXT = """
👑 Admin Panel

Stats:
- Users: {users}
- Commands: {commands}
- Active Today: {daily_active}
- Uptime: {uptime}

Admin Commands:
/broadcast [text]
/adminstats
/adminlist
/adminfeedback
/adminban [id]
/adminunban [id]
"""


# Helper functions
def check_user(update: Update) -> bool:
    user = update.effective_user
    if not user:
        return False

    user_id = user.id

    if db.is_banned(user_id):
        return False

    db.add_user(user_id, {
        'first_name': user.first_name,
        'username': user.username
    })

    db.update_user(user_id)
    return True


# Public commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not check_user(update):
        return

    user = update.effective_user
    first_name = user.first_name if user.first_name else "User"

    keyboard = [
        [InlineKeyboardButton("Open V-Tunnel", web_app=WebAppInfo(url=MINI_APP_URL))],
        [InlineKeyboardButton("Contact Developer", url="https://t.me/your_username")],
        [InlineKeyboardButton("Help", callback_data="help"),
         InlineKeyboardButton("About", callback_data="about")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        query = update.callback_query
        await query.edit_message_text(
            WELCOME_MESSAGE.format(first_name=first_name),
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            WELCOME_MESSAGE.format(first_name=first_name),
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not check_user(update):
        return

    if update.callback_query:
        query = update.callback_query
        await query.answer()
        message = query.message
    else:
        message = update.message

    keyboard = [
        [InlineKeyboardButton("Open V-Tunnel", web_app=WebAppInfo(url=MINI_APP_URL))],
        [InlineKeyboardButton("Home", callback_data="home"),
         InlineKeyboardButton("About", callback_data="about")],
        [InlineKeyboardButton("Contact Developer", url="https://t.me/your_username")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await query.edit_message_text(
            HELP_MESSAGE,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    else:
        await message.reply_text(
            HELP_MESSAGE,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not check_user(update):
        return

    if update.callback_query:
        query = update.callback_query
        await query.answer()
        message = query.message
    else:
        message = update.message

    keyboard = [
        [InlineKeyboardButton("Open V-Tunnel", web_app=WebAppInfo(url=MINI_APP_URL))],
        [InlineKeyboardButton("Home", callback_data="home"),
         InlineKeyboardButton("Help", callback_data="help")],
        [InlineKeyboardButton("Contact Developer", url="https://t.me/your_username")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    uptime_delta = datetime.now() - START_TIME
    hours = uptime_delta.seconds // 3600
    minutes = (uptime_delta.seconds % 3600) // 60
    uptime_str = f"{hours}h {minutes}m"

    about_text = ABOUT_MESSAGE + f"\n\nUptime: {uptime_str}"

    if update.callback_query:
        await query.edit_message_text(
            about_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    else:
        await message.reply_text(
            about_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id

    if not db.is_admin(user_id):
        await update.message.reply_text(
            "Access denied. Admin only.",
            parse_mode='Markdown'
        )
        return

    stats = db.get_stats()
    uptime_delta = datetime.now() - START_TIME
    hours = uptime_delta.seconds // 3600
    minutes = (uptime_delta.seconds % 3600) // 60

    stats_text = f"""
📊 Stats

Users:
- Total: {stats['total_users']}
- Active Today: {stats['daily_active']}

Usage:
- Total Commands: {stats['total_commands']}

System:
- Uptime: {hours}h {minutes}m
- Version: 2.0.0
- Status: Active
"""

    keyboard = [
        [InlineKeyboardButton("Refresh", callback_data="refresh_stats")],
        [InlineKeyboardButton("Home", callback_data="home")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(stats_text, reply_markup=reply_markup, parse_mode='Markdown')


async def mini_app_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not check_user(update):
        return

    keyboard = [
        [InlineKeyboardButton("Open V-Tunnel", web_app=WebAppInfo(url=MINI_APP_URL))],
        [InlineKeyboardButton("Home", callback_data="home"),
         InlineKeyboardButton("Help", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Click the button below to open V-Tunnel:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def feedback_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not check_user(update):
        return

    feedback_text = ' '.join(context.args)

    if not feedback_text:
        keyboard = [[InlineKeyboardButton("Home", callback_data="home")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "Send feedback: /feedback [your message]",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return

    user = update.effective_user
    db.add_feedback(user.id, feedback_text)

    for admin_id in db.admin_ids:
        try:
            await context.bot.send_message(
                admin_id,
                f"New Feedback\n\nUser: {user.first_name}\nID: `{user.id}`\n\n{feedback_text}",
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Error sending feedback to admin: {e}")

    keyboard = [[InlineKeyboardButton("Home", callback_data="home")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Feedback received!\n\n{feedback_text}",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def support_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not check_user(update):
        return

    keyboard = [
        [InlineKeyboardButton("Contact Developer", url="https://t.me/your_username")],
        [InlineKeyboardButton("Home", callback_data="home")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Contact the developer:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not check_user(update):
        return

    keyboard = [
        [InlineKeyboardButton("Help", callback_data="help")],
        [InlineKeyboardButton("Home", callback_data="home")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Unknown command. Use /help for assistance.",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


# Admin commands
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id

    if not db.is_admin(user_id):
        return

    stats = db.get_stats()
    uptime_delta = datetime.now() - START_TIME
    hours = uptime_delta.seconds // 3600
    minutes = (uptime_delta.seconds % 3600) // 60
    uptime_str = f"{hours}h {minutes}m"

    keyboard = [
        [InlineKeyboardButton("Broadcast", callback_data="admin_broadcast")],
        [InlineKeyboardButton("Full Stats", callback_data="admin_stats")],
        [InlineKeyboardButton("User List", callback_data="admin_list")],
        [InlineKeyboardButton("Feedbacks", callback_data="admin_feedback")],
        [InlineKeyboardButton("Ban User", callback_data="admin_ban")],
        [InlineKeyboardButton("Unban User", callback_data="admin_unban")],
        [InlineKeyboardButton("Home", callback_data="home")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        ADMIN_PANEL_TEXT.format(
            users=stats['total_users'],
            commands=stats['total_commands'],
            daily_active=stats['daily_active'],
            uptime=uptime_str
        ),
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def admin_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if not db.is_admin(user_id):
        return

    broadcast_text = ' '.join(context.args)

    if not broadcast_text:
        await update.message.reply_text(
            "Usage: /broadcast [message]",
            parse_mode='Markdown'
        )
        return

    total_users = len(db.users)
    sent = 0
    failed = 0

    for uid in db.users.keys():
        try:
            await context.bot.send_message(
                uid,
                f"Broadcast\n\n{broadcast_text}",
                parse_mode='Markdown'
            )
            sent += 1
        except Exception as e:
            failed += 1
            logger.error(f"Failed to send to {uid}: {e}")

    await update.message.reply_text(
        f"Broadcast sent!\n\nSent: {sent}\nFailed: {failed}\nTotal: {total_users}",
        parse_mode='Markdown'
    )


async def admin_stats_full(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if not db.is_admin(user_id):
        return

    stats = db.get_stats()
    days_active = max(1, (datetime.now() - START_TIME).days)
    avg_commands = stats['total_commands'] // days_active

    await update.message.reply_text(
        f"Admin Stats\n\n"
        f"Users: {stats['total_users']}\n"
        f"Active Today: {stats['daily_active']}\n"
        f"Total Commands: {stats['total_commands']}\n"
        f"Daily Average: {avg_commands}\n"
        f"Uptime: {days_active} days\n"
        f"Version: 2.0.0",
        parse_mode='Markdown'
    )


async def admin_list_users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if not db.is_admin(user_id):
        return

    users = db.users
    total = len(users)

    if total == 0:
        await update.message.reply_text("No users registered.")
        return

    user_list = ""
    count = 0
    for uid, info in users.items():
        if count >= 20:
            user_list += f"\n... and {total - 20} more"
            break
        user_list += f"`{uid}` - {info['name']}\n"
        count += 1

    await update.message.reply_text(
        f"Users ({total})\n\n{user_list}",
        parse_mode='Markdown'
    )


async def admin_feedback_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if not db.is_admin(user_id):
        return

    feedbacks = db.get_feedbacks(10)

    if not feedbacks:
        await update.message.reply_text("No feedbacks.")
        return

    text = "Last 10 Feedbacks:\n\n"
    for fb in feedbacks:
        text += f"User: `{fb['user_id']}`\n{fb['feedback']}\n{fb['time'].strftime('%Y-%m-%d %H:%M')}\n\n"

    await update.message.reply_text(text, parse_mode='Markdown')


async def admin_ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if not db.is_admin(user_id):
        return

    args = context.args
    if not args:
        await update.message.reply_text(
            "Usage: /adminban [user_id]",
            parse_mode='Markdown'
        )
        return

    try:
        target_id = int(args[0])
        if target_id in db.admin_ids:
            await update.message.reply_text("Cannot ban an admin!")
            return

        db.banned_users.add(target_id)
        await update.message.reply_text(f"User `{target_id}` banned.", parse_mode='Markdown')
        logger.info(f"Admin {user_id} banned user {target_id}")
    except ValueError:
        await update.message.reply_text("Invalid user ID.")


async def admin_unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if not db.is_admin(user_id):
        return

    args = context.args
    if not args:
        await update.message.reply_text(
            "Usage: /adminunban [user_id]",
            parse_mode='Markdown'
        )
        return

    try:
        target_id = int(args[0])
        if target_id in db.banned_users:
            db.banned_users.remove(target_id)
            await update.message.reply_text(f"User `{target_id}` unbanned.", parse_mode='Markdown')
            logger.info(f"Admin {user_id} unbanned user {target_id}")
        else:
            await update.message.reply_text(f"User `{target_id}` is not banned.", parse_mode='Markdown')
    except ValueError:
        await update.message.reply_text("Invalid user ID.")


async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not check_user(update):
        return

    data = update.message.web_app_data

    if data:
        logger.info(f"Webapp data from {update.effective_user.id}: {data.data}")
        await update.message.reply_text("Data received successfully!", parse_mode='Markdown')


# Callback handler
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not check_user(update):
        return

    query = update.callback_query
    await query.answer()

    data = query.data
    user_id = update.effective_user.id
    is_admin = db.is_admin(user_id)

    # Public callbacks
    if data == "home":
        await start(update, context)
    elif data == "help":
        await help_command(update, context)
    elif data == "about":
        await about_command(update, context)
    elif data == "stats" or data == "refresh_stats":
        if not is_admin:
            await query.edit_message_text(
                "Access denied. Admin only.",
                parse_mode='Markdown'
            )
            return
        await stats_command(update, context)

    # Admin callbacks
    elif data.startswith("admin_"):
        if not is_admin:
            return

        if data == "admin_broadcast":
            await query.edit_message_text(
                "Usage: /broadcast [message]",
                parse_mode='Markdown'
            )
        elif data == "admin_stats":
            await admin_stats_full(update, context)
        elif data == "admin_list":
            await admin_list_users(update, context)
        elif data == "admin_feedback":
            await admin_feedback_list(update, context)
        elif data == "admin_ban":
            await query.edit_message_text(
                "Usage: /adminban [user_id]",
                parse_mode='Markdown'
            )
        elif data == "admin_unban":
            await query.edit_message_text(
                "Usage: /adminunban [user_id]",
                parse_mode='Markdown'
            )


# Main entry point
async def run_bot() -> None:
    application = Application.builder().token(TOKEN).build()

    # Public commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("mini", mini_app_button))
    application.add_handler(CommandHandler("feedback", feedback_command))
    application.add_handler(CommandHandler("support", support_command))

    # Admin commands
    application.add_handler(CommandHandler("4dmin", admin_panel))
    application.add_handler(CommandHandler("broadcast", admin_broadcast))
    application.add_handler(CommandHandler("adminstats", admin_stats_full))
    application.add_handler(CommandHandler("adminlist", admin_list_users))
    application.add_handler(CommandHandler("adminfeedback", admin_feedback_list))
    application.add_handler(CommandHandler("adminban", admin_ban_user))
    application.add_handler(CommandHandler("adminunban", admin_unban_user))

    # Other handlers
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp_data))
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))
    application.add_handler(CallbackQueryHandler(button_callback))

    try:
        bot_info = await application.bot.get_me()
        bot_username = bot_info.username

        print("\n" + "=" * 50)
        print("V-Tunnel v2.0 Started")
        print(f"Bot: @{bot_username}")
        print(f"Admins: {db.admin_ids}")
        print("=" * 50)
        print("Running... (Ctrl+C to stop)")
        print("=" * 50 + "\n")
    except Exception as e:
        print(f"Could not get bot info: {e}")

    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        pass
    finally:
        await application.updater.stop()
        await application.stop()
        await application.shutdown()


def main() -> None:
    print("\n" + "=" * 50)
    print("V-Tunnel v2.0 Starting...")
    print("=" * 50 + "\n")

    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        print("\nBot stopped.")
    except Exception as e:
        print(f"\nError: {e}")
        print("\nSolution:")
        print("   pip install python-telegram-bot==20.8")
        print("   python bot.py")


if __name__ == '__main__':
    main()
