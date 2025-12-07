"""CSS styles and JavaScript for CareerLens UI"""
import streamlit as st
from modules.utils.helpers import get_img_as_base64
import os

# Load logo for hero banner
_logo_base64 = ""
_logo_html = ""

logo_paths = ["logo.png", "CareerLens_Logo.png"]
for logo_path in logo_paths:
    if os.path.exists(logo_path):
        try:
            _logo_base64 = get_img_as_base64(logo_path)
            _logo_html = f'<img src="data:image/png;base64,{_logo_base64}" class="hero-bg-logo">'
            break
        except Exception as e:
            _logo_html = '<div class="hero-bg-logo"></div>'
            break
else:
    _logo_html = '<div class="hero-bg-logo"></div>'


def render_styles():
    """Render all CSS styles and JavaScript for the application"""
    st.markdown("""
    <style>
        /* CareerLens Design System - CSS Variables */
        :root {{
            --navy: #0f172a;
            --cyan: #00d2ff;
            --bg-gray: #f3f4f6;
            --primary-accent: #0F62FE;
            --action-accent: #0F62FE;
            --bg-main: #f3f4f6;
            --bg-container: #F4F7FC;
            --card-bg: #FFFFFF;
            --text-primary: #161616;
            --text-secondary: #161616;
            --text-muted: #161616;
            --border-color: #E0E0E0;
            --hover-bg: #F0F0F0;
            --success-green: #10B981;
            --warning-amber: #F59E0B;
            --error-red: #EF4444;
            --navy-deep: #1e3a5f;
            --navy-light: #2C3E50;
        }}
        
        [data-theme="dark"],
        html[data-theme="dark"],
        html[data-theme="dark"] :root {{
            --primary-accent: #4589FF;
            --action-accent: #4589FF;
            --bg-main: #161616;
            --bg-container: #262626;
            --card-bg: #262626;
            --text-primary: #F4F4F4;
            --text-secondary: #F4F4F4;
            --text-muted: #F4F4F4;
            --border-color: #3D3D3D;
            --hover-bg: #333333;
            --navy: #1e293b;
            --cyan: #22d3ee;
            --bg-gray: #1f2937;
        }}
        
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header[data-testid="stHeader"] {{visibility: hidden; height: 0; padding: 0; margin: 0;}}
        .stDeployButton {{display: none;}}
        
        .stApp {{
            background-color: var(--bg-gray);
            color: var(--text-primary);
        }}
        
        [data-testid="stSidebar"] {{
            background-color: var(--navy);
            padding: 2rem 1rem;
        }}
        [data-testid="stSidebar"] * {{
            color: #94a3b8 !important;
        }}
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] .stMarkdown h2,
        [data-testid="stSidebar"] .stMarkdown h3 {{
            color: white !important;
        }}
        [data-testid="stSidebar"] .stButton > button {{
            background-color: var(--cyan) !important;
            color: var(--navy) !important;
            font-weight: 600 !important;
        }}
        [data-testid="stSidebar"] .stButton > button:hover {{
            background-color: #06b6d4 !important;
        }}
        
        .hero-container {{
            background: linear-gradient(135deg, var(--navy) 0%, #112545 100%);
            padding: 40px;
            border-radius: 12px;
            color: white;
            position: relative;
            overflow: hidden;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }}
        .hero-content {{
            position: relative;
            z-index: 2;
        }}
        .hero-title {{
            font-size: 32px;
            font-weight: 700;
            margin: 0;
            color: white;
        }}
        .hero-subtitle {{
            color: #94a3b8;
            font-size: 16px;
            margin-top: 10px;
        }}
        .hero-bg-logo {{
            position: absolute;
            right: -30px;
            top: -30px;
            width: 250px;
            opacity: 0.15;
            transform: rotate(-15deg);
            pointer-events: none;
            z-index: 1;
        }}
        
        .dashboard-metric-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .dashboard-metric-label {{
            font-size: 12px;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .dashboard-metric-value {{
            font-size: 28px;
            font-weight: 700;
            color: #111827;
            margin-top: 5px;
        }}
        
        [data-theme="dark"] .hero-container {{
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        }}
        [data-theme="dark"] .dashboard-metric-card {{
            background: var(--card-bg);
        }}
        [data-theme="dark"] .dashboard-metric-value {{
            color: var(--text-primary);
        }}
        
        .job-card {{
            background-color: var(--bg-container);
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
            border: none;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        .job-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        }}
        
        .match-score {{
            background-color: var(--action-accent);
            color: white;
            padding: 0.4rem 1rem;
            border-radius: 20px;
            font-weight: bold;
            display: inline-block;
            font-size: 0.9rem;
        }}
        
        .tag {{
            display: inline-block;
            background-color: var(--bg-container);
            color: var(--text-primary);
            padding: 0.3rem 0.8rem;
            border-radius: 12px;
            margin: 0.2rem;
            font-size: 0.85rem;
            border: none;
        }}
        
        .match-score-display {{
            font-size: 2rem;
            font-weight: bold;
            color: var(--action-accent);
            text-align: center;
        }}
        
        .main-header {{
            font-size: 3rem;
            font-weight: bold;
            color: var(--primary-accent);
            text-align: center;
            margin-bottom: 1rem;
            letter-spacing: -0.02em;
        }}
        
        .ws-reconnecting-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.7);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 99999;
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.3s, visibility 0.3s;
        }}
        .ws-reconnecting-overlay.active {{
            opacity: 1;
            visibility: visible;
        }}
        .ws-reconnecting-content {{
            background: white;
            padding: 30px 40px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }}
        [data-theme="dark"] .ws-reconnecting-content {{
            background: #262626;
            color: #f4f4f4;
        }}
        .ws-reconnecting-spinner {{
            width: 40px;
            height: 40px;
            border: 4px solid #e0e0e0;
            border-top-color: #0F62FE;
            border-radius: 50%;
            animation: ws-spin 1s linear infinite;
            margin: 0 auto 15px;
        }}
        @keyframes ws-spin {{
            to {{ transform: rotate(360deg); }}
        }}
        .ws-reconnecting-text {{
            font-size: 16px;
            color: #333;
            margin-bottom: 5px;
        }}
        [data-theme="dark"] .ws-reconnecting-text {{
            color: #f4f4f4;
        }}
        .ws-reconnecting-subtext {{
            font-size: 13px;
            color: #666;
        }}
        [data-theme="dark"] .ws-reconnecting-subtext {{
            color: #999;
        }}
    </style>
    <div id="ws-reconnecting-overlay" class="ws-reconnecting-overlay">
        <div class="ws-reconnecting-content">
            <div class="ws-reconnecting-spinner"></div>
            <div class="ws-reconnecting-text">Reconnecting...</div>
            <div class="ws-reconnecting-subtext">Please wait while we restore your connection</div>
        </div>
    </div>
    <script>
    (function() {
        function updateTheme() {
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            if (prefersDark) {
                document.documentElement.setAttribute('data-theme', 'dark');
                const stApp = document.querySelector('.stApp') || document.querySelector('[data-testid="stApp"]');
                if (stApp) {
                    stApp.setAttribute('data-theme', 'dark');
                }
                document.body.setAttribute('data-theme', 'dark');
            } else {
                document.documentElement.removeAttribute('data-theme');
                const stApp = document.querySelector('.stApp') || document.querySelector('[data-testid="stApp"]');
                if (stApp) {
                    stApp.removeAttribute('data-theme');
                }
                document.body.removeAttribute('data-theme');
            }
        }
        
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', updateTheme);
        } else {
            updateTheme();
        }
        
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
        if (mediaQuery.addEventListener) {
            mediaQuery.addEventListener('change', updateTheme);
        } else {
            mediaQuery.addListener(updateTheme);
        }
    })();
    
    (function() {
        const overlay = document.getElementById('ws-reconnecting-overlay');
        let isReconnecting = false;
        let reconnectAttempts = 0;
        const maxReconnectAttempts = 5;
        let reconnectTimer = null;
        
        function showReconnectingOverlay() {
            if (overlay && !isReconnecting) {
                isReconnecting = true;
                overlay.classList.add('active');
            }
        }
        
        function hideReconnectingOverlay() {
            if (overlay) {
                isReconnecting = false;
                reconnectAttempts = 0;
                overlay.classList.remove('active');
            }
        }
        
        function attemptReconnect() {
            if (reconnectAttempts >= maxReconnectAttempts) {
                window.location.reload();
                return;
            }
            
            reconnectAttempts++;
            const delay = Math.min(1000 * Math.pow(2, reconnectAttempts - 1), 16000);
            
            reconnectTimer = setTimeout(function() {
                if (navigator.onLine) {
                    try {
                        const stApp = window.parent.document || document;
                        const rerunButton = stApp.querySelector('[data-testid="stRerunButton"]');
                        if (rerunButton) {
                            rerunButton.click();
                            hideReconnectingOverlay();
                            return;
                        }
                    } catch (e) {
                        console.log('CareerLens: Could not trigger Streamlit rerun');
                    }
                    
                    if (reconnectAttempts >= 3) {
                        window.location.reload();
                    } else {
                        attemptReconnect();
                    }
                } else {
                    attemptReconnect();
                }
            }, delay);
        }
        
        window.addEventListener('offline', function() {
            showReconnectingOverlay();
        });
        
        window.addEventListener('online', function() {
            setTimeout(function() {
                hideReconnectingOverlay();
                window.location.reload();
            }, 1000);
        });
        
        const OriginalWebSocket = window.WebSocket;
        window.WebSocket = function(url, protocols) {
            const ws = protocols ? new OriginalWebSocket(url, protocols) : new OriginalWebSocket(url);
            
            if (url && (url.includes('_stcore/stream') || url.includes('logstream'))) {
                ws.addEventListener('close', function(event) {
                    if (event.code !== 1000 && event.code !== 1001) {
                        showReconnectingOverlay();
                        attemptReconnect();
                    }
                });
                
                ws.addEventListener('error', function(event) {
                    showReconnectingOverlay();
                    attemptReconnect();
                });
                
                ws.addEventListener('open', function() {
                    hideReconnectingOverlay();
                });
            }
            
            return ws;
        };
        window.WebSocket.prototype = OriginalWebSocket.prototype;
        window.WebSocket.CONNECTING = OriginalWebSocket.CONNECTING;
        window.WebSocket.OPEN = OriginalWebSocket.OPEN;
        window.WebSocket.CLOSING = OriginalWebSocket.CLOSING;
        window.WebSocket.CLOSED = OriginalWebSocket.CLOSED;
        
        window.addEventListener('beforeunload', function() {
            if (reconnectTimer) {
                clearTimeout(reconnectTimer);
            }
        });
    })();
    </script>
    """, unsafe_allow_html=True)


def get_logo_html():
    """Get logo HTML for hero banner"""
    return _logo_html
