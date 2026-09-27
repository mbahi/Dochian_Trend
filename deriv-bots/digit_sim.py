import random, collections
R = random.SystemRandom()
M_RET = 9.2   # Matches: total return per 1 stake on win (approx; check your proposal)
D_RET = 1.06  # Differs: total return per 1 stake on win (approx)
def digit(): return R.randrange(10)

# ---- 1. Signal strategies: does picking a "smart" digit beat 10%? ----
N = 400_000
hist = collections.deque(maxlen=100)
for _ in range(100): hist.append(digit())
wins = collections.Counter()
for _ in range(N):
    c = collections.Counter(hist)
    picks = {
      'fixed 3 (your bot)': 3,
      'coldest digit (last 100)': min(range(10), key=lambda d: c[d]),
      'hottest digit (last 100)': max(range(10), key=lambda d: c[d]),
      'repeat last digit': hist[-1],
      'last digit +1': (hist[-1]+1)%10,
    }
    nxt = digit()
    for k,p in picks.items(): wins[k] += (nxt==p)
    hist.append(nxt)
print(f"Signal test over {N:,} ticks (Matches, return {M_RET}x):")
for k,w in wins.items():
    p = w/N
    print(f"  {k:28s} win rate {p*100:5.2f}%   EV per $1 = {p*M_RET-1:+.3f}")

# ---- 2. Bankroll runs from $1.17 ----
def run(strategy, bal=1.17, target=5.0, max_trades=2000):
    base = 0.35; stake = base
    for t in range(max_trades):
        if bal >= target: return 'hit', t
        if stake > bal: stake = bal
        if stake < 0.35: return 'bust', t
        bal -= stake
        if strategy=='matches_flat':
            win = digit()==3; 
            if win: bal += stake*M_RET
        elif strategy=='matches_mart':  # recover-and-profit martingale x1.13
            win = digit()==3
            if win: bal += stake*M_RET; stake = base
            else: stake *= 1.13
        elif strategy=='differs_flat':
            win = digit()!=3
            if win: bal += stake*D_RET
        elif strategy=='differs_mart':  # classic x11 recovery
            win = digit()!=3
            if win: bal += stake*D_RET; stake = base
            else: stake *= 11
    return 'timeout', max_trades
print("\nBankroll $1.17, $0.35 min stake, goal $5.00, 20,000 runs each:")
for s in ['matches_flat','matches_mart','differs_flat','differs_mart']:
    res = collections.Counter(run(s)[0] for _ in range(20000))
    print(f"  {s:14s} reach $5: {res['hit']/200:5.1f}%   bust: {res['bust']/200:5.1f}%   neither: {res['timeout']/200:5.1f}%")
