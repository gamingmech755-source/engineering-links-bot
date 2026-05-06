import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID', '0'))
ADSTERRA_LINK = os.getenv('ADSTERRA_LINK')

DISCLAIMER = """
⚠️ **DISCLAIMER** ⚠️

We do not host or share any pirated content. Our channel only shares links to courses that are already available on Telegram. All rights belong to the respective institutes and content owners.

If any owner has an issue, please contact us and the content will be removed immediately.

We respect copyright laws and comply with DMCA regulations.

**Copyright Disclaimer:** Under Section 107 of the Copyright Act 1976, allowance is made for "fair use". Non-profit or educational use tips the balance in favor of fair use.

By continuing, you agree to these terms.
"""

BRANCHES = {
    'cse': {
        'name': 'Computer Science Engineering',
        'links': [
            ('pwthor.live', 'https://pwthor.live'),
            ('ASM Universe', 'https://asmultiverse.com'),
            ('Spidy Universe', 'https://t.me/Spidyxuniverse0'),
            ('Study Group', 'https://t.me/+m2kdPw7UkI8yODM1'),
            ('Squid Study', 'https://squidstudy.eu.org'),
            ('GATE ESE 27', 'https://t.me/Gate_ese27'),
            ('GATE Prep Zone', 'https://t.me/GATEPrepZone'),
            ('Engineering Waala', 'https://t.me/EngineeringWaala'),
            ('VD List', 'https://t.me/addlist/VD_Og7nrSINmZGFl'),
            ('PW Jarvis', 'https://pwjarvis.com')
        ]
    },
    'ece': {
        'name': 'Electronics & Communication Engineering',
        'links': [
            ('pwthor.live', 'https://pwthor.live'),
            ('ASM Universe', 'https://asmultiverse.com'),
            ('Spidy Universe', 'https://t.me/Spidyxuniverse0'),
            ('Study Group', 'https://t.me/+m2kdPw7UkI8yODM1'),
            ('Squid Study', 'https://squidstudy.eu.org'),
            ('GATE ESE 27', 'https://t.me/Gate_ese27'),
            ('GATE Prep Zone', 'https://t.me/GATEPrepZone'),
            ('Engineering Waala', 'https://t.me/EngineeringWaala'),
            ('VD List', 'https://t.me/addlist/VD_Og7nrSINmZGFl'),
            ('PW Jarvis', 'https://pwjarvis.com'),
            ('ECE WhatsApp', 'https://whatsapp.com/channel/0029Vb8AsJkKmCPZLrIUfL2A'),
            ('ECE Telegram', 'https://t.me/+chVmtEO8IFJiOThl')
        ]
    },
    'ee': {
        'name': 'Electrical Engineering',
        'links': [
            ('pwthor.live', 'https://pwthor.live'),
            ('ASM Universe', 'https://asmultiverse.com'),
            ('Spidy Universe', 'https://t.me/Spidyxuniverse0'),
            ('Study Group', 'https://t.me/+m2kdPw7UkI8yODM1'),
            ('Squid Study', 'https://squidstudy.eu.org'),
            ('GATE ESE 27', 'https://t.me/Gate_ese27'),
            ('GATE Prep Zone', 'https://t.me/GATEPrepZone'),
            ('Engineering Waala', 'https://t.me/EngineeringWaala'),
            ('VD List', 'https://t.me/addlist/VD_Og7nrSINmZGFl'),
            ('PW Jarvis', 'https://pwjarvis.com'),
            ('EE WhatsApp', 'https://whatsapp.com/channel/0029Vb8AsJkKmCPZLrIUfL2A'),
            ('EE Telegram', 'https://t.me/+chVmtEO8IFJiOThl')
        ]
    },
    'me': {
        'name': 'Mechanical Engineering',
        'links': [
            ('Mechanical GATE ESE JE Notes', 'https://t.me/mechanical_Gate_ese_je_notes2027')
        ]
    },
    'civil': {
        'name': 'Civil Engineering',
        'links': [
            ('pwthor.live', 'https://pwthor.live'),
            ('ASM Universe', 'https://asmultiverse.com'),
            ('Spidy Universe', 'https://t.me/Spidyxuniverse0'),
            ('Study Group', 'https://t.me/+m2kdPw7UkI8yODM1'),
            ('Squid Study', 'https://squidstudy.eu.org'),
            ('GATE ESE 27', 'https://t.me/Gate_ese27'),
            ('GATE Prep Zone', 'https://t.me/GATEPrepZone'),
            ('Engineering Waala', 'https://t.me/EngineeringWaala'),
            ('VD List', 'https://t.me/addlist/VD_Og7nrSINmZGFl'),
            ('PW Jarvis', 'https://pwjarvis.com')
        ]
    }
}

