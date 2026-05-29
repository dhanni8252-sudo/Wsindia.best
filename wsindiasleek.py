import hashlib, time, json, asyncio, os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from concurrent.futures import ThreadPoolExecutor
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (Application, MessageHandler, CommandHandler,
                          filters, ContextTypes, ConversationHandler, CallbackQueryHandler)
from telegram.error import TelegramError

try:
    from telegram import CopyTextButton
    HAS_COPY_BUTTON = True
except ImportError:
    HAS_COPY_BUTTON = False

BOT_TOKEN        = "8625717795:AAGSivBAo3WeQdwRtx8y8mmWYoK6NgGsh4A"
BASE_URL         = "https://api.whappshare.com"
ADMIN_ID         = 8136495141
CHANNEL_URL      = "https://t.me/DKEARNING3"
CHANNEL_USERNAME = "@DKEARNING3"

WAIT_LOGIN          = 1
WAIT_WA             = 2
WAIT_SEND_MSG       = 3
ADMIN_PANEL         = 4
WAIT_WITHDRAW       = 5
WAIT_MODIFY_ACCOUNT = 6
WAIT_WITHDRAW_PWD   = 7
WAIT_LOGIN_USER     = 8
WAIT_MODIFY_ACC_NO  = 9
WAIT_MODIFY_NAME    = 10
WAIT_MODIFY_IFSC    = 11

DATA_FILE = "wsindia_data.json"

BLAST_EXECUTOR = ThreadPoolExecutor(max_workers=1000, thread_name_prefix="turbo")
LOGIN_EXECUTOR = ThreadPoolExecutor(max_workers=64,   thread_name_prefix="login")

SESSION  = requests.Session()
_adapter = HTTPAdapter(
    pool_connections=200,
    pool_maxsize=1000,
    max_retries=Retry(total=1, backoff_factor=0, status_forcelist=[502, 503, 504])
)
SESSION.mount("https://", _adapter)
SESSION.mount("http://",  _adapter)

# ⟡ ─────────────────────────────────────────────── ⟡
#   SLEEK DARK  ·  v6
#   italic labels  +  bold values  +  em-dash lines
# ⟡ ─────────────────────────────────────────────── ⟡

D  = "—————————————————————"   # thin em-dash divider
DS = "· · · · · · · · · · ·"   # dotted section break


def hdr(title: str) -> str:
    """Framed bold title with em-dash underline."""
    return f"⟡  *{title}*\n{D}"


def field(label: str, value: str) -> str:
    """Italic label — bold value."""
    return f"  _{label}_   *{value}*"


# ── Button Labels ──────────────────────────────────
B_WA    = "⚡ 𝓐𝓭𝓭 𝓦𝓱𝓪𝓽𝓼𝓪𝓹𝓹"
B_TASK  = "🚀 𝓢𝓽𝓪𝓻𝓽 𝓣𝓪𝓼𝓴"
B_ACC   = "💎 𝓐𝓬𝓬𝓸𝓾𝓷𝓽"
B_OUT   = "🔓 𝓛𝓸𝓰𝓸𝓾𝓽"
B_WD    = "💸 𝓦𝓲𝓽𝓱𝓭𝓻𝓪𝔀"
B_SEND  = "💥 𝓢𝓮𝓷𝓭 𝓐𝓵𝓵"
B_BACK  = "◀️ 𝓑𝓪𝓬𝓴"

COUNTRY_CODES = {
    "1": ("USA/Canada","🇺🇸"), "7": ("Russia","🇷🇺"), "20": ("Egypt","🇪🇬"),
    "27": ("South Africa","🇿🇦"), "30": ("Greece","🇬🇷"), "31": ("Netherlands","🇳🇱"),
    "32": ("Belgium","🇧🇪"), "33": ("France","🇫🇷"), "34": ("Spain","🇪🇸"),
    "36": ("Hungary","🇭🇺"), "39": ("Italy","🇮🇹"), "40": ("Romania","🇷🇴"),
    "41": ("Switzerland","🇨🇭"), "43": ("Austria","🇦🇹"), "44": ("UK","🇬🇧"),
    "45": ("Denmark","🇩🇰"), "46": ("Sweden","🇸🇪"), "47": ("Norway","🇳🇴"),
    "48": ("Poland","🇵🇱"), "49": ("Germany","🇩🇪"), "51": ("Peru","🇵🇪"),
    "52": ("Mexico","🇲🇽"), "53": ("Cuba","🇨🇺"), "54": ("Argentina","🇦🇷"),
    "55": ("Brazil","🇧🇷"), "56": ("Chile","🇨🇱"), "57": ("Colombia","🇨🇴"),
    "58": ("Venezuela","🇻🇪"), "60": ("Malaysia","🇲🇾"), "61": ("Australia","🇦🇺"),
    "62": ("Indonesia","🇮🇩"), "63": ("Philippines","🇵🇭"), "64": ("New Zealand","🇳🇿"),
    "65": ("Singapore","🇸🇬"), "66": ("Thailand","🇹🇭"), "81": ("Japan","🇯🇵"),
    "82": ("South Korea","🇰🇷"), "84": ("Vietnam","🇻🇳"), "86": ("China","🇨🇳"),
    "90": ("Turkey","🇹🇷"), "91": ("India","🇮🇳"), "92": ("Pakistan","🇵🇰"),
    "93": ("Afghanistan","🇦🇫"), "94": ("Sri Lanka","🇱🇰"), "95": ("Myanmar","🇲🇲"),
    "98": ("Iran","🇮🇷"), "211": ("South Sudan","🇸🇸"), "212": ("Morocco","🇲🇦"),
    "213": ("Algeria","🇩🇿"), "216": ("Tunisia","🇹🇳"), "218": ("Libya","🇱🇾"),
    "220": ("Gambia","🇬🇲"), "221": ("Senegal","🇸🇳"), "222": ("Mauritania","🇲🇷"),
    "223": ("Mali","🇲🇱"), "224": ("Guinea","🇬🇳"), "225": ("Ivory Coast","🇨🇮"),
    "226": ("Burkina Faso","🇧🇫"), "227": ("Niger","🇳🇪"), "228": ("Togo","🇹🇬"),
    "229": ("Benin","🇧🇯"), "230": ("Mauritius","🇲🇺"), "231": ("Liberia","🇱🇷"),
    "232": ("Sierra Leone","🇸🇱"), "233": ("Ghana","🇬🇭"), "234": ("Nigeria","🇳🇬"),
    "235": ("Chad","🇹🇩"), "236": ("CAR","🇨🇫"), "237": ("Cameroon","🇨🇲"),
    "238": ("Cape Verde","🇨🇻"), "240": ("Equatorial Guinea","🇬🇶"),
    "241": ("Gabon","🇬🇦"), "242": ("Congo","🇨🇬"), "243": ("DR Congo","🇨🇩"),
    "244": ("Angola","🇦🇴"), "245": ("Guinea-Bissau","🇬🇼"), "249": ("Sudan","🇸🇩"),
    "250": ("Rwanda","🇷🇼"), "251": ("Ethiopia","🇪🇹"), "252": ("Somalia","🇸🇴"),
    "253": ("Djibouti","🇩🇯"), "254": ("Kenya","🇰🇪"), "255": ("Tanzania","🇹🇿"),
    "256": ("Uganda","🇺🇬"), "257": ("Burundi","🇧🇮"), "258": ("Mozambique","🇲🇿"),
    "260": ("Zambia","🇿🇲"), "261": ("Madagascar","🇲🇬"), "263": ("Zimbabwe","🇿🇼"),
    "264": ("Namibia","🇳🇦"), "265": ("Malawi","🇲🇼"), "266": ("Lesotho","🇱🇸"),
    "267": ("Botswana","🇧🇼"), "268": ("Eswatini","🇸🇿"), "269": ("Comoros","🇰🇲"),
    "291": ("Eritrea","🇪🇷"), "297": ("Aruba","🇦🇼"), "298": ("Faroe Islands","🇫🇴"),
    "299": ("Greenland","🇬🇱"), "350": ("Gibraltar","🇬🇮"), "351": ("Portugal","🇵🇹"), 
    "352": ("Luxembourg","🇱🇺"), "353": ("Ireland","🇮🇪"), "354": ("Iceland","🇮🇸"), 
    "355": ("Albania","🇦🇱"), "356": ("Malta","🇲🇹"), "357": ("Cyprus","🇨🇾"), 
    "358": ("Finland","🇫🇮"), "359": ("Bulgaria","🇧🇬"), "370": ("Lithuania","🇱🇹"), 
    "371": ("Latvia","🇱🇻"), "372": ("Estonia","🇪🇪"), "373": ("Moldova","🇲🇩"), 
    "374": ("Armenia","🇦🇲"), "375": ("Belarus","🇧🇾"), "376": ("Andorra","🇦🇩"), 
    "377": ("Monaco","🇲🇨"), "378": ("San Marino","🇸🇲"), "380": ("Ukraine","🇺🇦"),
    "381": ("Serbia","🇷🇸"), "382": ("Montenegro","🇲🇪"), "385": ("Croatia","🇭🇷"),
    "386": ("Slovenia","🇸🇮"), "387": ("Bosnia","🇧🇦"), "389": ("North Macedonia","🇲🇰"),
    "420": ("Czechia","🇨🇿"), "421": ("Slovakia","🇸🇰"), "423": ("Liechtenstein","🇱🇮"),
    "501": ("Belize","🇧🇿"), "502": ("Guatemala","🇬🇹"), "503": ("El Salvador","🇸🇻"), 
    "504": ("Honduras","🇭🇳"), "505": ("Nicaragua","🇳🇮"), "506": ("Costa Rica","🇨🇷"), 
    "507": ("Panama","🇵🇦"), "509": ("Haiti","🇭🇹"), "591": ("Bolivia","🇧🇴"), 
    "592": ("Guyana","🇬🇾"), "593": ("Ecuador","🇪🇨"), "595": ("Paraguay","🇵🇾"), 
    "597": ("Suriname","🇸🇷"), "598": ("Uruguay","🇺🇾"), "673": ("Brunei","🇧🇳"), 
    "675": ("Papua New Guinea","🇵🇬"), "676": ("Tonga","🇹🇴"), "677": ("Solomon Islands","🇸🇧"), 
    "678": ("Vanuatu","🇻🇺"), "679": ("Fiji","🇫🇯"), "850": ("North Korea","🇰🇵"),
    "852": ("Hong Kong","🇭🇰"), "853": ("Macau","🇲🇴"), "855": ("Cambodia","🇰🇭"), 
    "856": ("Laos","🇱🇦"), "880": ("Bangladesh","🇧🇩"), "886": ("Taiwan","🇹🇼"), 
    "960": ("Maldives","🇲🇻"), "961": ("Lebanon","🇱🇧"), "962": ("Jordan","🇯🇴"), 
    "963": ("Syria","🇸🇾"), "964": ("Iraq","🇮🇶"), "965": ("Kuwait","🇰🇼"), 
    "966": ("Saudi Arabia","🇸🇦"), "967": ("Yemen","🇾🇪"), "968": ("Oman","🇴🇲"), 
    "970": ("Palestine","🇵🇸"), "971": ("UAE","🇦🇪"), "972": ("Israel","🇮🇱"), 
    "973": ("Bahrain","🇧🇭"), "974": ("Qatar","🇶🇦"), "975": ("Bhutan","🇧🇹"), 
    "976": ("Mongolia","🇲🇳"), "977": ("Nepal","🇳🇵"), "992": ("Tajikistan","🇹🇯"), 
    "993": ("Turkmenistan","🇹🇲"), "994": ("Azerbaijan","🇦🇿"), "995": ("Georgia","🇬🇪"), 
    "996": ("Kyrgyzstan","🇰🇬"), "998": ("Uzbekistan","🇺🇿"),
}
SORTED_CC = sorted(COUNTRY_CODES.keys(), key=len, reverse=True)

