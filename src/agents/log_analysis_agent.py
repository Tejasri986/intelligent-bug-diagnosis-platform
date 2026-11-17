
import re
from typing import Optional

from pydantic import BaseModel, Field


class LogAnalysisResult(BaseModel):
    exception_type: Optional[str] = None
    error_message: Optional[str] = None
    failure_file: Optional[str] = None
    failure_class: Optional[str] = None
    failure_method: Optional[str] = None
    failure_line: Optional[int] = None
    probable_code_path: list[str] = Field(default_factory=list)
    confidence_score: float = 0.0
    reasoning: str = "No log information available."


def analyze_logs(log_text: str) -> LogAnalysisResult:

    if not log_text or not log_text.strip():
        return LogAnalysisResult()

    # Detect Python exception types
    exception_match = re.search(
        r"^\s*([A-Za-z_][A-Za-z0-9_.]*(?:Exception|Error)):\s*(.*)$",
        log_text,
        re.MULTILINE
    )

    # Extract Python exception message
    error_message = None
    if exception_match:
        error_message = exception_match.group(2).strip()

    # Detect ERROR, FATAL or CRITICAL log messages
    if not error_message:
        error_match = re.search(
            r"(?:ERROR|FATAL|CRITICAL)[:\s-]+(.+)",
            log_text,
            re.IGNORECASE
        )
        if error_match:
            error_message = error_match.group(1).strip()

    # Detect Python traceback location
    file_match = re.search(
        r'File "([^"]+)", line (\d+), in ([A-Za-z_][A-Za-z0-9_]*)',
        log_text
    )

    # Detect Java-style class and method
    class_match = re.search(
        r"\bat\s+([A-Za-z_$][A-Za-z0-9_$.]*)\.[A-Za-z_$][A-Za-z0-9_$]*",
        log_text
    )

    # Extract code path
    code_path = []

    for line in log_text.splitlines():
        if " at " in line or 'File "' in line:
            code_path.append(line.strip())

    # Calculate preliminary confidence
    confidence = 85.0 if exception_match else (
        65.0 if error_message else 50.0
    )

    return LogAnalysisResult(
        exception_type=(
            exception_match.group(1) if exception_match else None
        ),
        error_message=error_message,
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
            int(file_match.group(2)) if file_match else None
        ),
        probable_code_path=code_path,
        confidence_score=confidence,
        reasoning=(
            "Exception type, message and traceback information detected."
            if exception_match and file_match
            else "Error information detected in logs."
            if error_message or exception_match
            else "Limited error information detected in logs."
        )
    )