user_stats = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id not in user_stats:
        user_stats[user_id] = {'views': 0, 'branches_accessed': []}
    
    keyboard = [[InlineKeyboardButton("✅ I Agree & Continue", callback_data='agree')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(DISCLAIMER, reply_markup=reply_markup, parse_mode='Markdown')

async def agree_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("🖥️ CSE", callback_data='branch_cse')],
        [InlineKeyboardButton("📡 ECE", callback_data='branch_ece')],
        [InlineKeyboardButton("⚡ EE", callback_data='branch_ee')],
        [InlineKeyboardButton("🔧 ME", callback_data='branch_me')],
        [InlineKeyboardButton("🏗️ Civil", callback_data='branch_civil')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="📚 **Select Your Engineering Branch:**",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def branch_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    branch_key = query.data.split('_')[1]
    user_id = query.from_user.id
    
    if user_id in user_stats:
        user_stats[user_id]['views'] += 1
        if branch_key not in user_stats[user_id]['branches_accessed']:
            user_stats[user_id]['branches_accessed'].append(branch_key)
    
    ad_message = f"""
📢 **ADVERTISEMENT**

Check out amazing resources and earn rewards!

🔗 [Click Here for Exclusive Offers]({ADSTERRA_LINK})

After viewing the ad, click below to access your study materials.
"""
    
    keyboard = [
        [InlineKeyboardButton("📖 View Study Links", callback_data=f'links_{branch_key}')],
        [InlineKeyboardButton("🔙 Back to Branches", callback_data='agree')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=ad_message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def links_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    branch_key = query.data.split('_')[1]
    branch = BRANCHES[branch_key]
    
    links_text = f"🎓 **{branch['name']} Resources:**\n\n"
    for name, url in branch['links']:
        links_text += f"📌 [{name}]({url})\n"
    
    links_text += "\n\n💡 *All links are to publicly available resources on Telegram and other platforms.*"
    
    keyboard = [
        [InlineKeyboardButton("🔙 Back to Branches", callback_data='agree')],
        [InlineKeyboardButton("📞 Contact Admin", callback_data='contact')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=links_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def contact_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    contact_text = f"""
📞 **Contact Information**

For copyright issues, content removal requests, or inquiries:

👤 **Admin ID:** `{ADMIN_ID}`

Please DM the admin with your concern and it will be addressed immediately.

We respect all intellectual property rights and comply with DMCA regulations.
"""
    
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='agree')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=contact_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = """
🤖 **Engineering Links Bot Help**

**Commands:**
/start - Start the bot and view disclaimer
/help - Show this help message
/stats - View your statistics (admin only)

**Features:**
✅ Browse resources by engineering branch
✅ Access curated study links
✅ Join community channels
✅ Monetized with ethical ads

**Branches Available:**
🖥️ CSE - Computer Science Engineering
📡 ECE - Electronics & Communication Engineering
⚡ EE - Electrical Engineering
🔧 ME - Mechanical Engineering
🏗️ Civil - Civil Engineering

**Disclaimer:**
We do not host pirated content. All links are to publicly available resources. All rights belong to respective institutes and content owners.

For copyright concerns, contact the admin immediately.
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ Unauthorized. Only admin can view stats.")
        return
    
    total_users = len(user_stats)
    total_views = sum(stats['views'] for stats in user_stats.values())
    
    stats_text = f"""
📊 **Bot Statistics**

👥 Total Users: {total_users}
👁️ Total Views: {total_views}

**Branch Access Count:**
"""
    
    branch_counts = {}
    for stats in user_stats.values():
        for branch in stats['branches_accessed']:
            branch_counts[branch] = branch_counts.get(branch, 0) + 1
    
    for branch, count in sorted(branch_counts.items(), key=lambda x: x[1], reverse=True):
        branch_name = BRANCHES[branch]['name']
        stats_text += f"\n{branch.upper()}: {count}"
    
    await update.message.reply_text(stats_text, parse_mode='Markdown')

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CallbackQueryHandler(agree_callback, pattern='^agree$'))
    application.add_handler(CallbackQueryHandler(branch_callback, pattern='^branch_'))
    application.add_handler(CallbackQueryHandler(links_callback, pattern='^links_'))
    application.add_handler(CallbackQueryHandler(contact_callback, pattern='^contact$'))
    
    application.run_polling()

if __name__ == '__main__':
    main()
