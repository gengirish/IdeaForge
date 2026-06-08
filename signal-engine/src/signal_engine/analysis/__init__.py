"""Phase 2 retention analysis — delta, contradictions, kill criteria."""

from signal_engine.analysis.contradictions import ContradictionAlert, detect_contradictions
from signal_engine.analysis.delta import DeltaSummary, compute_delta
from signal_engine.analysis.kill_criteria import KillCriteriaAlert, evaluate_kill_criteria

__all__ = [
    "ContradictionAlert",
    "DeltaSummary",
    "KillCriteriaAlert",
    "compute_delta",
    "detect_contradictions",
    "evaluate_kill_criteria",
]
