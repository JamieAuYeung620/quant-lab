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

trades = signal.diff().abs()
trades.loc["2024-04-20": "2024-06-15"]
print(trades.sum())
# %%
cost = 0.001
strat_net = strat_returns - trades.shift(1) * cost
net_curve = (1 + strat_net).cumprod()

ax = bh_curve.plot(label="Buy & Hold")
strat_curve.plot(ax=ax, label="Strategy")
net_curve.plot(ax=ax, label="Strategy after costs")
plt.legend()
plt.show()

#Costs don't matter too much to the strategy
# %%
import numpy as np
r = strat_net.dropna() #Daily returns, NaN values are dropped
curve = (1 + r).cumprod() #Cumulative returns

total_return = curve.iloc[-1] - 1 #Returns the final return
years = len(r) / 252 #Trading days in a year
ann_return = (1 + total_return) ** (1 / years) - 1
ann_vol = r.std() * np.sqrt(252) #Annualized volatility
sharpe = ann_return / ann_vol #Sharpe ratio

#Drawdown is the difference between the peak and the trough of the curve
peak = curve.cummax() #Cumulative max of the curve
dd = curve/peak - 1
max_dd = dd.min()

print(total_return, ann_return, ann_vol, sharpe, max_dd)
#Total Return = +39.7, Annual Return = 5.9% a year
# #Annual Volatility = 18.4% a year, Sharpe Ratio = 0.32
# Max Drawdown = -29.8%

# %%
def metrics(r, rf=0.04):
    r = r.dropna()
    curve = (1 + r).cumprod()
    years = len(r) / 252
    total_return = curve.iloc[-1] - 1
    ann_return = (1 + total_return) ** (1 / years) - 1
    ann_vol = r.std() * np.sqrt(252)
    sharpe = (ann_return - rf) / ann_vol

    peak = curve.cummax()
    dd = curve/peak - 1
    max_dd = dd.min()

    return {"total": total_return, "ann_return": ann_return, "sharpe": sharpe, "max_dd": max_dd}

print(metrics(strat_net))
print(metrics(returns))

# %% Look ahead bias check: What if we did not lag into the signal?
cheat_returns = returns * signal 
cheat_curve = (1 + cheat_returns).cumprod() 

ax = bh_curve.plot(label = "Buy & Hold")
strat_curve.plot(ax=ax, label = "Strategy (lagged, honest)")
cheat_curve.plot(ax=ax, label = "Strategy (no lag cheating)")
plt.legend()
plt.show()

fast_signal = (returns > 0).astype(int)    
print("honest:  ", metrics(strat_returns))
print("cheating:", metrics(cheat_returns))
print("fast, cheating:", metrics(returns * fast_signal))
print("fast, honest:  ", metrics(returns * fast_signal.shift(1)))

# %%
