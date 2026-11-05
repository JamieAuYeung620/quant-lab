# %%
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
data = yf.download("AAPL", start = "2021-01-01")

# %%
print(type(data))
close = data["Close"]["AAPL"]
last5rows = close.tail(5)
plt.plot(close)
plt.show()

# %%
returns = close.pct_change() #shows percentage change
returns.head()

plt.plot(returns)
plt.show()

# %%
(1 + returns).cumprod().plot()
plt.show()

# %%
ma20 = close.rolling(20).mean() #Moving averages
ma50 = close.rolling(50).mean()
ax = close.plot(label="Close") #Getting the ma and close on same graph
ma20.plot(ax=ax, label="MA20")
ma50.plot(ax=ax, label="MA50")
plt.legend()
plt.show()
# %%
ax = close.loc["2024"].plot(label="Close") #Zooming on 2024
ma20.loc["2024"].plot(ax=ax, label="MA20")
ma50.loc["2024"].plot(ax=ax, label="MA50")
plt.legend()
plt.show()
# %%
signal = (ma20 > ma50)
signal.loc["2024"]
# %%
