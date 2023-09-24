"""Collection for stats about code"""

PYLINT_FILE_NAME = "pylint.txt"
PYLINT_STATUS_NAME = "pylint_status.txt"
MYPY_FILE_NAME = "mypy.txt"
MYPY_STATUS_NAME = "mypy_status.txt"
COVERAGE_FILE_NAME = "coverage.log"
COVERAGE_STATUS_NAME = "coverage_status.log"
LINTERS_FILE_NAME = "linters.txt"
LIBRARY_NAME = "DroneVis"


def get_pylint_data() -> str:
    """Retrieve pylint data"""
    pylint_errors = ""
    with open(PYLINT_FILE_NAME, "r", encoding="utf-8") as pylint_file:
        for line in pylint_file.readlines():
            pylint_errors += "\t" + line
    stat_data = ""
    with open(PYLINT_STATUS_NAME, "r", encoding="utf-8") as pylint_file:
        stat_data = pylint_file.readline()

    pylint_status: bool = int(stat_data) == 0
    if pylint_status:
        pylint_data = "* Pylint: ran :ok:"
    else:
        pylint_data = (
            "* <details><summary>Pylint: problems :warning: "
            + "(click for details)</summary>\n"
        )
        pylint_data += f"\n\t```\n{pylint_errors}\t```\n"
        pylint_data += "</details>"
    return pylint_data


def get_mypy_data() -> str:
    """Retrieve mypy stats"""
    mypy_errors = ""
    with open(MYPY_FILE_NAME, "r", encoding="utf-8") as mypy_file:
        for line in mypy_file.readlines():
            mypy_errors += "\t" + line
    stat_data = ""
    with open(MYPY_STATUS_NAME, "r", encoding="utf-8") as mypy_file:
        stat_data = mypy_file.readline()

    mypy_status: bool = int(stat_data) == 0
    mypy_data: str = " "
    if mypy_status:
        mypy_data = "* Mypy: ran :ok:"
    else:
        mypy_data = "* <details><summary>Mypy: problems :warning: (click for details)</summary>\n"
        mypy_data += f"\n\t```\n{mypy_errors}\t```\n"
        mypy_data += "</details>"
    return mypy_data


def get_coverage_details() -> str:
    """Retrieve coverage stats"""
    coverage_stats = ""
    with open(COVERAGE_FILE_NAME, "r", encoding="utf-8") as coverage_file:
        for line in coverage_file.readlines():
            coverage_stats += "\t" + line
    stat_data = ""
    with open(COVERAGE_STATUS_NAME, "r", encoding="utf-8") as coverage_file:
        stat_data = coverage_file.readline()

    coverage_status: bool = int(stat_data) == 0
    if coverage_status:
        coverage_data = (
            "* <details><summary>Coverage: ran :ok: (click for details)</summary>\n"
        )
        coverage_data += f"\n\t```\n{coverage_stats}\t```\n"
        coverage_data += "</details>"

    else:
        coverage_data = "* Coverage: problems :warning:"
    return coverage_data


def main() -> None:
    """Main script for collecting stats"""
    linters_data = f"#### Linters stats for {LIBRARY_NAME} PR\n"
    linters_data += get_pylint_data() + "\n\n"
    linters_data += get_mypy_data() + "\n\n"
    linters_data += get_coverage_details()

    with open(LINTERS_FILE_NAME, "w", encoding="utf-8") as linters_file:
        linters_file.write(linters_data)


if __name__ == "__main__":
    main()
