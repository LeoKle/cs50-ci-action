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
    md_lines.append("| Problem | Solution | Type | Status | Message |")
    md_lines.append("|---|---|---|---|---|")

    for r in results:
        emoji = {"ok": "✅", "fail": "🔴", "warning": "⚠️"}.get(r.status, r.status)
        reason_clean = clean_ansi(r.reason or "").replace("\n", " ")
        message = f"<details><summary>Reason</summary>{reason_clean}</details>" if r.reason else ""

        md_lines.append(
            f"| {r.problem_name} | {r.solution_name or ''} | {r.solution_type or ''} | {emoji} | {message} |"
        )

    # Add summary at the bottom
    md_lines.append("")
    md_lines.append(f"## Problem Summary: {total} total")
    md_lines.append(f"✅ Passed: {passed}")
    md_lines.append(f"🔴 Failed: {failed}")
    md_lines.append(f"⚠️ Warnings: {warns}")

    return "\n".join(md_lines)
