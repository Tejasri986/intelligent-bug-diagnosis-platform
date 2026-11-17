from pydantic import BaseModel
from typing import Optional


class LogAnalysisResult(BaseModel):
    exception_type: Optional[str] = None
    error_message: Optional[str] = None
    failure_file: Optional[str] = None
    failure_class: Optional[str] = None
    failure_method: Optional[str] = None
    failure_line: Optional[int] = None
    probable_code_path: list[str] = []
    confidence_score: float = 0.0
    reasoning: str = "No log information available."


def analyze_logs(log_text: str) -> LogAnalysisResult:
    import re

    if not log_text.strip():
        return LogAnalysisResult()

    exception_match = re.search(
        r"([A-Za-z_][A-Za-z0-9_.]*(?:Exception|Error))",
        log_text
    )

    error_match = re.search(
        r"(?:ERROR|FATAL|CRITICAL)[:\s-]*(.+)",
        log_text,
        re.IGNORECASE
    )

    file_match = re.search(
        r'File "([^"]+)", line (\d+), in ([A-Za-z_][A-Za-z0-9_]*)',
        log_text
    )

    class_match = re.search(
        r"\bat ([A-Za-z_][A-Za-z0-9_.]*)\.",
        log_text
    )

    line_match = re.search(
        r":(\d+)(?::\d+)?\)?$",
        log_text,
        re.MULTILINE
    )

    code_path = []

    for line in log_text.splitlines():
        if " at " in line or 'File "' in line:
            code_path.append(line.strip())

    confidence = 85.0 if exception_match else 50.0

    return LogAnalysisResult(
        exception_type=(
            exception_match.group(1) if exception_match else None
        ),
        error_message=(
            error_match.group(1).strip() if error_match else None
        ),
        failure_file=(
            file_match.group(1) if file_match else None
        ),
        failure_method=(
            file_match.group(3) if file_match else None
        ),
        failure_class=(
            class_match.group(1) if class_match else None
        ),
        failure_line=(
            int(file_match.group(2)) if file_match
            else int(line_match.group(1)) if line_match
            else None
        ),
        probable_code_path=code_path,
        confidence_score=confidence,
        reasoning=(
            "Exception information detected in logs."
            if exception_match
            else "Limited error information detected in logs."
        )
    )