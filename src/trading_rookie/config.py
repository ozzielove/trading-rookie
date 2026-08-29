from __future__ import annotations

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Runtime config. Live is opt-in. Adaptation is always on."""

    model_config = SettingsConfigDict(
        env_prefix="TRADING_ROOKIE_",
        env_file=".env",
        extra="ignore",
    )

    mode: str = Field(default="paper", description="paper | live")
    bankroll: float = Field(default=50.0, gt=0)
    risk_pct: float = Field(default=0.01, gt=0, le=0.05)
    min_weight: float = Field(default=0.05, gt=0, lt=0.5)
    learning_rate: float = Field(default=0.08, gt=0, lt=1)
    morph_rate: float = Field(default=0.04, gt=0, lt=1)
    spawn_error_threshold: float = Field(default=0.35, gt=0)
    min_history_days: int = Field(default=180, ge=180)

    @field_validator("mode")
    @classmethod
    def mode_ok(cls, v: str) -> str:
        v = v.lower().strip()
        if v not in {"paper", "live"}:
            raise ValueError("mode must be paper or live")
        return v

    def stake(self, equity: float) -> float:
        return max(0.0, equity * self.risk_pct)
