import requests
import json
import base64
import re
from datetime import datetime
import os

# لینک‌های مخزن barry-far
SOURCES = {
    'vmess': 'https://raw.githubusercontent.com/barry-far/V2ray-config/main/Splitted-By-Protocol/vmess.txt',
    'vless': 'https://raw.githubusercontent.com/barry-far/V2ray-config/main/Splitted-By-Protocol/vless.txt',
    'trojan': 'https://raw.githubusercontent.com/barry-far/V2ray-config/main/Splitted-By-Protocol/trojan.txt',
    'ss': 'https://raw.githubusercontent.com/barry-far/V2ray-config/main/Splitted-By-Protocol/ss.txt'
}

def fetch_configs(url):
    """دریافت کانفیگ‌ها از یک لینک"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            # جدا کردن خطوط و حذف خطوط خالی
            lines = response.text.strip().split('\n')
            configs = [line.strip() for line in lines if line.strip()]
            return configs
        else:
            print(f"❌ خطا در دریافت {url}: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ خطا در دریافت {url}: {e}")
        return []

def decode_v2ray_config(encoded_str):
    """تلاش برای دیکد کردن کانفیگ V2ray"""
    try:
        # اگر لینک با vless:// یا vmess:// شروع بشه
        if encoded_str.startswith(('vmess://', 'vless://', 'trojan://')):
            return encoded_str
        
        # اگر base64 باشه
        try:
            decoded = base64.b64decode(encoded_str).decode('utf-8')
            return decoded
        except:
            return encoded_str
    except:
        return encoded_str

def extract_country_from_config(config):
    """استخراج کشور از کانفیگ (ساده)"""
    # الگوهای رایج برای تشخیص کشور
    patterns = {
        'US': ['us', 'united states', 'america', 'new york', 'california'],
        'DE': ['de', 'germany', 'frankfurt'],
        'NL': ['nl', 'netherlands', 'amsterdam'],
        'UK': ['uk', 'united kingdom', 'london', 'gb'],
        'FR': ['fr', 'france', 'paris'],
        'CA': ['ca', 'canada', 'toronto'],
        'AU': ['au', 'australia', 'sydney'],
        'SG': ['sg', 'singapore'],
        'JP': ['jp', 'japan', 'tokyo'],
        'IR': ['ir', 'iran', 'tehran'],
        'TR': ['tr', 'turkey', 'istanbul']
    }
    
    config_lower = config.lower()
    for country, keywords in patterns.items():
        for keyword in keywords:
            if keyword in config_lower:
                return country
    return '🌍 Unknown'

def generate_vpn_html(configs_list):
    """تولید محتوای جدید برای فایل VPN.html"""
    
    # پردازش کانفیگ‌ها
    processed_configs = []
    for idx, config in enumerate(configs_list[:300]):  # حداکثر ۳۰۰ کانفیگ
        decoded = decode_v2ray_config(config)
        country = extract_country_from_config(decoded)
        
        # تشخیص نوع پروتکل
        protocol = 'Unknown'
        if config.startswith('vmess://'):
            protocol = 'Vmess'
        elif config.startswith('vless://'):
            protocol = 'Vless'
        elif config.startswith('trojan://'):
            protocol = 'Trojan'
        elif 'ss://' in config:
            protocol = 'SS'
        
        processed_configs.append({
            'id': idx + 1,
            'config': config,
            'decoded': decoded[:100] + '...' if len(decoded) > 100 else decoded,
            'country': country,
            'protocol': protocol,
            'active': True
        })
    
    # ساخت فایل HTML جدید
    html_template = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VPN Configs - V-Tunnel</title>
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
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
            color: #667eea;
            font-weight: bold;
        }
        
        .filters {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-bottom: 20px;
        }
        
        .filter-btn {
            padding: 8px 20px;
            border: 1px solid rgba(255,255,255,0.15);
            background: rgba(255,255,255,0.05);
            color: #e0e6f0;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 14px;
        }
        
        .filter-btn:hover, .filter-btn.active {
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-color: transparent;
            transform: translateY(-2px);
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
            border-color: #667eea;
            box-shadow: 0 0 20px rgba(102, 126, 234, 0.2);
        }
        
        .config-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }
        
        .config-card {
            background: rgba(255,255,255,0.05);
            border-radius: 16px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.08);
            backdrop-filter: blur(10px);
            transition: all 0.3s;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        
        .config-card:hover {
            transform: translateY(-5px);
            border-color: #667eea;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
        }
        
        .config-card .badge {
            position: absolute;
            top: 15px;
            left: 15px;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            background: rgba(102, 126, 234, 0.3);
            border: 1px solid rgba(102, 126, 234, 0.2);
        }
        
        .config-card .country {
            font-size: 24px;
            margin-bottom: 10px;
        }
        
        .config-card .protocol {
            display: inline-block;
            padding: 3px 12px;
            border-radius: 12px;
            font-size: 12px;
            background: rgba(118, 75, 162, 0.3);
            margin: 5px 0;
        }
        
        .config-card .config-preview {
            margin-top: 10px;
            padding: 10px;
            background: rgba(0,0,0,0.3);
            border-radius: 8px;
            font-size: 12px;
            color: #8899bb;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            font-family: monospace;
            direction: ltr;
            text-align: left;
        }
        
        .config-card .copy-btn {
            margin-top: 12px;
            padding: 8px 20px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border: none;
            border-radius: 20px;
            color: white;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s;
            width: 100%;
        }
        
        .config-card .copy-btn:hover {
            transform: scale(1.02);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3);
        }
        
        .config-card .copy-btn.copied {
            background: #10b981;
        }
        
        .loading {
            text-align: center;
            padding: 50px;
            font-size: 18px;
            color: #667eea;
        }
        
        .no-results {
            text-align: center;
            padding: 50px;
            color: #8899bb;
        }
        
        @media (max-width: 768px) {
            .header { flex-direction: column; align-items: stretch; }
            .search-box { width: 100%; }
            .config-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>🔒 V-Tunnel VPN Configs</h1>
            <div class="stats">
                <div class="stat-item">📡 Total: <span id="totalCount">0</span></div>
                <div class="stat-item">🟢 Active: <span id="activeCount">0</span></div>
                <div class="stat-item">🔄 Updated: <span id="updateTime">Loading...</span></div>
            </div>
        </div>
        
        <!-- Filters -->
        <div class="filters">
            <button class="filter-btn active" data-filter="all">🌐 All</button>
            <button class="filter-btn" data-filter="Vmess">📦 Vmess</button>
            <button class="filter-btn" data-filter="Vless">📦 Vless</button>
            <button class="filter-btn" data-filter="Trojan">📦 Trojan</button>
            <button class="filter-btn" data-filter="SS">📦 SS</button>
            <input type="text" class="search-box" id="searchInput" placeholder="🔍 Search configs...">
        </div>
        
        <!-- Configs Grid -->
        <div id="configGrid" class="config-grid"></div>
    </div>

    <script>
        // داده‌های کانفیگ از سرور
        const configsData = CONFIGS_PLACEHOLDER;
        
        let currentFilter = 'all';
        let currentSearch = '';
        
        function renderConfigs() {
            const grid = document.getElementById('configGrid');
            const filtered = configsData.filter(c => {
                const matchFilter = currentFilter === 'all' || c.protocol === currentFilter;
                const matchSearch = c.decoded.toLowerCase().includes(currentSearch.toLowerCase()) || 
                                   c.country.includes(currentSearch) ||
                                   c.protocol.toLowerCase().includes(currentSearch.toLowerCase());
                return matchFilter && matchSearch;
            });
            
            if (filtered.length === 0) {
                grid.innerHTML = '<div class="no-results">😕 No configs found</div>';
                return;
            }
            
            grid.innerHTML = filtered.map(c => `
                <div class="config-card" onclick="copyConfig('${c.id}')">
                    <div class="badge">#${c.id}</div>
                    <div class="country">${c.country}</div>
                    <div class="protocol">${c.protocol}</div>
                    <div class="config-preview">${c.decoded}</div>
                    <button class="copy-btn" onclick="event.stopPropagation(); copyConfig('${c.id}')">
                        📋 Copy Config
                    </button>
                </div>
            `).join('');
            
            // به‌روزرسانی آمار
            document.getElementById('totalCount').textContent = configsData.length;
            document.getElementById('activeCount').textContent = configsData.filter(c => c.active).length;
            document.getElementById('updateTime').textContent = new Date().toLocaleString('fa-IR');
        }
        
        function copyConfig(id) {
            const config = configsData.find(c => c.id == id);
            if (!config) return;
            
            navigator.clipboard.writeText(config.config).then(() => {
                const btn = document.querySelector(`.config-card:nth-child(${id}) .copy-btn`);
                if (btn) {
                    btn.textContent = '✅ Copied!';
                    btn.classList.add('copied');
                    setTimeout(() => {
                        btn.textContent = '📋 Copy Config';
                        btn.classList.remove('copied');
                    }, 2000);
                }
            }).catch(() => {
                // Fallback for older browsers
                const textarea = document.createElement('textarea');
                textarea.value = config.config;
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand('copy');
                document.body.removeChild(textarea);
                alert('✅ Config copied to clipboard!');
            });
        }
        
        // Event Listeners
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                currentFilter = this.dataset.filter;
                renderConfigs();
            });
        });
        
        document.getElementById('searchInput').addEventListener('input', function() {
            currentSearch = this.value;
            renderConfigs();
        });
        
        // Render initial
        renderConfigs();
    </script>
</body>
</html>"""
    
    # جایگزینی داده‌ها در HTML
    configs_json = json.dumps(processed_configs, ensure_ascii=False, indent=2)
    final_html = html_template.replace('CONFIGS_PLACEHOLDER', configs_json)
    
    return final_html

def update_vpn_file():
    """عملکرد اصلی به‌روزرسانی"""
    print("🔄 Starting VPN config update...")
    
    all_configs = []
    
    # دریافت کانفیگ‌ها از همه منابع
    for protocol, url in SOURCES.items():
        print(f"📥 Fetching {protocol} configs...")
        configs = fetch_configs(url)
        if configs:
            # اضافه کردن شناسه پروتکل به هر کانفیگ
            tagged_configs = [config for config in configs if config.strip()]
            all_configs.extend(tagged_configs)
            print(f"✅ Received {len(tagged_configs)} {protocol} configs")
    
    if not all_configs:
        print("❌ No configs received!")
        return False
    
    print(f"📊 Total configs received: {len(all_configs)}")
    
    # تولید HTML جدید
    new_html = generate_vpn_html(all_configs)
    
    # ذخیره فایل
    file_path = os.path.join('mini-app', 'VPN.html')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print(f"✅ VPN.html updated successfully at {datetime.now()}")
    print(f"📁 File saved: {file_path}")
    return True

if __name__ == "__main__":
    update_vpn_file()