from models.result import Result
from utils.ansi import clean_ansi


def build_results_markdown(results: list[Result]) -> str:
    """
    Build a Markdown table + summary for a list of Result objects.
    ANSI color codes are cleaned and messages are collapsed.
    """
    passed = sum(1 for r in results if r.status == "ok")
    failed = sum(1 for r in results if r.status == "fail")
    warns = sum(1 for r in results if r.status == "warning")
    total = len(results)

    md_lines = []

    # Table header
    md_lines.extend(("| Problem | Solution | Type | Status | Message |", "|---|---|---|---|---|"))

    for r in results:
        emoji = {"ok": "✅", "fail": "🔴", "warning": "⚠️"}.get(r.status, r.status)
        reason_clean = clean_ansi(r.reason or "").replace("\n", " ")
        message = f"<details><summary>Reason</summary>{reason_clean}</details>" if r.reason else ""

        problem_name = r.problem_name
        solution_name = r.solution_name or ""
        md_lines.append(
            f"| {problem_name} | {solution_name} | {r.solution_type or ''} | {emoji} | {message} |"
        )

    # Add summary at the bottom
    md_lines.extend((
        "",
        f"## Problem Summary: {total} total",
        f"✅ Passed: {passed}",
        f"🔴 Failed: {failed}",
        f"⚠️ Warnings: {warns}",
    ))

    return "\n".join(md_lines)
