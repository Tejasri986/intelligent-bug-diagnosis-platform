
from pydantic import BaseModel, Field
from typing import Literal


class TriageResult(BaseModel):
    report_id: str

    severity: Literal[
        "Critical",
        "High",
        "Medium",
        "Low"
    ]

    priority: Literal[
        "P0",
        "P1",
        "P2",
        "P3"
    ]

    affected_component: str

    confidence_score: float = Field(
        ge=0,
        le=100,
        description="Confidence score between 0 and 100"
    )

    reasoning: str


def classify_severity(text: str) -> str:
    text = text.lower()

    critical_keywords = [
        "data loss",
        "security breach",
        "data corruption",
        "system-wide failure",
        "complete system failure",
        "system completely down",
        "critical service outage"
    ]

    high_keywords = [
        "application crash",
        "application fails",
        "application failure",
        "app crashes",
        "system crash",
        "unable to login",
        "service unavailable",
        "major functionality failure",
        "database connection failed",
        "database connection failure",
        "database unavailable",
        "connection refused",
        "connection timeout",
        "server unavailable"
    ]

    medium_keywords = [
        "incorrect result",
        "feature not working",
        "functionality issue",
        "unexpected behavior",
        "request failed",
        "query failed",
        "database error"
    ]

    low_keywords = [
        "ui issue",
        "alignment issue",
        "color issue",
        "minor warning",
        "cosmetic issue",
        "spelling mistake"
    ]

    if any(keyword in text for keyword in critical_keywords):
        return "Critical"

    elif any(keyword in text for keyword in high_keywords):
        return "High"

    elif any(keyword in text for keyword in medium_keywords):
        return "Medium"

    elif any(keyword in text for keyword in low_keywords):
        return "Low"

    return "Medium"


def classify_priority(severity: str) -> str:
    priority_mapping = {
        "Critical": "P0",
        "High": "P1",
        "Medium": "P2",
        "Low": "P3"
    }

    return priority_mapping.get(severity, "P2")



def identify_component(text: str) -> str:
    text = text.lower()

    # Check specific UI problems before authentication keywords
    ui_keywords = [
        "button", "screen", "layout", "css",
        "alignment", "display", "ui issue",
        "not responding when clicked",
        "does not respond when clicked",
        "visual issue"
    ]

    if any(keyword in text for keyword in ui_keywords):
        return "User Interface"

    component_keywords = {
        "Database": [
            "database", "sql", "query", "mongodb",
            "postgresql", "mysql"
        ],
        "Authentication": [
            "login", "logout", "password",
            "authentication", "authorization",
            "token", "permission"
        ],
        "API": [
            "api", "endpoint", "http request",
            "rest", "response code", "request failed"
        ],
        "User Interface": [
            "ui", "button", "screen", "layout",
            "css", "alignment", "display"
        ],
        "Network": [
            "network", "connection timeout",
            "connection refused", "dns",
            "socket", "connectivity"
        ],
        "File System": [
            "file not found", "file upload",
            "file access", "directory",
            "permission denied"
        ]
    }

    for component, keywords in component_keywords.items():
        if any(keyword in text for keyword in keywords):
            return component

    return "Unknown"



def calculate_confidence(text: str, component: str) -> float:
    text = text.lower()

    severity_keywords = [
        "data loss", "security breach",
        "data corruption", "system-wide failure",
        "complete system failure", "system completely down",
        "critical service outage", "application crash",
        "application fails", "application failure",
        "app crashes", "system crash", "unable to login",
        "service unavailable", "major functionality failure",
        "database connection failed",
        "database connection failure",
        "database unavailable", "connection refused",
        "connection timeout", "server unavailable",
        "incorrect result", "feature not working",
        "functionality issue", "unexpected behavior",
        "request failed", "query failed", "database error",
        "ui issue", "alignment issue", "color issue",
        "minor warning", "cosmetic issue", "spelling mistake"
    ]

    severity_found = any(
        keyword in text for keyword in severity_keywords
    )

    if severity_found and component != "Unknown":
        return 90.0

    elif severity_found:
        return 75.0

    elif component != "Unknown":
        return 60.0

    return 35.0


def generate_reasoning(
    severity: str,
    priority: str,
    component: str,
    confidence: float
) -> str:

    return (
        f"Severity classified as {severity} and priority assigned "
        f"as {priority}. The affected component is {component}. "
        f"Classification confidence is {confidence}%."
    )


def run_triage(report_id: str, text: str) -> TriageResult:
    severity = classify_severity(text)
    priority = classify_priority(severity)
    component = identify_component(text)
    confidence = calculate_confidence(text, component)

    reasoning = generate_reasoning(
        severity, priority, component, confidence
    )

    return TriageResult(
        report_id=report_id,
        severity=severity,
        priority=priority,
        affected_component=component,
        confidence_score=confidence,
        reasoning=reasoning
    )
