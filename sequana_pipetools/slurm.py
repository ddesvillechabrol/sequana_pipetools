from pathlib import Path
import parse
import re


class DebugJob:
    """Helper for sequana jobs debugging on slurm cluster.

    Assumptions:
    - Working on slurm
    - Only a single sequana job has been launched in the path specified.

    Usage:
    DebugJob(path_to_analysis_folder)

    :param path: Path to a working directory from a sequana pipeline execution
    (Directory containing slurm_*.out files)
    :param context: The number of lines to print around the error line.
    """

    def __init__(self, path, context=5):
        self.path = Path(path)
        self.context = context
        self.slurm_out = sorted([f for f in self.path.glob("slurm*.out")])

        if not self.slurm_out:
            raise IOError(f"No slurm*.out files were found in {path}")

        with open(self.slurm_out[0], "r") as f:
            self.snakemaster = f.read()

        self.percent = self._get_percent()
        self.errors = self._get_rules_with_errors()
        self.n_errors = len(self.errors)

    def __repr__(self):

        return self._report()

    def _report(self):

        message = "#" * 33 + " DEBUG REPORT " + "#" * 33 + "\n\n"
        message += f"The analysis reached {self.percent}%. A total of {self.n_errors} errors has been found.\n"
        message += f"Errors are comming from rule(s): {','.join(set([e['rule'] for e in self.errors]))}\n\n"

        for e in self.errors:
            message += f"Rule: {e['rule']}, SlurmID: {e['slurm_id']}\n"

            message += self._get_error_message(self.path / e["log"])
            message += self._get_error_message(
                self.path / ("slurm-" + str(e["slurm_id"]) + ".out")
            )

        message += "\n" + "#" * 80

        return message

    def _get_error_message(self, log_file):
        """Extract error message from a log file."""

        message = ""
        with open(log_file, "r") as f:

            # Get lines with "error" in:
            error_lines = [
                i
                for i, line in enumerate(f)
                if re.findall("error", line, re.IGNORECASE)
            ]

            if not error_lines:
                return "-" * 80 + f"\nNo error found in {log_file}.\n" + "-" * 80 + "\n"

            # Add a number of lines around (ie the context)
            lines_to_print = [
                list(range(i - self.context, i + self.context + 1)) for i in error_lines
            ]
            # Flats and uniquify the list of list
            lines_to_print = set([y for x in lines_to_print for y in x])

        message += "-" * 80 + "\n"
        message += f"Error messages found in {log_file} (context: {self.context}):\n"
        with open(log_file, "r") as f:
            for i, line in enumerate(f):
                if i in lines_to_print:
                    message += line

        message += "-" * 80 + "\n"
        return message

    def _get_percent(self):
        """Get at which percentage the analysis stopped"""

        step_percent = "{:d} of {:d} steps ({percent:g}%) done"

        # Get last percentage
        last_percent_parse = [x for x in parse.findall(step_percent, self.snakemaster)]
        return last_percent_parse[-1]["percent"]

    def _get_rules_with_errors(self):
        """Return name and log files of rules which returned an error.,"""

        errors = """Error in rule {rule:S}:
    jobid: {jobid:d}
    output: {output}
    log: {log:S} (check log file(s) for error message)
    cluster_jobid: Submitted batch job {slurm_id:d}"""

        return list(parse.findall(errors, self.snakemaster))
