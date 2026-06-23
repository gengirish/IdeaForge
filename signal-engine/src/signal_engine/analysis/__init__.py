"""Phase 2 retention analysis — delta, contradictions, kill criteria, hair-on-fire."""

from signal_engine.analysis.contradictions import ContradictionAlert, detect_contradictions
from signal_engine.analysis.delta import DeltaSummary, compute_delta
from signal_engine.analysis.hair_on_fire import (
    HAIR_ON_FIRE_WINDOW_DAYS,
    filter_hair_on_fire,
    render_hair_on_fire_analysis,
    write_hair_on_fire_analysis,
)
from signal_engine.analysis.kill_criteria import KillCriteriaAlert, evaluate_kill_criteria

__all__ = [
    "ContradictionAlert",
    "DeltaSummary",
    "HAIR_ON_FIRE_WINDOW_DAYS",
    "KillCriteriaAlert",
    "compute_delta",
    "detect_contradictions",
    "evaluate_kill_criteria",
    "filter_hair_on_fire",
    "render_hair_on_fire_analysis",
    "write_hair_on_fire_analysis",
]
