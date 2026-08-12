import re
import json
import os
from datetime import datetime
from telethon import TelegramClient, events
import asyncio

# تنظیمات - اینارو باید از my.telegram.org بگیری
API_ID = 12345  # API ID خودت رو وارد کن
API_HASH = 'your_api_hash_here'  # API Hash خودت رو وارد کن
CHANNEL_USERNAME = 'ProxyMTProto'  # نام کاربری کانال

def parse_proxy_message(text):
    """پارس کردن پیام و استخراج اطلاعات پروکسی"""
    proxies = []
    
    # الگوی تشخیص پروکسی MTProto
    # معمولاً به این فرمته: 
    # Server: xxx
    # Port: xxx
    # Secret: xxx
    # @ProxyMTProto
    
    # جدا کردن پروکسی‌ها با الگوی تکراری
    blocks = re.split(r'@ProxyMTProto', text)
    
    for block in blocks:
        if not block.strip():
            continue
            
        # استخراج سرور
        server_match = re.search(r'Server:\s*(.+?)(?:\n|$)', block, re.IGNORECASE)
        # استخراج پورت
        port_match = re.search(r'Port:\s*(\d+)', block, re.IGNORECASE)
        # استخراج سکرت
        secret_match = re.search(r'Secret:\s*([a-fA-F0-9]+|=+[a-zA-Z0-9+/=]+)', block, re.IGNORECASE)
        
        server = server_match.group(1).strip() if server_match else 'Unknown'
        port = port_match.group(1) if port_match else '443'
        secret = secret_match.group(1) if secret_match else ''
        
        # اگر سکرت پیدا نشد، شاید به فرمت دیگه‌ای باشه
        if not secret:
            # چک کردن خطوطی که با Secret شروع نمیشن ولی شبیه سکرتن
            lines = block.strip().split('\n')
            for line in lines:
                if '=' in line or len(line.strip()) > 30:
                    secret = line.strip()
                    break
        
        if secret:
            # ساخت لینک پروکسی
            proxy_link = f"https://t.me/proxy?server={server}&port={port}&secret={secret}"
            
            proxies.append({
                'server': server,
                'port': port,
                'secret': secret,
                'link': proxy_link,
                'active': True
            })
    
    return proxies

async def fetch_proxies_from_channel():
    """دریافت پروکسی‌ها از کانال تلگرام"""
    print("🔄 Connecting to Telegram...")
    
    # ایجاد کلاینت
    client = TelegramClient('session_proxy', API_ID, API_HASH)
    
    try:
        await client.start()
        print("✅ Connected to Telegram!")
        
        # گرفتن کانال
        channel = await client.get_entity(f'@{CHANNEL_USERNAME}')
        print(f"📢 Channel: {channel.title}")
        
        # دریافت پیام‌های اخیر (حداکثر ۵۰ پیام)
        messages = []
        async for message in client.iter_messages(channel, limit=50):
            if message.text:
                messages.append(message.text)
                print(f"📝 Found message: {message.text[:50]}...")
        
        if not messages:
            print("❌ No messages found!")
            return []
        
        # پردازش همه پیام‌ها
        all_proxies = []
        for msg in messages:
            proxies = parse_proxy_message(msg)
            all_proxies.extend(proxies)
            print(f"✅ Found {len(proxies)} proxies in a message")
        
        # حذف پروکسی‌های تکراری بر اساس secret
        unique_proxies = []
        seen_secrets = set()
        for proxy in all_proxies:
            if proxy['secret'] not in seen_secrets:
                seen_secrets.add(proxy['secret'])
                unique_proxies.append(proxy)
        
        print(f"📊 Total unique proxies found: {len(unique_proxies)}")
        return unique_proxies
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return []
    finally:
        await client.disconnect()
        print("🔌 Disconnected from Telegram")

