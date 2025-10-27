# coin_manager.py

class CoinManager:
    coins = 0  # Start with 0 coins

    @staticmethod
    def add_coins(amount):
        CoinManager.coins += amount

    @staticmethod
    def use_coins(amount):
        if CoinManager.coins >= amount:
            CoinManager.coins -= amount
            return True
        return False

    @staticmethod
    def get_coins():
        return CoinManager.coins
