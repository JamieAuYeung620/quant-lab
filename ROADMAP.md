# quant-lab roadmap

One stage at a time. Each stage has a "done when" test. Tick the box, commit, move on.
Rebuild the previous stage's cell from blank before starting a new one.

Daily session shape (45–90 min):
1. `source .venv/bin/activate`
2. LeetCode: 1–2 problems from NeetCode 150, in order. 10 min cap each.
3. Backtester: the next unticked item below.
4. `git add . && git commit -m "..." && git push`

---

## Stage 0 — Environment  ✅
- [x] venv, VS Code, Python extension, yfinance/pandas/matplotlib installed
- [x] Download one ticker, plot it
- [x] Repo on GitHub, `.gitignore` excludes `.venv`

## Stage 1 — Understand the data  ✅
- [x] Daily returns: `close.pct_change()`
- [x] Cumulative return: `(1 + returns).cumprod()` matches price shape
- [x] `close` is a Series, not a one-column DataFrame

## Stage 2 — Moving averages  (in progress)
- [x] `ma20`, `ma50` via `.rolling(n).mean()`
- [x] Overlay all three on one chart with legend
- [ ] Zoom to one year with `.loc["2024"]` and eyeball the crossovers
- [ ] `notes/pandas.md` has entries for rolling, loc, overlay plotting

**Done when:** you can rebuild this cell from blank and explain why the first 49 rows of ma50 are NaN.

## Stage 3 — Signal
Turn "MA20 above MA50" into a column of 1s and 0s.
- [ ] `signal = (ma20 > ma50)` — look at it, it's True/False
- [ ] Convert to 1/0 with `.astype(int)`
- [ ] Plot signal under the price chart; check it's 1 when orange is above green
- [ ] Count how many days in / out: `signal.sum()`, `len(signal)`

**Concepts to look up:** boolean Series, `.astype`, `.shift`
**Done when:** `signal.loc["2025"]` shows 0 through the spring drop and 1 after the recovery.

## Stage 4 — Strategy returns and equity curve
This is the backtester.
- [ ] `strat_returns = signal.shift(1) * returns`
      (shift(1): today's return is earned on yesterday's signal, otherwise you're peeking)
- [ ] `strat_curve = (1 + strat_returns).cumprod()`
- [ ] `bh_curve = (1 + returns).cumprod()`
- [ ] Plot both on one chart, legend "Strategy" / "Buy & hold"

**Concepts to look up:** look-ahead bias, why shift(1) matters
**Done when:** you can say in one sentence whether the 20/50 crossover beat buy-and-hold on AAPL 2021–2026, and by roughly how much.

## Stage 5 — Transaction costs
- [ ] `trades = signal.diff().abs()` — 1 on days the signal flips, 0 otherwise
- [ ] `cost = 0.001` (10 bps per trade); `strat_returns_net = strat_returns - trades * cost`
- [ ] Re-plot the equity curve net of costs
- [ ] Count trades: `trades.sum()`

**Done when:** you know how many trades the strategy made and how much costs ate.

## Stage 6 — Metrics
Write a function `metrics(returns_series)` that returns a dict with:
- [ ] total return
- [ ] annualised return: `(1 + total) ** (252 / n_days) - 1`
- [ ] annualised vol: `returns.std() * sqrt(252)`
- [ ] Sharpe: ann_return / ann_vol
- [ ] max drawdown: `(curve / curve.cummax() - 1).min()`
- [ ] Call it on both strat and buy-and-hold, print both dicts

**Concepts to look up:** Sharpe ratio, drawdown, `.cummax()`, writing a function that returns a dict
**Done when:** you can explain each number to a non-coder.

## Stage 7 — Competition basket
- [ ] Download 5–10 tickers at once: `yf.download(["AAPL", "MSFT", ...])`
- [ ] `close` is now a DataFrame, one column per ticker; the same code runs on all columns at once
- [ ] Equal-weight the strategy returns across tickers: `.mean(axis=1)`
- [ ] Equity curve and metrics for the basket

**Done when:** one chart, basket strategy vs basket buy-and-hold.

## Stage 8 — Refactor
- [ ] Move the signal logic into a function `crossover_signal(close, fast, slow)`
- [ ] Move the backtest into a function `backtest(close, signal, cost)`
- [ ] Try fast=10, slow=30. Try 50/200. Does any pair survive costs?
- [ ] Split into files: `data.py`, `signals.py`, `backtest.py`, `metrics.py`

**Concepts to look up:** functions with parameters, importing your own files
**Done when:** changing the strategy is one line, not a rewrite.

## Stage 9 — README
- [ ] Save the final chart: `plt.savefig("equity_curve.png")`
- [ ] README.md: what it does, how to run it, the chart, one paragraph of findings
- [ ] Flip the repo to Public

**Done when:** someone at a bank could click the link and understand it in 60 seconds.

---

## Notebook sections (paper)
1. Python syntax (MATLAB → Python table)
2. Data structures (list / set / dict / string / tuple)
3. Patterns (hash map lookup, counting, check-then-add)
4. Big-O
5. Finance concepts met along the way (returns vs prices, look-ahead, Sharpe, drawdown)

## Repo notes (markdown)
- `notes/pandas.md` — verb, one-line meaning, example from your own code
- `notes/leetcode.md` — problem, pattern, complexity, one sentence
