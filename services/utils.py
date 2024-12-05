import pandas

def calculate_ema(data, period, column="price"):
    return data[column].ewm(span=period, adjust=False).mean()

def calculate_macd(data, short_period=12, long_period=26, signal_period=9):
    data["macd_line"] = calculate_ema(data, short_period) - calculate_ema(data, long_period)
    data["signal_line"] = data["macd_line"].ewm(span=signal_period, adjust=False).mean()
    data["macd_histogram"] = data["macd_line"] - data["signal_line"]
    return data

def calculate_supertrend(data, period=10, multiplier=3):
    data["high"] = data['price'].rolling(window=period).max()
    data["low"] = data['price'].rolling(window=period).min()
    hl2 = (data["high"] + data["low"]) / 2
    data["atr"] = hl2.rolling(window=period).mean()

    supertrend_upperband = hl2 + (multiplier * data["atr"])
    supertrend_lowerband = hl2 - (multiplier * data["atr"])

    supertrend = []
    in_uptrend = True

    for i in range(len(data)):
        if data["price"][i] > supertrend_upperband[i]:
            in_uptrend = True
        elif data["price"][i] < supertrend_lowerband[i]:
            in_uptrend = False

        if in_uptrend:
            supertrend.append(supertrend_lowerband[i])
        else:
            supertrend.append(supertrend_upperband[i])

    data["supertrend"] = supertrend
    return data