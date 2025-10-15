import subprocess
from collections.abc import Callable
from pathlib import Path

from models.result import Result


def valid_subdirs(path: Path):
    # filter any files that are not dirs
    # filter any dirs that start with . or _ to skip dirs like .template or .git
    return [
        item for item in path.iterdir() if item.is_dir() and not item.name.startswith((".", "_"))
    ]


def _default_runner(problem_dir: Path, solution_dir: Path):
    return subprocess.run(
        ["uv", "run", "check50", "--dev", str(problem_dir)],
        cwd=solution_dir,
        capture_output=True,
        text=True,
    )


class ProblemTester:
    def __init__(self, problems_dir: Path, solutions_dir: Path, runner=None):
        self.problems_dir = problems_dir
        self.solutions_dir = solutions_dir
        self.results = []

        self.runner = runner or _default_runner

    def test_problems(self):
        for item in valid_subdirs(self.problems_dir):
            cs50_check_file = item / ".cs50.yml"
            # skip any folder that is not a valid problem
            if not cs50_check_file.exists():
                continue

            self.test_problem(item)

    def test_problem(self, problem_dir: Path):
        solutions_dir = None
        for item in valid_subdirs(self.solutions_dir):
            if problem_dir.name == item.name:
                solutions_dir = item
                break

        if not solutions_dir:
            print(f"Found no solution for {problem_dir.name}")
            return

        print(f"Testing {problem_dir.name}")
        self.test_all_solutions(problem_dir, solutions_dir)

    def is_valid_solution(name: str) -> bool:
        return name.startswith(("alt_", "valid_"))

    def is_invalid_solution(name: str) -> bool:
        return name.startswith(("fail_", "invalid_"))

    def test_all_solutions(self, problem_dir: Path, solutions_dir: Path):
        tests_run = 0

        # iterate through valid solutions & invalid solutions
        for solution_dir in solutions_dir.iterdir():
            if not solution_dir.is_dir():
                continue

            if solution_dir.name.startswith(("alt_", "valid_")):
                self.test_solution_generic(
                    problem_dir,
                    solution_dir,
                    is_passing=lambda returncode: returncode == 0,
                    solution_type="valid",
                )
                tests_run += 1
            elif solution_dir.name.startswith(("fail_", "invalid_")):
                self.test_solution_generic(
                    problem_dir,
                    solution_dir,
                    is_passing=lambda returncode: returncode != 0,
                    solution_type="invalid",
                )
                tests_run += 1

        if tests_run == 0:
            warning_result = Result(
                problem_name=problem_dir.name,
                solution_name=None,
                solution_type=None,
                result=None,
                status="warning",
                reason="No tests found",
            )
            print(warning_result.pretty_print())
            self.results.append(warning_result)

    def test_solution_generic(
        self,
        problem_dir: Path,
        solution_dir: Path,
        is_passing: Callable[
            [int], bool
        ],  # function to determine if runner_result is considered a pass
        solution_type: str = "valid",
    ):
        runner_result = self.runner(problem_dir, solution_dir)

        problem_name = problem_dir.name
        solution_name = solution_dir.name

        # determine result
        passed = is_passing(runner_result.returncode)
        result_literal = "passed" if passed else "failed"

        # determine semantic status
        status = "ok" if passed else "fail"

        result = Result(
            problem_name=problem_name,
            solution_name=solution_name,
            solution_type=solution_type,
            result=result_literal,
            status=status,
            reason=None if passed else runner_result.stdout,
        )

        print(result.pretty_print())
        self.results.append(result)
