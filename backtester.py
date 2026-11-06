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

# %% plotting mas with close
ma20 = close.rolling(20).mean() #Moving averages
ma50 = close.rolling(50).mean()
ax = close.plot(label="Close") #Getting the ma and close on same graph
ma20.plot(ax=ax, label="MA20")
ma50.plot(ax=ax, label="MA50")
plt.legend()
plt.show()
# %% plotting the mas in the same graph on 2024
ax = close.loc["2024"].plot(label="Close") #Zooming on 2024
ma20.loc["2024"].plot(ax=ax, label="MA20")
ma50.loc["2024"].plot(ax=ax, label="MA50")
plt.legend()
plt.show()
# %% Strategy of ma20 above ma50
signal = (ma20 > ma50)
signal.loc["2024"]
signal = signal.astype(int) #Converting to 1s and 0s

#Signal.sum counts days in market, len(signal) is total number of days
#Ratio is time invested
print(signal.sum(), len(signal)) 
# %%
#First backtest result, the strategy returns are less than the buyhold curve
strat_returns = returns * signal.shift(1)
strat_curve = (1 + strat_returns).cumprod()
bh_curve = (1 + returns).cumprod()

#First plot creates axis
ax = bh_curve.plot(label="Buy & Hold")
strat_curve.plot(ax=ax, label="MA20 > MA50")
plt.legend()
plt.show()



# %%
