# 24/7 runtime

Claude Code builds. It does not trade.

Trader: Python `trading_rookie paper` (later live) under systemd or Docker on a Hostinger VPS. One process. Restart=always. Logs to disk. HALT file stops orders.

Supervisor: OpenClaw on the same VPS if Ozirus wants chat control. Allowed: status, HALT, unhalt. Forbidden: placing orders, holding Kalshi private keys in a prompt, calling a model per market tick.

Hostinger is a separate bill from the 50 USD bankroll. Do not buy a VPS from this repo automatically.

Suggested unit: restart on-failure, WorkingDirectory=repo, EnvironmentFile=.env, ExecStart=venv python -m trading_rookie paper