def generate_proxy_html(proxies_list):
    """تولید محتوای جدید برای فایل Proxy.html"""
    
    # مرتب‌سازی بر اساس سرور
    proxies_list.sort(key=lambda x: x['server'])
    
    html_template = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MTProto Proxies - V-Tunnel</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Vazirmatn', 'Segoe UI', sans-serif;
            background: #0a0e1a;
            color: #e0e6f0;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            background: rgba(255,255,255,0.05);
            border-radius: 16px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            margin-bottom: 30px;
            flex-wrap: wrap;
            gap: 15px;
        }
        .header h1 {
            font-size: 24px;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .stats {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }
        .stat-item {
            background: rgba(255,255,255,0.05);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
            border: 1px solid rgba(255,255,255,0.08);
        }
        .stat-item span {
            color: #f5576c;
            font-weight: bold;
        }
        .filters {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-bottom: 20px;
        }
        .search-box {
            padding: 10px 20px;
            border-radius: 25px;
            border: 1px solid rgba(255,255,255,0.1);
            background: rgba(255,255,255,0.05);
            color: #e0e6f0;
            width: 250px;
            font-size: 14px;
            outline: none;
            transition: all 0.3s;
        }
        .search-box:focus {
            border-color: #f5576c;
            box-shadow: 0 0 20px rgba(245, 87, 108, 0.2);
        }
        .proxy-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }
        .proxy-card {
            background: rgba(255,255,255,0.05);
            border-radius: 16px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.08);
            backdrop-filter: blur(10px);
            transition: all 0.3s;
        }
        .proxy-card:hover {
            transform: translateY(-5px);
            border-color: #f5576c;
            box-shadow: 0 10px 30px rgba(245, 87, 108, 0.2);
        }
        .proxy-card .server {
            font-size: 20px;
            font-weight: bold;
            color: #f5576c;
            margin-bottom: 10px;
        }
        .proxy-card .details {
            display: flex;
            gap: 15px;
            font-size: 14px;
            color: #8899bb;
            margin: 10px 0;
        }
        .proxy-card .secret {
            padding: 10px;
            background: rgba(0,0,0,0.3);
            border-radius: 8px;
            font-size: 12px;
            color: #f093fb;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            font-family: monospace;
            direction: ltr;
            text-align: left;
        }
        .proxy-card .actions {
            display: flex;
            gap: 10px;
            margin-top: 15px;
        }
        .proxy-card .actions button {
            flex: 1;
            padding: 10px;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s;
            color: white;
        }
        .btn-copy {
            background: linear-gradient(135deg, #f093fb, #f5576c);
        }
        .btn-copy:hover {
            transform: scale(1.02);
            box-shadow: 0 5px 20px rgba(245, 87, 108, 0.3);
        }
        .btn-copy.copied {
            background: #10b981;
        }
        .btn-link {
            background: rgba(255,255,255,0.1);
        }
        .btn-link:hover {
            background: rgba(255,255,255,0.2);
        }
        .no-results {
            text-align: center;
            padding: 50px;
            color: #8899bb;
        }
        @media (max-width: 768px) {
            .header { flex-direction: column; align-items: stretch; }
            .search-box { width: 100%; }
            .proxy-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔗 MTProto Proxies</h1>
            <div class="stats">
                <div class="stat-item">📡 Total: <span id="totalCount">0</span></div>
                <div class="stat-item">🟢 Active: <span id="activeCount">0</span></div>
                <div class="stat-item">🔄 Updated: <span id="updateTime">Loading...</span></div>
            </div>
        </div>
        
        <div class="filters">
            <input type="text" class="search-box" id="searchInput" placeholder="🔍 Search proxy (server/port/secret)...">
        </div>
        
        <div id="proxyGrid" class="proxy-grid"></div>
    </div>

    <script>
        const proxiesData = PROXIES_PLACEHOLDER;
        let currentSearch = '';
        
        function renderProxies() {
            const grid = document.getElementById('proxyGrid');
            const filtered = proxiesData.filter(p => {
                const search = currentSearch.toLowerCase();
                return p.server.toLowerCase().includes(search) || 
                       p.port.includes(search) ||
                       p.secret.toLowerCase().includes(search);
            });
            
            if (filtered.length === 0) {
                grid.innerHTML = '<div class="no-results">😕 No proxies found</div>';
                return;
            }
            
            grid.innerHTML = filtered.map(p => `
                <div class="proxy-card">
                    <div class="server">🖥️ ${p.server}</div>
                    <div class="details">
                        <span>📌 Port: ${p.port}</span>
                    </div>
                    <div class="secret">🔑 ${p.secret}</div>
                    <div class="actions">
                        <button class="btn-copy" onclick="copyProxy('${p.id}')">📋 Copy</button>
                        <button class="btn-link" onclick="openLink('${p.id}')">🔗 Link</button>
                    </div>
                </div>
            `).join('');
            
            document.getElementById('totalCount').textContent = proxiesData.length;
            document.getElementById('activeCount').textContent = proxiesData.filter(p => p.active).length;
            document.getElementById('updateTime').textContent = new Date().toLocaleString('fa-IR');
        }
        
        function copyProxy(id) {
            const proxy = proxiesData.find(p => p.id == id);
            if (!proxy) return;
            
            const text = `Server: ${proxy.server}\\nPort: ${proxy.port}\\nSecret: ${proxy.secret}`;
            
            navigator.clipboard.writeText(text).then(() => {
                const btn = document.querySelector(`.proxy-card:nth-child(${id}) .btn-copy`);
                if (btn) {
                    btn.textContent = '✅ Copied!';
                    btn.classList.add('copied');
                    setTimeout(() => {
                        btn.textContent = '📋 Copy';
                        btn.classList.remove('copied');
                    }, 2000);
                }
            }).catch(() => {
                const textarea = document.createElement('textarea');
                textarea.value = text;
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand('copy');
                document.body.removeChild(textarea);
                alert('✅ Proxy copied!');
            });
        }
        
        function openLink(id) {
            const proxy = proxiesData.find(p => p.id == id);
            if (proxy && proxy.link) {
                window.open(proxy.link, '_blank');
            }
        }
        
        document.getElementById('searchInput').addEventListener('input', function() {
            currentSearch = this.value;
            renderProxies();
        });
        
        renderProxies();
    </script>
</body>
</html>"""
    
    # اضافه کردن id به هر پروکسی
    for idx, proxy in enumerate(proxies_list):
        proxy['id'] = idx + 1
    
    # جایگزینی داده‌ها
    proxies_json = json.dumps(proxies_list, ensure_ascii=False, indent=2)
    final_html = html_template.replace('PROXIES_PLACEHOLDER', proxies_json)
    
    return final_html

async def main():
    """تابع اصلی"""
    print("🚀 Starting Proxy MTProto updater...")
    
    # دریافت پروکسی‌ها
    proxies = await fetch_proxies_from_channel()
    
    if not proxies:
        print("❌ No proxies found!")
        return False
    
    # تولید HTML جدید
    new_html = generate_proxy_html(proxies)
    
    # ذخیره فایل
    file_path = os.path.join('mini-app', 'Proxy.html')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print(f"✅ Proxy.html updated successfully at {datetime.now()}")
    print(f"📁 File saved: {file_path}")
    print(f"📊 Total proxies: {len(proxies)}")
    
    # نمایش چند نمونه
    print("\n📋 Sample proxies:")
    for proxy in proxies[:5]:
        print(f"  - Server: {proxy['server']}, Port: {proxy['port']}")
    
    return True

if __name__ == "__main__":
    asyncio.run(main())
