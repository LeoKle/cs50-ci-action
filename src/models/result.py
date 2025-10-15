from typing import Literal

from pydantic import BaseModel


class Result(BaseModel):
    problem_name: str
    solution_name: str | None = None  # None if no tests were found
    solution_type: Literal["valid", "invalid"] | None = None
    result: Literal["passed", "failed"] | None = None  # actual test result
    status: Literal["ok", "fail", "warning"]  # semantic meaning
    reason: str | None = None

    def pretty_print(self) -> str:
        if self.status == "ok":
            return f"✅\t{self.problem_name} - {self.solution_name or 'No solution'}"
        elif self.status == "fail":
            return f"🔴\t{self.problem_name} - {self.solution_name or 'Failed'}"
        else:  # warning
            return f"⚠️\t{self.problem_name} - {self.reason or 'No tests found'}"