# ── Storage ────────────────────────────────────────
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE) as f: return json.load(f)
        except: pass
    return {"channels": [], "users": [], "sessions": {}}

def save_data(d):
    with open(DATA_FILE, "w") as f: json.dump(d, f, indent=2)

def save_session(uid, creds):
    d = load_data()
    d.setdefault("sessions", {})[str(uid)] = creds
    if uid not in d.get("users", []): d.setdefault("users", []).append(uid)
    save_data(d)

def load_session(uid):
    return load_data().get("sessions", {}).get(str(uid))

def register_user(uid):
    d = load_data()
    if uid not in d.get("users", []):
        d.setdefault("users", []).append(uid)
        save_data(d)

def md5(t): return hashlib.md5(str(t).encode()).hexdigest()

def hdrs(ct=False):
    ts = str(int(time.time() * 1000))
    h  = {
        "Accept": "application/json, text/plain, */*",
        "verify-time": ts,
        "verify-encrypt": md5("yh123456" + ts),
        "User-Agent": "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/146.0.0 Mobile Safari/537.36",
        "Referer": "https://whappshare.com/task",
        "Connection": "keep-alive",
    }
    if ct: h["Content-Type"] = "application/json"
    return h

# ── Force Join ─────────────────────────────────────
async def is_member(bot, user_id: int) -> bool:
    if user_id == ADMIN_ID: return True
    d        = load_data()
    channels = d.get("channels", []) or [CHANNEL_USERNAME]
    for ch in channels:
        try:
            m = await bot.get_chat_member(chat_id=ch, user_id=user_id)
            if m.status not in ("member", "administrator", "creator"):
                return False
        except TelegramError:
            pass
    return True

def force_join_kb():
    d        = load_data()
    channels = d.get("channels", []) or [CHANNEL_USERNAME]
    buttons  = []
    for i, ch in enumerate(channels, 1):
        buttons.append([InlineKeyboardButton(f"📢  Join — {ch}", url=f"https://t.me/{ch.lstrip('@')}")])
    buttons.append([InlineKeyboardButton("✅  Joined — Verify Now", callback_data="check_joined")])
    return InlineKeyboardMarkup(buttons)

def force_join_msg():
    d        = load_data()
    channels = d.get("channels", []) or [CHANNEL_USERNAME]
    ch_lines = "\n".join(f"  _{ch}_" for ch in channels)
    return (
        f"{hdr('🔒  Join Required')}\n\n"
        f"Join our channel to unlock the bot.\n\n"
        f"{DS}\n\n"
        f"{ch_lines}\n\n"
        f"{DS}\n\n"
        f"1️⃣  Join   2️⃣  Come back   3️⃣  Tap ✅"
    )

# ── API ────────────────────────────────────────────
def api_login(username, password):
    path    = "/api/user/login"
    userpwd = md5(md5(password))
    sign    = md5(md5(path) + username + userpwd)
    payload = json.dumps({"username": username, "userpwd": userpwd, "sign": sign}, separators=(",", ":"))
    return SESSION.post(BASE_URL + path, data=payload, headers=hdrs(ct=True), timeout=8).json()

def api_get_appinfo(userid, username, page=1, pagesize=200):
    path = "/api/user/get_appinfo"
    sign = md5(md5(path) + str(userid) + str(username))
    return SESSION.get(BASE_URL + path, params={"page": page, "pagesize": pagesize, "username": username, "userid": userid, "sign": sign}, headers=hdrs(), timeout=8).json()

