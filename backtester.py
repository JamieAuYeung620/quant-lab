# %%
import yfinance as yf
import matplotlib.pyplot as plt
data = yf.download("AAPL", start = "2021-01-01")

# %%
print(type(data))
close = data['Close']
last5rows = close.tail(5)
plt.plot(close)
plt.show()

