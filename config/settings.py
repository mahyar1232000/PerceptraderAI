# config/settings.py

import os
import json
import logging

# دایرکتوری پیکربندی (config)
BASE_DIR = os.path.dirname(__file__)


def load_credentials() -> dict:
    """
    بارگذاری تنظیمات از credentials.json.
    از json.load برای تبدیل JSON به دیکشنری پایتون استفاده می‌کند. :contentReference[oaicite:6]{index=6}
    """
    cred_path = os.path.join(BASE_DIR, 'credentials.json')
    try:
        with open(cred_path, 'r', encoding='utf-8') as f:
            creds = json.load(f)
    except Exception as e:
        logging.error(f"Cannot load credentials.json: {e}")
        raise

    # تبدیل مسیر نسبی mt5 terminal به مسیر مطلق
    project_root = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
    mt5_rel = creds.get('mt5', {}).get('terminal_path', 'mt5/terminal64.exe')
    creds['mt5']['terminal_path'] = os.path.join(project_root,
                                                 mt5_rel)  # uses os.path.join :contentReference[oaicite:7]{index=7}

    return creds
