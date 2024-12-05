import pandas 
import sys
from services.utils import calculate_macd, calculate_supertrend

def apply_strategy(data):
    data = calculate_macd(data)
    data = calculate_supertrend(data)

    signals = ["HOLD"] * len(data) # Assigning all signals as HOLD.
    cumulative_profit_loss = [0] * len(data)
    unrealised_gain_loss = [0] * len(data)

    trade_open = None # To check whether position is opened or closed.
    entry_price = None
    max_price = None
    min_price = sys.maxsize
    total_pnl = 0 # realised profit or loss
    gain_loss = 0 # unrealised profit or loss

    target_price_rate = 0.10 # 10% above or below entry price
    stop_loss_price_rate = 0.04 # 4% above or below entry price to minimize loss
    trailing_stop_price_rate = 0.025 # 2.5% below or above target price
    

    for i in range(1, len(data)):
        current_price = data["price"][i]

        # Generate BUY Signal
        if (
            data["macd_line"][i] < data["signal_line"][i]
            and data["macd_line"][i-1] >= data["signal_line"][i-1]
            and current_price > data["supertrend"][i]
            and trade_open is None
        ):
            signals[i] = "ENTER_BUY"
            trade_open = "OPEN_BUY"
            entry_price = current_price
            max_price = current_price

        # Generate SELL Signal
        elif (
            data["macd_line"][i] > data["signal_line"][i]
            and data["macd_line"][i-1] <= data["signal_line"][i-1]
            and current_price < data["supertrend"][i]
            and trade_open is None
        ):
            signals[i] = "ENTER_SELL"
            trade_open = "OPEN_SELL"
            entry_price = current_price
            min_price = current_price

        # Check for Exit Conditions for Long positions
        elif trade_open == "OPEN_BUY":
            max_price = max(max_price, current_price)
            stop_loss_price = entry_price - (entry_price * stop_loss_price_rate)
            target_price = entry_price + (entry_price * target_price_rate)

            if current_price >= target_price:
                trailing_stop_price = max_price - (max_price * trailing_stop_price_rate)
            else: 
                trailing_stop_price = None

            if current_price <= stop_loss_price or (trailing_stop_price and current_price <= trailing_stop_price):
                signals[i] = "EXIT_SELL"
                pnl = current_price - entry_price
                total_pnl += pnl
                gain_loss = 0
                trade_open = None

            else : 
                gain_loss = current_price - entry_price

        # Check for Exit Conditions for Short positions
        elif trade_open == "OPEN_SELL":
            min_price = min(min_price, current_price)
            stop_loss_price = entry_price + (entry_price * stop_loss_price_rate)
            target_price = entry_price - (entry_price * target_price_rate)

            if current_price <= target_price:
                trailing_stop_price = min_price + (min_price * trailing_stop_price_rate)
            else: 
                trailing_stop_price = None

            if current_price >= stop_loss_price or (trailing_stop_price and current_price >= trailing_stop_price):
                signals[i] = "EXIT_BUY"
                pnl = entry_price - current_price
                total_pnl += pnl
                trade_open = None
                gain_loss = 0

            else : 
                gain_loss = entry_price - current_price

        cumulative_profit_loss[i] = total_pnl

        unrealised_gain_loss[i] = gain_loss

    data["signals"] = signals
    data["unrealised_gain_loss"] = unrealised_gain_loss
    data["cumulative_pnl"] = cumulative_profit_loss
    return data