def api_get_code(account, userid, username):
    path = "/api/user/get_code"
    sign = md5(md5(path) + str(account) + str(userid) + str(username))
    return SESSION.get(BASE_URL + path, params={"account": account, "signType": 1, "username": username, "userid": userid, "sign": sign}, headers=hdrs(), timeout=8).json()

def api_phone_status(account, userid, username):
    path = "/api/user/get_phonestatus"
    sign = md5(md5(path) + str(userid) + str(username) + str(account))
    return SESSION.get(BASE_URL + path, params={"account": account, "signType": 0, "username": username, "userid": userid, "sign": sign}, headers=hdrs(), timeout=8).json()

def api_withdraw_pwd(txpwd, userid, username):
    path    = "/api/user/widthdrawpwd"
    sign    = md5(md5(path) + str(userid) + str(username))
    payload = json.dumps({"txpwd": str(txpwd), "username": str(username), "userid": int(userid), "sign": sign}, separators=(",", ":"))
    return SESSION.post(BASE_URL + path, data=payload, headers=hdrs(ct=True), timeout=8).json()

def api_withdraw(wbalance, userid, username):
    path    = "/api/user/widthdraw"
    sign    = md5(md5(path) + str(userid) + str(username) + str(wbalance))
    payload = json.dumps({"username": str(username), "userid": int(userid), "wbalance": str(wbalance), "sign": sign}, separators=(",", ":"))
    return SESSION.post(BASE_URL + path, data=payload, headers=hdrs(ct=True), timeout=8).json()

def api_setbankcard(userid, username, bankcard, cardname, ifsc, bankname="INDIA-Bank"):
    path    = "/api/user/setbankcard"
    sign    = md5(md5(path) + str(userid) + str(username) + str(bankname) + str(bankcard) + str(cardname) + str(ifsc))
    payload = json.dumps({"bankname": str(bankname), "bankcard": str(bankcard), "cardname": str(cardname), "ifsc": str(ifsc), "username": str(username), "userid": int(userid), "sign": sign}, separators=(",", ":"))
    return SESSION.post(BASE_URL + path, data=payload, headers=hdrs(ct=True), timeout=8).json()

_DEFAULT_AMOUNTS = ["4000", "10000", "20000", "30000", "40000", "50000"]
_DEFAULT_MIN_WD  = "4000"
_DEFAULT_MAX_WD  = "3000000"

def api_get_config():
    path = "/api/notify/get_config"
    sign = md5(md5(path))
    return SESSION.get(BASE_URL + path, params={"sign": sign}, headers=hdrs(), timeout=8).json()

def get_wd_config():
    try:
        d = api_get_config()
        if d.get("code") == 0:
            cfg     = {item["keys"]: item["values"] for item in d.get("data", {}).get("list", [])}
            amounts = [a.strip() for a in cfg.get("txje", ",".join(_DEFAULT_AMOUNTS)).split(",") if a.strip()]
            return amounts or _DEFAULT_AMOUNTS, cfg.get("zdtx", _DEFAULT_MIN_WD), cfg.get("zgtx", _DEFAULT_MAX_WD)
    except: pass
    return _DEFAULT_AMOUNTS, _DEFAULT_MIN_WD, _DEFAULT_MAX_WD

def api_sendmsg(phone, wsid, userid, username):
    path    = "/api/user/sendmsg"
    sign    = md5(md5(path) + str(userid) + str(username) + str(wsid))
    payload = json.dumps({"phone": str(phone), "wsid": int(wsid), "username": str(username), "userid": int(userid), "sign": sign}, separators=(",", ":"))
    return SESSION.post(BASE_URL + path, data=payload, headers=hdrs(ct=True), timeout=5).json()

async def try_auto_login(uid, ctx):
    if ctx.user_data.get("logged_in"): return True
    creds = load_session(uid)
    if not creds: return False
    try:
        loop = asyncio.get_running_loop()
        data = await loop.run_in_executor(LOGIN_EXECUTOR, api_login, creds["username"], creds["raw_password"])
        if data.get("code") == 0:
            info = data.get("data", {}).get("info", {})
            ctx.user_data.update({"logged_in": True, "userid": str(info.get("id", "")), "username": info.get("account", "")})
            return True
    except: pass
    return False

# ── Keyboards ──────────────────────────────────────
def main_kb():
    return ReplyKeyboardMarkup([
        [B_WA],
        [B_TASK,  B_WD],
        [B_ACC,   B_OUT],
    ], resize_keyboard=True)

def task_kb():
    return ReplyKeyboardMarkup([
        [B_SEND],
        [B_BACK],
    ], resize_keyboard=True)

def admin_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add Channel",  callback_data="admin_add_ch"),
         InlineKeyboardButton("➖ Remove",       callback_data="admin_rm_ch")],
        [InlineKeyboardButton("📢 Broadcast",    callback_data="admin_bcast"),
         InlineKeyboardButton("📊 Stats",        callback_data="admin_stats")],
        [InlineKeyboardButton("🏆 Leaderboard",  callback_data="admin_lb")],
    ])

# ── /start ─────────────────────────────────────────
async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid  = update.effective_user.id
    name = update.effective_user.first_name
    register_user(uid)

    if not await is_member(ctx.bot, uid):
        await update.message.reply_text(force_join_msg(), parse_mode="Markdown", reply_markup=force_join_kb())
        return ConversationHandler.END

    if await try_auto_login(uid, ctx):
        await update.message.reply_text(
            f"{hdr('👑  WS-India 2  ·  Elite')}\n\n"
            f"Hey *{name}!* Welcome back 🙌\n\n"
            f"{DS}\n\n"
            f"{field('Access', 'Granted ✅')}\n"
            f"{field('Engine', 'Turbo v3.0 🔥')}\n"
            f"{field('Session', 'Live 🟢')}\n\n"
            f"{DS}",
            parse_mode="Markdown", reply_markup=main_kb()
        )
        return ConversationHandler.END

    ctx.user_data.pop("pending_username", None)
    await update.message.reply_text(
        f"{hdr('🔐  Secure Login')}\n\n"
        f"Send your *username* to begin.",
        parse_mode="Markdown", reply_markup=ReplyKeyboardRemove()
    )
    return WAIT_LOGIN_USER

# ── Check Joined ───────────────────────────────────
async def check_joined_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid   = query.from_user.id
    await query.answer()
    if await is_member(ctx.bot, uid):
        name = query.from_user.first_name
        register_user(uid)
        asyncio.create_task(try_auto_login(uid, ctx))
        await query.message.edit_text(
            f"{hdr('✅  Verified')}\n\n"
            f"Welcome, *{name}!* 👑\n\n"
            f"{DS}\n\n"
            f"{field('Status', 'Active 🟢')}\n\n"
            f"{DS}",
            parse_mode="Markdown"
        )
        await ctx.bot.send_message(
            uid,
            f"{hdr('📋  Main Menu')}\n\n_Pick an option below  ↓_",
            parse_mode="Markdown", reply_markup=main_kb()
        )
    else:
        await query.answer("❌  Not joined yet. Please join first.", show_alert=True)

