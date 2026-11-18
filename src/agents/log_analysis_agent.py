
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

    # Detect Python, Java and JavaScript exceptions
    exception_match = re.search(
        r"^\s*([A-Za-z_$][A-Za-z0-9_.$]*(?:Exception|Error)):\s*(.*)$",
        log_text,
        re.MULTILINE
    )

    # Detect Java exceptions written as "Exception in thread"
    if not exception_match:
        exception_match = re.search(
            r'Exception in thread\s+"[^"]+"\s+'
            r'([A-Za-z_$][A-Za-z0-9_.$]*(?:Exception|Error)):\s*(.*)',
            log_text
        )

    # Extract exception message
    error_message = None

    if exception_match:
        error_message = exception_match.group(2).strip()

    # Detect ERROR, FATAL or CRITICAL messages
    if not error_message:
        error_match = re.search(
            r"(?:ERROR|FATAL|CRITICAL)[:\s-]+(.+)",
            log_text,
            re.IGNORECASE
        )

        if error_match:
            error_message = error_match.group(1).strip()

    # Detect Python traceback location
    python_match = re.search(
        r'File "([^"]+)", line (\d+), in ([A-Za-z_][A-Za-z0-9_]*)',
        log_text
    )

    # Detect Java stack trace location
    java_match = re.search(
        r"\bat\s+([\w.$]+)\.([\w$<>]+)\(([^():]+\.java):(\d+)\)",
        log_text
    )

    # Detect JavaScript / Node.js stack trace location
    js_match = re.search(
        r"\bat\s+(?:(.*?)\s+\()?(.+?\.[cm]?js):(\d+):(\d+)\)?",
        log_text
    )

    failure_file = None
    failure_class = None
    failure_method = None
    failure_line = None

    # Extract Python details
    if python_match:
        failure_file = python_match.group(1)
        failure_method = python_match.group(3)
        failure_line = int(python_match.group(2))

    # Extract Java details
    elif java_match:
        failure_class = java_match.group(1)
        failure_method = java_match.group(2)
        failure_file = java_match.group(3)
        failure_line = int(java_match.group(4))

    # Extract JavaScript details
    elif js_match:
        failure_method = js_match.group(1) or None
        failure_file = js_match.group(2)
        failure_line = int(js_match.group(3))

    # Collect stack trace lines
    code_path = []

    for line in log_text.splitlines():
        stripped_line = line.strip()

        if stripped_line.startswith("at ") or 'File "' in stripped_line:
            code_path.append(stripped_line)

    # Calculate preliminary confidence
    has_location = bool(
        python_match or java_match or js_match
    )

    confidence = (
        90.0 if exception_match and has_location
        else 85.0 if exception_match
        else 75.0 if has_location
        else 65.0 if error_message
        else 50.0
    )

    # Generate reasoning
    if exception_match and has_location:
        reasoning = (
            "Exception type, message and stack trace location detected."
        )
    elif exception_match or error_message:
        reasoning = "Error information detected in logs."
    elif has_location:
        reasoning = "Stack trace location detected."
    else:
        reasoning = "Limited error information detected in logs."

    return LogAnalysisResult(
        exception_type=(
            exception_match.group(1) if exception_match else None
        ),
        error_message=error_message,
        failure_file=failure_file,
        failure_class=failure_class,
        failure_method=failure_method,
        failure_line=failure_line,
        probable_code_path=code_path,
        confidence_score=confidence,
        reasoning=reasoning
    )
