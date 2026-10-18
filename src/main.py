
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf


# 1. 基础配置
SYMBOLS = ["AAPL", "SPY", "QQQ"]
PERIOD = "2y"

# 绝对定位到桌面的主文件夹
BASE_DIR = Path.home() / "Desktop" / "Quant Trading System"

# 指定主文件夹下的两个子文件夹
DATA_DIR = BASE_DIR / "data"
CHART_DIR = BASE_DIR / "charts"

DATA_DIR.mkdir(exist_ok=True)
CHART_DIR.mkdir(exist_ok=True)


# 2. 获取历史行情
def get_data(symbol):
    print(f"Downloading {symbol}...")

    df = yf.download(
        symbol,
        period=PERIOD,
        interval="1d",
        auto_adjust=True,
        multi_level_index=False,
        progress=False,
    )

    if df.empty:
        raise ValueError(f"No data found for {symbol}")

    df = df.sort_index()

    # 检查关键字段
    required = ["Open", "High", "Low", "Close", "Volume"]

    if not all(col in df.columns for col in required):
        raise ValueError(f"Missing price columns for {symbol}")

    return df


# 3. 计算技术指标
def calculate_indicators(df):
    df = df.copy()

    df["MA10"] = df["Close"].rolling(10).mean()
    df["MA30"] = df["Close"].rolling(30).mean()

    return df


# 4. 保存行情数据
def save_data(df, symbol):
    file_path = DATA_DIR / f"{symbol}.csv"
    df.to_csv(file_path)

    print(f"Data saved: {file_path}")


# 5. 绘制走势图
def plot_data(df, symbol):
    plt.figure(figsize=(12, 6))

    plt.plot(df.index, df["Close"], label="Close")
    plt.plot(df.index, df["MA10"], label="MA10")
    plt.plot(df.index, df["MA30"], label="MA30")

    plt.title(f"{symbol} Price and Moving Averages")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid(alpha=0.3)

    file_path = CHART_DIR / f"{symbol}.png"

    plt.savefig(file_path, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"Chart saved: {file_path}")


# 6. 程序入口
def main():
    for symbol in SYMBOLS:
        try:
            df = get_data(symbol)
            df = calculate_indicators(df)

            save_data(df, symbol)
            plot_data(df, symbol)

            print(f"{symbol}: {len(df)} trading days loaded")
            print("-" * 40)

        except Exception as error:
            print(f"Error processing {symbol}: {error}")


if __name__ == "__main__":
    main()
