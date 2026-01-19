# analytics/metrics.py

import pandas as pd
from typing import List, Dict


def results_to_student_row(results: Dict) -> Dict:
    """
    Convert a single pipeline result into a flat student-level row.

    Parameters
    ----------
    results : Dict
        Output from run_assessment_pipeline.

    Returns
    -------
    Dict
        Flattened student-level record.
    """
    return {
        "student_name": results["student_name"],
        "total_correct": results["total_correct"],
        "total_questions": results["total_questions"],
        "score_percent": results["score_percent"]
    }


def aggregate_results(results_list: List[Dict]) -> pd.DataFrame:
    """
    Aggregate multiple student results into a DataFrame.

    Parameters
    ----------
    results_list : List[Dict]
        List of pipeline outputs (one per student).

    Returns
    -------
    pd.DataFrame
        Student-level results table.
    """
    rows = [results_to_student_row(r) for r in results_list]
    return pd.DataFrame(rows)


def compute_summary_metrics(df: pd.DataFrame) -> Dict:
    """
    Compute sponsor-level summary metrics.

    Parameters
    ----------
    df : pd.DataFrame
        Student-level results DataFrame.

    Returns
    -------
    Dict
        Aggregate performance metrics.
    """
    return {
        "num_students": len(df),
        "average_score": round(df["score_percent"].mean(), 2),
        "median_score": round(df["score_percent"].median(), 2),
        "pass_rate_percent": round(
            (df["score_percent"] >= 50).mean() * 100, 2
        )
    }


def compare_baseline_endline(
    baseline_df: pd.DataFrame,
    endline_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Compare baseline vs endline scores per student.

    Assumes student_name is the join key.

    Parameters
    ----------
    baseline_df : pd.DataFrame
    endline_df : pd.DataFrame

    Returns
    -------
    pd.DataFrame
        Improvement table.
    """
    merged = baseline_df.merge(
        endline_df,
        on="student_name",
        suffixes=("_baseline", "_endline")
    )

    merged["score_improvement"] = (
        merged["score_percent_endline"]
        - merged["score_percent_baseline"]
    )

    return merged