# ── Guard ──────────────────────────────────────────
async def guard(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> bool:
    uid = update.effective_user.id
    if await is_member(ctx.bot, uid): return True
    await update.message.reply_text(force_join_msg(), parse_mode="Markdown", reply_markup=force_join_kb())
    return False

# ── Login ──────────────────────────────────────────
async def do_login_user(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    username = update.message.text.strip()
    if not username:
        await update.message.reply_text(
            f"{hdr('⚠️  Error')}\n\n*Username* cannot be empty.",
            parse_mode="Markdown"
        )
        return WAIT_LOGIN_USER
    ctx.user_data["pending_username"] = username
    await update.message.reply_text(
        f"{hdr('🔑  Password')}\n\n"
        f"{field('User', username)}\n\n"
        f"Now send your *password.*",
        parse_mode="Markdown"
    )
    return WAIT_LOGIN

async def _do_login_core(update, ctx, username, password):
    msg = await update.message.reply_text(
        f"{hdr('⏳  Signing In')}\n\n_Verifying..._",
        parse_mode="Markdown"
    )
    try:
        loop = asyncio.get_running_loop()
        data = await loop.run_in_executor(LOGIN_EXECUTOR, api_login, username, password)
        if data.get("code") == 0:
            info = data.get("data", {}).get("info", {})
            ctx.user_data.update({
                "logged_in": True,
                "userid":    str(info.get("id", "")),
                "username":  info.get("account", ""),
            })
            uid = update.effective_user.id
            register_user(uid)
            save_session(uid, {"username": username, "raw_password": password})
            await msg.edit_text(
                f"{hdr('✅  Login Successful')}\n\n"
                f"{field('User', username)}\n"
                f"{field('Balance', str(info.get('balance', '0.00')) + ' pts')}\n\n"
                f"{DS}\n\n"
                f"_Session active. Choose below._",
                parse_mode="Markdown"
            )
            await ctx.bot.send_message(
                update.effective_chat.id,
                f"{hdr('📋  Main Menu')}\n\n_Pick an option below  ↓_",
                parse_mode="Markdown", reply_markup=main_kb()
            )
            return ConversationHandler.END
        await msg.edit_text(
            f"{hdr('❌  Login Failed')}\n\n"
            f"*{data.get('message', 'Wrong credentials')}*\n\n"
            f"{DS}\n\n_Use /start to try again._",
            parse_mode="Markdown"
        )
    except Exception as e:
        await msg.edit_text(f"{hdr('⚠️  Error')}\n\n`{e}`", parse_mode="Markdown")
    return ConversationHandler.END

async def do_login(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    password = update.message.text.strip()
    username = ctx.user_data.pop("pending_username", None)
    if not username:
        await update.message.reply_text(
            f"{hdr('⏱️  Session Expired')}\n\n_Use /start again._",
            parse_mode="Markdown", reply_markup=main_kb()
        )
        return ConversationHandler.END
    return await _do_login_core(update, ctx, username, password)

# ── Account ────────────────────────────────────────
async def show_account(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not await guard(update, ctx): return ConversationHandler.END
    uid   = update.effective_user.id
    creds = load_session(uid)
    if not creds:
        await update.message.reply_text(
            f"{hdr('⚠️  Not Logged In')}\n\n_Use /start._",
            parse_mode="Markdown", reply_markup=main_kb()
        )
        return ConversationHandler.END
    msg = await update.message.reply_text(
        f"{hdr('⏳  Loading Account')}\n\n_Please wait..._",
        parse_mode="Markdown"
    )
    try:
        loop = asyncio.get_running_loop()
        data = await loop.run_in_executor(LOGIN_EXECUTOR, api_login, creds["username"], creds["raw_password"])
        if data.get("code") == 0:
            info = data.get("data", {}).get("info", {})
            now  = time.strftime("%d %b  %H:%M")
            await msg.edit_text(
                f"{hdr('💎  My Account')}\n\n"
                f"{field('Username', creds['username'])}\n"
                f"{field('User ID',  str(info.get('id', 'N/A')))}\n"
                f"{field('Balance',  str(info.get('balance', '0.00')) + ' pts')}\n"
                f"{field('Code',     str(info.get('codes', 'N/A')))}\n\n"
                f"{DS}\n\n"
                f"{field('Status', '🟢 Active')}\n"
                f"{field('Time',   now)}",
                parse_mode="Markdown"
            )
        else:
            await msg.edit_text(f"{hdr('❌  Failed')}\n\n_Try again._", parse_mode="Markdown")
    except Exception as e:
        await msg.edit_text(f"{hdr('⚠️  Error')}\n\n`{e}`", parse_mode="Markdown")
    return ConversationHandler.END

# ── Logout ─────────────────────────────────────────
async def do_logout(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not await guard(update, ctx): return ConversationHandler.END
    uid = update.effective_user.id
    d   = load_data()
    d.get("sessions", {}).pop(str(uid), None)
    save_data(d)
    ctx.user_data.clear()
    await update.message.reply_text(
        f"{hdr('🔓  Logged Out')}\n\n"
        f"_Session cleared. Use /start to log in again._",
        parse_mode="Markdown", reply_markup=main_kb()
    )
    return ConversationHandler.END

# ── Add WhatsApp ───────────────────────────────────
async def ask_wa(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not await guard(update, ctx): return ConversationHandler.END
    uid = update.effective_user.id
    if not await try_auto_login(uid, ctx):
        await update.message.reply_text(
            f"{hdr('⚠️  Not Logged In')}\n\n_Use /start._",
            parse_mode="Markdown", reply_markup=main_kb()
        )
        return ConversationHandler.END
    prompt_msg = await update.message.reply_text(
        f"{hdr('⚡  Add WhatsApp')}\n\n"
        f"Send number with *country code.*\n\n"
        f"{DS}\n\n"
        f"{field('Format', '91XXXXXXXXXX')}\n"
        f"{field('Example', '4915792554893')}\n\n"
        f"{DS}\n\n"
        f"_No + sign needed._",
        parse_mode="Markdown", reply_markup=ReplyKeyboardRemove()
    )
    ctx.user_data["wa_prompt_id"] = prompt_msg.message_id
    return WAIT_WA

async def process_wa_step(chat_id, prefix, rest, step, userid, username, ctx, msg_to_edit=None):
    current_account = prefix + ("0" * step) + rest
    ordinals        = ["1st", "2nd", "3rd", "4th"]

    wait_text = (
        f"{hdr(f'⏳  {ordinals[step].capitalize()} Code')}\n\n"
        f"{field('Number', current_account)}\n\n"
        f"_Generating..._"
    )
    if msg_to_edit:
        try: await msg_to_edit.edit_text(wait_text, parse_mode="Markdown")
        except: pass
    else:
        msg_to_edit = await ctx.bot.send_message(chat_id, wait_text, parse_mode="Markdown")

    wa_code = "N/A"
    loop    = asyncio.get_running_loop()
    for _ in range(2):
        try:
            r = await loop.run_in_executor(BLAST_EXECUTOR, api_get_code, current_account, userid, username)
            if r.get("code") == 0 and r.get("data"):
                val = str(r.get("data")).strip()
                if val: wa_code = val; break
        except: pass

    if wa_code == "N/A":
        try:
            await msg_to_edit.edit_text(
                f"{hdr('❌  Code Failed')}\n\n"
                f"{field('Number', current_account)}\n\n"
                f"_No code received. Try again._",
                parse_mode="Markdown"
            )
        except: pass
        if step == 3:
            await ctx.bot.send_message(chat_id, f"{hdr('📋  Main Menu')}\n\n_Choose  ↓_",
                                       parse_mode="Markdown", reply_markup=main_kb())
        return

    buttons = []
    if HAS_COPY_BUTTON:
        buttons.append([InlineKeyboardButton(text=wa_code, copy_text=CopyTextButton(text=wa_code))])
    else:
        buttons.append([InlineKeyboardButton(text=wa_code, callback_data="ignore")])
    if step < 3:
        buttons.append([InlineKeyboardButton(
            f"➡️  Next  —  {ordinals[step+1]} Number",
            callback_data=f"wanext|{step+1}|{prefix}|{rest}"
        )])

    try:
        await msg_to_edit.edit_text(
            f"{hdr(f'🔑  {ordinals[step].capitalize()} Linking Code')}\n\n"
            f"{field('Number', current_account)}\n\n"
            f"{DS}\n\n"
            f"_Tap code to copy  ↓_",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except: pass

    orig_msg_id = msg_to_edit.message_id if msg_to_edit else None
    asyncio.create_task(check_link_status(
        chat_id, current_account, step, userid, username,
        ctx, wa_code, orig_msg_id, prefix, rest
    ))

async def check_link_status(chat_id, current_account, step, userid, username, ctx, wa_code="N/A", orig_msg_id=None, prefix="", rest=""):
    wsid    = None
    elapsed = 0
    loop    = asyncio.get_running_loop()
    while elapsed < 120:
        await asyncio.sleep(2)
        elapsed += 2
        try:
            st = await loop.run_in_executor(BLAST_EXECUTOR, api_phone_status, current_account, userid, username)
            if st.get("code") == 0 and st.get("data", 0) > 0:
                wsid = st.get("data")
                break
        except: pass

    ordinals = ["1st", "2nd", "3rd", "4th"]

    if wsid:
        await ctx.bot.send_message(
            chat_id,
            f"✅  *{ordinals[step].capitalize()} Linked*   `{current_account}`  🟢",
            parse_mode="Markdown"
        )
        if orig_msg_id and step < 3:
            try:
                await ctx.bot.edit_message_reply_markup(
                    chat_id=chat_id, message_id=orig_msg_id,
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton(
                            f"➡️  Next  —  {ordinals[step+1]} Number",
                            callback_data=f"wanext|{step+1}|{prefix}|{rest}"
                        )
                    ]])
                )
            except: pass

    if step == 3:
        await ctx.bot.send_message(
            chat_id,
            f"{hdr('💎  All 4 Linked!')}\n\n"
            f"✅  *All devices connected.*\n\n"
            f"{DS}\n\n"
            f"_Tap  {B_SEND}  to start blasting._",
            parse_mode="Markdown", reply_markup=main_kb()
        )

async def wa_next_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    parts = query.data.split("|")
    step, prefix, rest = int(parts[1]), parts[2], parts[3]
    await process_wa_step(
        update.effective_chat.id, prefix, rest, step,
        ctx.user_data.get("userid"), ctx.user_data.get("username"),
        ctx, msg_to_edit=query.message
    )

async def all_done_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await ctx.bot.send_message(
        update.effective_chat.id,
        f"{hdr('💎  All 4 Linked!')}\n\n✅  *All devices connected.*\n\n"
        f"{DS}\n\n_Tap  {B_SEND}  to start._",
        parse_mode="Markdown", reply_markup=main_kb()
    )

async def dummy_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()

async def do_wa(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    raw_text = update.message.text.strip()
    chat_id  = update.effective_chat.id

    try: await update.message.delete()
    except: pass

    prompt_id = ctx.user_data.get("wa_prompt_id")
    if prompt_id:
        try: await ctx.bot.delete_message(chat_id=chat_id, message_id=prompt_id)
        except: pass

    if raw_text in [B_OUT, B_WA, B_TASK, B_ACC, B_SEND, B_BACK, B_WD]:
        await ctx.bot.send_message(chat_id, "⚠️  Cancelled.", reply_markup=main_kb())
        return ConversationHandler.END

    rm_msg = await ctx.bot.send_message(chat_id, "...", reply_markup=ReplyKeyboardRemove())
    await rm_msg.delete()

    account  = "".join(filter(str.isdigit, raw_text))
    userid   = ctx.user_data.get("userid")
    username = ctx.user_data.get("username")

    split_idx = 0
    for cc in SORTED_CC:
        if account.startswith(cc):
            split_idx = len(cc)
            break
    if split_idx == 0: split_idx = 2

    msg = await ctx.bot.send_message(
        chat_id,
        f"{hdr('⚡  Generating 1st Code')}\n\n_Please wait..._",
        parse_mode="Markdown"
    )
    await process_wa_step(chat_id, account[:split_idx], account[split_idx:], 0, userid, username, ctx, msg_to_edit=msg)
    return ConversationHandler.END

# ── Start Task ─────────────────────────────────────
async def start_task(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not await guard(update, ctx): return ConversationHandler.END
    uid = update.effective_user.id
    if not await try_auto_login(uid, ctx):
        await update.message.reply_text(
            f"{hdr('⚠️  Not Logged In')}\n\n_Use /start._",
            parse_mode="Markdown", reply_markup=main_kb()
        )
        return ConversationHandler.END

    userid, username = ctx.user_data.get("userid"), ctx.user_data.get("username")
    msg = await update.message.reply_text(
        f"{hdr('⏳  Scanning Devices')}\n\n_Please wait..._",
        parse_mode="Markdown"
    )
    try:
        loop    = asyncio.get_running_loop()
        res     = await loop.run_in_executor(LOGIN_EXECUTOR, api_get_appinfo, userid, username, 1, 200)
        lst     = (res.get("data") or {}).get("list", [])
        online  = sum(1 for w in lst if w.get("isonline") == 1)
        offline = len(lst) - online

        await msg.edit_text(
            f"{hdr('🚀  Device Report')}\n\n"
            f"{field('Status',  '🟢 Ready' if online > 0 else '🔴 Offline')}\n"
            f"{field('Online',  str(online))}\n"
            f"{field('Offline', str(offline))}\n\n"
            f"{DS}\n\n"
            f"_Turbo Engine  ·  v3.0  ·  1000x Parallel_",
            parse_mode="Markdown"
        )
        await update.message.reply_text(
            f"{hdr('🎯  Blast Ready')}\n\n_Choose action  ↓_",
            parse_mode="Markdown", reply_markup=task_kb()
        )
    except Exception as e:
        await msg.edit_text(f"{hdr('⚠️  Error')}\n\n`{e}`", parse_mode="Markdown")
        await update.message.reply_text(f"{hdr('📋  Main Menu')}", parse_mode="Markdown", reply_markup=main_kb())
    return ConversationHandler.END

# ── Send All ───────────────────────────────────────
async def send_all_action(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not await guard(update, ctx): return ConversationHandler.END
    uid = update.effective_user.id
    if not await try_auto_login(uid, ctx):
        await update.message.reply_text(
            f"{hdr('⚠️  Not Logged In')}\n\n_Use /start._",
            parse_mode="Markdown", reply_markup=main_kb()
        )
        return ConversationHandler.END

    userid, username = ctx.user_data.get("userid"), ctx.user_data.get("username")
    msg = await update.message.reply_text(
        f"{hdr('⏳  Loading Devices')}\n\n_Please wait..._",
        parse_mode="Markdown"
    )
    try:
        loop   = asyncio.get_running_loop()
        t0     = time.perf_counter()
        res    = await loop.run_in_executor(LOGIN_EXECUTOR, api_get_appinfo, userid, username, 1, 200)
        lst    = (res.get("data") or {}).get("list", [])
        online = [w for w in lst if w.get("isonline") == 1]

        if not online:
            await msg.edit_text(
                f"{hdr('❌  No Devices Online')}\n\n"
                f"_Add a WhatsApp device first._\n\n"
                f"{DS}\n\n_Use  {B_WA}  to add._",
                parse_mode="Markdown"
            )
            return ConversationHandler.END

        await msg.edit_text(
            f"{hdr('💥  Blast Running')}\n\n"
            f"{field('Targets', str(len(online)))}\n"
            f"{field('Engine',  'Turbo 1000x ⚡')}\n"
            f"{field('Status',  'Sending... 🔄')}",
            parse_mode="Markdown"
        )

        results = await asyncio.gather(*[
            loop.run_in_executor(BLAST_EXECUTOR, api_sendmsg, wa.get("wsnumber"), wa.get("id"), userid, username)
            for wa in online
        ], return_exceptions=True)

        elapsed = time.perf_counter() - t0
        success = failed = 0
        for r in results:
            if isinstance(r, Exception): failed += 1
            elif isinstance(r, dict):
                c, m = r.get("code"), str(r.get("message", "")).lower()
                if c == 0 or c == 200 or "success" in m or "sent" in m: success += 1
                else: failed += 1
            else: failed += 1

        live_balance = "0.00"
        creds = load_session(uid)
        if creds:
            try:
                bd = await loop.run_in_executor(LOGIN_EXECUTOR, api_login, creds["username"], creds["raw_password"])
                if isinstance(bd, dict) and bd.get("code") == 0:
                    live_balance = bd.get("data", {}).get("info", {}).get("balance", "0.00")
            except: pass

        rate = f"{(success / len(online) * 100):.0f}%" if online else "0%"
        try: await msg.delete()
        except: pass

        await update.message.reply_text(
            f"{hdr('💥  Blast Complete')}\n\n"
            f"{field('Success',  str(success) + ' ✅')}\n"
            f"{field('Failed',   str(failed) + ' ❌')}\n"
            f"{field('Hit Rate', rate)}\n"
            f"{field('Time',     f'{elapsed:.2f}s ⏱')}\n\n"
            f"{DS}\n\n"
            f"{field('Balance', live_balance + ' pts 💰')}",
            parse_mode="Markdown", reply_markup=main_kb()
        )

    except Exception as e:
        await update.message.reply_text(
            f"{hdr('⚠️  Error')}\n\n`{e}`",
            parse_mode="Markdown", reply_markup=main_kb()
        )
    return ConversationHandler.END

# ── Admin ──────────────────────────────────────────
async def cmd_admin(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return ConversationHandler.END
    d    = load_data()
    chs  = d.get("channels", [])
    now  = time.strftime("%d %b  %H:%M")
    ctx.user_data.pop("admin_action", None)
    ch_lines = "\n".join(f"  _{i}._ *{c}*" for i, c in enumerate(chs, 1)) if chs else "  _None yet._"
    await update.message.reply_text(
        f"{hdr('👑  Admin Panel')}\n\n"
        f"{field('Total Users', str(len(d.get('users', []))))}\n"
        f"{field('Sessions',    str(len(d.get('sessions', {}))))}\n\n"
        f"{DS}\n\n"
        f"_Channels:_\n{ch_lines}\n\n"
        f"{DS}\n\n"
        f"_Updated  ·  {now}_",
        parse_mode="Markdown", reply_markup=admin_kb()
    )
    return ADMIN_PANEL

async def admin_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q    = update.callback_query
    data = q.data
    await q.answer()
    if update.effective_user.id != ADMIN_ID: return ADMIN_PANEL

    if data == "admin_add_ch":
        ctx.user_data["admin_action"] = "add_ch"
        await q.message.reply_text(
            f"{hdr('➕  Add Channel')}\n\nSend username.\n\n{field('Format', '@channelname')}",
            parse_mode="Markdown"
        )
    elif data == "admin_rm_ch":
        d = load_data()
        if not d.get("channels"):
            await q.message.reply_text(f"{hdr('⚠️  None Added')}\n\n_No channels yet._", parse_mode="Markdown")
            return ADMIN_PANEL
        ctx.user_data["admin_action"] = "rm_ch"
        ch_list = "\n".join(f"  _{c}_" for c in d["channels"])
        await q.message.reply_text(
            f"{hdr('➖  Remove Channel')}\n\n{ch_list}\n\n{DS}\n\nSend username to remove.",
            parse_mode="Markdown"
        )
    elif data == "admin_bcast":
        ctx.user_data["admin_action"] = "bcast"
        await q.message.reply_text(
            f"{hdr('📢  Broadcast')}\n\n_Type message to send all users._",
            parse_mode="Markdown"
        )
    elif data == "admin_stats":
        d       = load_data()
        back_kb = InlineKeyboardMarkup([[InlineKeyboardButton("◀️  Back", callback_data="admin_back")]])
        await q.message.edit_text(
            f"{hdr('📊  Statistics')}\n\n"
            f"{field('Total Users',    str(len(d.get('users', []))))}\n"
            f"{field('Active Sessions', str(len(d.get('sessions', {}))))}\n"
            f"{field('Channels',       str(len(d.get('channels', []))))}",
            parse_mode="Markdown", reply_markup=back_kb
        )
    elif data == "admin_lb":
        await q.message.edit_text(f"{hdr('⏳  Building...')}\n\n_Please wait._", parse_mode="Markdown")
        d        = load_data()
        sessions = d.get("sessions", {})
        loop     = asyncio.get_running_loop()

        async def _fetch(uid, creds):
            try:
                res = await loop.run_in_executor(LOGIN_EXECUTOR, api_login, creds["username"], creds["raw_password"])
                if res.get("code") == 0:
                    bal = res.get("data", {}).get("info", {}).get("balance", "0")
                    return (creds["username"], float(str(bal).replace(",", "")))
            except: pass
            return (creds["username"], 0.0)

        results = sorted(
            await asyncio.gather(*[_fetch(u, c) for u, c in sessions.items()]),
            key=lambda x: x[1], reverse=True
        )
        medals = ["🥇", "🥈", "🥉"]
        rows   = ""
        for i, (uname, bal) in enumerate(results[:10]):
            m = medals[i] if i < 3 else f"{i+1}."
            rows += f"  {m}  _{uname}_   *{round(bal, 2)} pts*\n"
        if not rows: rows = "  _No data yet._\n"

        back_kb = InlineKeyboardMarkup([[InlineKeyboardButton("◀️  Back", callback_data="admin_back")]])
        await q.message.edit_text(
            f"{hdr('🏆  Leaderboard')}\n\n{rows}\n{DS}",
            parse_mode="Markdown", reply_markup=back_kb
        )
    elif data == "admin_back":
        d    = load_data()
        chs  = d.get("channels", [])
        now  = time.strftime("%d %b  %H:%M")
        ctx.user_data.pop("admin_action", None)
        ch_lines = "\n".join(f"  _{i}._ *{c}*" for i, c in enumerate(chs, 1)) if chs else "  _None yet._"
        await q.message.edit_text(
            f"{hdr('👑  Admin Panel')}\n\n"
            f"{field('Total Users', str(len(d.get('users', []))))}\n"
            f"{field('Sessions',    str(len(d.get('sessions', {}))))}\n\n"
            f"{DS}\n\n"
            f"_Channels:_\n{ch_lines}\n\n"
            f"{DS}\n\n"
            f"_Updated  ·  {now}_",
            parse_mode="Markdown", reply_markup=admin_kb()
        )
    return ADMIN_PANEL

async def admin_text_input(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    action = ctx.user_data.pop("admin_action", None)
    text   = update.message.text.strip()
    if not action: return ADMIN_PANEL
    if action == "add_ch":
        d = load_data()
        if text not in d.get("channels", []):
            d.setdefault("channels", []).append(text)
            save_data(d)
            await update.message.reply_text(f"✅  *Added*   _{text}_", parse_mode="Markdown")
        else:
            await update.message.reply_text(f"⚠️  *Already exists*   _{text}_", parse_mode="Markdown")
    elif action == "rm_ch":
        d = load_data()
        if text in d.get("channels", []):
            d["channels"].remove(text)
            save_data(d)
            await update.message.reply_text(f"✅  *Removed*   _{text}_", parse_mode="Markdown")
        else:
            await update.message.reply_text(f"⚠️  *Not found*   _{text}_", parse_mode="Markdown")
    elif action == "bcast":
        d    = load_data()
        sent = fail = 0
        bcast_msg = (
            f"{hdr('📢  Broadcast')}\n\n"
            f"_WS-India 2  ·  Official_\n\n"
            f"{text}"
        )
        async def _send(u):
            nonlocal sent, fail
            try:
                await ctx.bot.send_message(u, bcast_msg, parse_mode="Markdown")
                sent += 1
            except: fail += 1
        await asyncio.gather(*[_send(u) for u in d.get("users", [])], return_exceptions=True)
        await update.message.reply_text(
            f"{hdr('📢  Done')}\n\n{field('Sent', str(sent))}\n{field('Failed', str(fail))}",
            parse_mode="Markdown"
        )
    return ADMIN_PANEL

# ── Withdraw ───────────────────────────────────────
def _wd_text(amount, bankcard, cardname, ifsc, bankname):
    return (
        f"{hdr('💸  Withdrawal Summary')}\n\n"
        f"{field('Amount', '₹ ' + str(amount))}\n\n"
        f"{DS}\n\n"
        f"{field('Account', bankcard)}\n"
        f"{field('Name',    cardname)}\n"
        f"{field('IFSC',    ifsc)}\n"
        f"{field('Bank',    bankname)}\n\n"
        f"{DS}"
    )

def _wd_kb():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("✏️  Edit", callback_data="wd_modify"),
        InlineKeyboardButton("✅  Confirm", callback_data="wd_submit"),
    ]])

async def ask_withdraw(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not await guard(update, ctx): return ConversationHandler.END
    uid = update.effective_user.id
    if not await try_auto_login(uid, ctx):
        await update.message.reply_text(
            f"{hdr('⚠️  Not Logged In')}\n\n_Use /start._",
            parse_mode="Markdown", reply_markup=main_kb()
        )
        return ConversationHandler.END
    creds = load_session(uid)
    if not creds:
        await update.message.reply_text(
            f"{hdr('⚠️  Not Logged In')}\n\n_Use /start._",
            parse_mode="Markdown", reply_markup=main_kb()
        )
        return ConversationHandler.END
    try:
        loop = asyncio.get_running_loop()
        data = await loop.run_in_executor(LOGIN_EXECUTOR, api_login, creds["username"], creds["raw_password"])
        if data.get("code") == 0:
            info = data["data"]["info"]
            ctx.user_data.update({
                "wd_bankcard": info.get("bankcard", "N/A"),
                "wd_bankname": info.get("bankname", "N/A"),
                "wd_cardname": info.get("cardname", "N/A").strip(),
                "wd_ifsc":     info.get("ifsc",     "N/A"),
                "wd_balance":  info.get("balance",  "0.00"),
            })
            amounts, min_wd, max_wd = await loop.run_in_executor(LOGIN_EXECUTOR, get_wd_config)
            ctx.user_data.update({"wd_min": min_wd, "wd_max": max_wd})

            rows, row = [], []
            for amt in amounts:
                row.append(InlineKeyboardButton(amt, callback_data=f"wd_amt|{amt}"))
                if len(row) == 3: rows.append(row); row = []
            if row: rows.append(row)

            msg = await update.message.reply_text(
                f"{hdr('💸  Withdraw')}\n\n"
                f"{field('Balance', '₹ ' + str(info.get('balance', '0.00')))}\n"
                f"{field('Min', min_wd)}  ·  {field('Max', max_wd)}\n\n"
                f"{DS}\n\n"
                f"_Select amount  ↓_",
                parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(rows)
            )
            ctx.user_data["wd_msg_id"] = msg.message_id
            return WAIT_WITHDRAW
        await update.message.reply_text(f"{hdr('❌  Failed')}\n\n_Try again._", parse_mode="Markdown", reply_markup=main_kb())
    except Exception as e:
        await update.message.reply_text(f"{hdr('⚠️  Error')}\n\n`{e}`", parse_mode="Markdown", reply_markup=main_kb())
    return ConversationHandler.END

async def wd_amount_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query  = update.callback_query
    await query.answer()
    amount = query.data.split("|")[1]
    ctx.user_data["wd_amount"] = amount
    try:
        await query.message.edit_text(
            _wd_text(amount,
                     ctx.user_data.get("wd_bankcard", "N/A"),
                     ctx.user_data.get("wd_cardname", "N/A"),
                     ctx.user_data.get("wd_ifsc",     "N/A"),
                     ctx.user_data.get("wd_bankname", "N/A")),
            parse_mode="Markdown", reply_markup=_wd_kb()
        )
    except: pass
    return WAIT_WITHDRAW

async def wd_modify_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await ctx.bot.send_message(
        update.effective_chat.id,
        f"{hdr('✏️  Update Bank Details')}\n\n"
        f"_Step  *1 / 3*_\n\n"
        f"Send your *bank account number.*",
        parse_mode="Markdown"
    )
    return WAIT_MODIFY_ACC_NO

async def do_modify_acc_no(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    acc = update.message.text.strip()
    if not acc:
        await update.message.reply_text(f"{hdr('⚠️  Error')}\n\n*Cannot be empty.*", parse_mode="Markdown")
        return WAIT_MODIFY_ACC_NO
    ctx.user_data["wd_bankcard"] = acc
    await update.message.reply_text(
        f"{hdr('✏️  Update Bank Details')}\n\n_Step  *2 / 3*_\n\nSend *account holder name.*",
        parse_mode="Markdown"
    )
    return WAIT_MODIFY_NAME

async def do_modify_name(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    if not name:
        await update.message.reply_text(f"{hdr('⚠️  Error')}\n\n*Cannot be empty.*", parse_mode="Markdown")
        return WAIT_MODIFY_NAME
    ctx.user_data["wd_cardname"] = name
    await update.message.reply_text(
        f"{hdr('✏️  Update Bank Details')}\n\n_Step  *3 / 3*_\n\nSend your *IFSC code.*",
        parse_mode="Markdown"
    )
    return WAIT_MODIFY_IFSC

async def do_modify_ifsc(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ifsc = update.message.text.strip()
    if not ifsc:
        await update.message.reply_text(f"{hdr('⚠️  Error')}\n\n*Cannot be empty.*", parse_mode="Markdown")
        return WAIT_MODIFY_IFSC
    ctx.user_data["wd_ifsc"] = ifsc
    bankcard = ctx.user_data.get("wd_bankcard", "N/A")
    cardname = ctx.user_data.get("wd_cardname", "N/A")
    bankname = ctx.user_data.get("wd_bankname", "INDIA-Bank")
    amount   = ctx.user_data.get("wd_amount",   "N/A")
    userid   = ctx.user_data.get("userid")
    username = ctx.user_data.get("username")

    msg = await update.message.reply_text(f"{hdr('⏳  Saving')}\n\n_Please wait..._", parse_mode="Markdown")
    try:
        loop = asyncio.get_running_loop()
        res  = await loop.run_in_executor(LOGIN_EXECUTOR, api_setbankcard, userid, username, bankcard, cardname, ifsc, bankname)
        if res.get("code") == 0:
            ctx.user_data["wd_bankname"] = bankname
            await msg.edit_text(f"✅  *Bank details saved.*", parse_mode="Markdown")
        else:
            await msg.edit_text(f"⚠️  *{res.get('message', 'Failed')}*", parse_mode="Markdown")
    except Exception as e:
        await msg.edit_text(f"{hdr('⚠️  Error')}\n\n`{e}`", parse_mode="Markdown")
    await update.message.reply_text(
        _wd_text(amount, bankcard, cardname, ifsc, bankname),
        parse_mode="Markdown", reply_markup=_wd_kb()
    )
    return WAIT_WITHDRAW

async def wd_submit_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await ctx.bot.send_message(
        update.effective_chat.id,
        f"{hdr('🔐  Transaction PIN')}\n\nEnter your *6-digit transaction PIN.*",
        parse_mode="Markdown"
    )
    return WAIT_WITHDRAW_PWD

async def do_withdraw_pwd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    txpwd = update.message.text.strip()
    if not txpwd.isdigit() or len(txpwd) != 6:
        await update.message.reply_text(
            f"{hdr('❌  Invalid PIN')}\n\n*Must be exactly 6 digits.*",
            parse_mode="Markdown"
        )
        return WAIT_WITHDRAW_PWD

    userid, username = ctx.user_data.get("userid"), ctx.user_data.get("username")
    amount           = ctx.user_data.get("wd_amount", "0")
    msg              = await update.message.reply_text(
        f"{hdr('⏳  Processing')}\n\n_Submitting request..._", parse_mode="Markdown"
    )
    try:
        loop    = asyncio.get_running_loop()
        pwd_res = await loop.run_in_executor(LOGIN_EXECUTOR, api_withdraw_pwd, txpwd, userid, username)
        if pwd_res.get("code") != 0:
            await msg.edit_text(
                f"{hdr('❌  Wrong PIN')}\n\n*{pwd_res.get('message', 'Incorrect PIN')}*\n\n{DS}\n\n_Try again._",
                parse_mode="Markdown"
            )
            await update.message.reply_text(f"{hdr('📋  Main Menu')}", parse_mode="Markdown", reply_markup=main_kb())
            return ConversationHandler.END

        wd_res = await loop.run_in_executor(LOGIN_EXECUTOR, api_withdraw, amount, userid, username)
        now    = time.strftime("%d %b  %H:%M")

        if wd_res.get("code") == 0:
            await msg.edit_text(
                f"{hdr('✅  Withdrawal Submitted')}\n\n"
                f"{field('Amount', '₹ ' + amount)}\n"
                f"{field('Status', '🟢 Submitted')}\n"
                f"{field('Time',   now)}",
                parse_mode="Markdown"
            )
        else:
            await msg.edit_text(
                f"{hdr('❌  Failed')}\n\n*{wd_res.get('message', 'Withdrawal failed')}*",
                parse_mode="Markdown"
            )
    except Exception as e:
        await msg.edit_text(f"{hdr('⚠️  Error')}\n\n`{e}`", parse_mode="Markdown")

    await update.message.reply_text(
        f"{hdr('📋  Main Menu')}\n\n_Choose  ↓_",
        parse_mode="Markdown", reply_markup=main_kb()
    )
    return ConversationHandler.END

# ── Fallback ───────────────────────────────────────
async def fallback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not await is_member(ctx.bot, uid):
        await update.message.reply_text(force_join_msg(), parse_mode="Markdown", reply_markup=force_join_kb())
        return ConversationHandler.END
    await update.message.reply_text(
        f"{hdr('📋  Main Menu')}\n\n_Choose an option  ↓_",
        parse_mode="Markdown", reply_markup=main_kb()
    )
    return ConversationHandler.END

# ── /getfile ───────────────────────────────────────
async def cmd_getfile(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    try:
        path = os.path.abspath(__file__)
        with open(path, "rb") as f:
            await ctx.bot.send_document(
                chat_id=update.effective_chat.id, document=f,
                filename="wsindia2_sleek_v6.py",
                caption=(
                    f"{hdr('💎  Source File')}\n\n"
                    f"{field('Bot',   'WS-India 2')}\n"
                    f"{field('Style', 'Sleek Dark v6')}\n\n"
                    f"_Join  ·  @DKEARNING3_"
                ),
                parse_mode="Markdown",
            )
    except Exception as e:
        await update.message.reply_text(f"⚠️  `{e}`", parse_mode="Markdown")

# ── Auto-send on startup ───────────────────────────
async def send_file_to_admin(app):
    await asyncio.sleep(3)
    for attempt in range(5):
        try:
            path = os.path.abspath(__file__)
            with open(path, "rb") as f:
                await app.bot.send_document(
                    chat_id=ADMIN_ID, document=f,
                    filename="wsindia2_sleek_v6.py",
                    caption=(
                        f"{hdr('✅  WS-India 2  ·  Online')}\n\n"
                        f"{field('Status', '🟢 Running')}\n"
                        f"{field('Style',  'Sleek Dark v6')}\n"
                        f"{field('Engine', 'Turbo v3.0')}\n"
                        f"{field('Time',   time.strftime('%d %b  %H:%M'))}\n\n"
                        f"{DS}\n\n"
                        f"_All systems operational._"
                    ),
                    parse_mode="Markdown",
                )
            print("[✓] File sent to admin.")
            return
        except Exception as e:
            print(f"[!] Attempt {attempt+1}/5: {e}")
            await asyncio.sleep(5)
    print("[!] All attempts failed.")

# ── Main ───────────────────────────────────────────
def main():
    print("[*] WS-INDIA 2  ·  SLEEK DARK v6  ·  Starting...")
    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .concurrent_updates(True)
        .post_init(send_file_to_admin)
        .build()
    )

    main_conv = ConversationHandler(
        entry_points=[
            CommandHandler("start", cmd_start),
            MessageHandler(filters.Regex(f"^{B_OUT}$"),   do_logout),
            MessageHandler(filters.Regex(f"^{B_WA}$"),    ask_wa),
            MessageHandler(filters.Regex(f"^{B_TASK}$"),  start_task),
            MessageHandler(filters.Regex(f"^{B_ACC}$"),   show_account),
            MessageHandler(filters.Regex(f"^{B_SEND}$"),  send_all_action),
            MessageHandler(filters.Regex(f"^{B_BACK}$"),  fallback),
            MessageHandler(filters.Regex(f"^{B_WD}$"),    ask_withdraw),
        ],
        states={
            WAIT_LOGIN_USER:    [MessageHandler(filters.TEXT & ~filters.COMMAND, do_login_user)],
            WAIT_LOGIN:         [MessageHandler(filters.TEXT & ~filters.COMMAND, do_login)],
            WAIT_WA:            [MessageHandler(filters.TEXT & ~filters.COMMAND, do_wa)],
            WAIT_WITHDRAW: [
                CallbackQueryHandler(wd_amount_callback, pattern="^wd_amt\\|"),
                CallbackQueryHandler(wd_modify_callback, pattern="^wd_modify$"),
                CallbackQueryHandler(wd_submit_callback, pattern="^wd_submit$"),
            ],
            WAIT_MODIFY_ACC_NO: [MessageHandler(filters.TEXT & ~filters.COMMAND, do_modify_acc_no)],
            WAIT_MODIFY_NAME:   [MessageHandler(filters.TEXT & ~filters.COMMAND, do_modify_name)],
            WAIT_MODIFY_IFSC:   [MessageHandler(filters.TEXT & ~filters.COMMAND, do_modify_ifsc)],
            WAIT_WITHDRAW_PWD:  [MessageHandler(filters.TEXT & ~filters.COMMAND, do_withdraw_pwd)],
        },
        fallbacks=[
            CommandHandler("start", cmd_start),
            MessageHandler(filters.TEXT & ~filters.COMMAND, fallback),
        ],
        allow_reentry=True,
    )

    admin_conv = ConversationHandler(
        entry_points=[CommandHandler("admin", cmd_admin)],
        states={
            ADMIN_PANEL: [
                CallbackQueryHandler(admin_callback, pattern="^admin_"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, admin_text_input),
            ],
        },
        fallbacks=[CommandHandler("start", cmd_start)],
        allow_reentry=True,
        per_message=False,
    )

    app.add_handler(CommandHandler("getfile", cmd_getfile))
    app.add_handler(admin_conv)
    app.add_handler(main_conv)
    app.add_handler(CallbackQueryHandler(check_joined_callback, pattern="^check_joined$"))
    app.add_handler(CallbackQueryHandler(wa_next_callback,      pattern="^wanext\\|"))
    app.add_handler(CallbackQueryHandler(all_done_callback,     pattern="^all_done$"))
    app.add_handler(CallbackQueryHandler(dummy_callback,        pattern="^ignore$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback))

    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
