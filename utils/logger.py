import logging
import os
from datetime import datetime


def setup_logger(name: str, log_dir: str = "logs", level: int = logging.INFO) -> logging.Logger:
    """
    ایجاد و پیکربندی یک logger با نام مشخص.

    :param name: نام logger
    :param log_dir: مسیر ذخیره‌سازی فایل‌های لاگ
    :param level: سطح لاگ‌گیری
    :return: شیء logger پیکربندی‌شده
    """
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # جلوگیری از افزودن چندین handler به logger
    if not logger.handlers:
        # قالب‌بندی لاگ‌ها
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # ایجاد handler برای فایل
        file_handler = logging.FileHandler(os.path.join(log_dir, f"{name}.log"))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # ایجاد handler برای کنسول
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
