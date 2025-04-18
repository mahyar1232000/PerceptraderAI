# trade/multi_asset_support.py

import logging


class MultiAssetManager:
    """
    پشتیبانی از دارایی‌های مختلف: فارکس، کریپتو، سهام و کالا.
    """

    def __init__(self, assets: list[str]):
        self.assets = assets
        logging.info(f"MultiAssetManager initialized with assets: {assets}")

    def is_supported(self, symbol: str) -> bool:
        """
        بررسی پشتیبانی دارایی بر اساس نماد.
        """
        supported = symbol in self.assets
        if not supported:
            logging.warning(f"Asset {symbol} not supported.")
        return supported
