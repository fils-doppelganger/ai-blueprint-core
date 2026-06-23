#!/usr/bin/env python3
"""Save Model Influence Statement responses and rendered outputs."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

ROLE_OPTIONS = [
    "Conceptualization",
    "Data curation",
    "Formal analysis",
    "Funding acquisition",
    "Investigation",
    "Methodology",
    "Project administration",
    "Resources",
    "Software",
    "Supervision",
    "Validation",
    "Visualization",
    "Writing - original draft",
    "Writing - review & editing",
]

TRAINING_OPTIONS = ("yes", "no", "unknown")

MODEL_FIELDS = (
    "modelName",
    "author",
    "version",
    "descriptionLink",
    "license",
    "task",
    "co2Emissions",
    "paperLink",
    "baseModel",
    "pid",
)

RESPONSIBILITY_STATEMENT = (
    "The contents of this publication are solely the responsibility of the listed "
    "authors. It is the responsibility of the listed authors to verify that all "
    "AI-generated code in this work executes as intended."
)


def value_or_unknown(value: Any) -> str:
    if value is None:
        return "unknown"
    text = str(value).strip()
    return text if text else "unknown"


def value_or_empty(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    return text


def visible_models(form: dict[str, Any]) -> list[dict[str, Any]]:
    if form.get("usedModel") != "yes":
        return []
    models = form.get("models") or []
    if form.get("disclosureScope") == "single":
        return models[:1]
    return models


def disclosed_roles(form: dict[str, Any]) -> list[str]:
    roles = list(form.get("roles") or [])
    custom = value_or_empty(form.get("customRoles"))
    if custom:
        roles.extend(item.strip() for item in custom.split(",") if item.strip())
    return roles


def build_safe_name(title: str) -> str:
    safe = re.sub(
        r"[^a-z0-9]+", "-", (title or "model-influence-statement").strip(), flags=re.I
    )
    safe = safe.strip("-").lower()
    return safe or "model-influence-statement"


def build_statement_text(form: dict[str, Any]) -> str:
    """Plain-text statement matching upstream buildStatementText.

    Kept for parity with the upstream app and exercised by the test suite. The
    skill's file outputs use ``build_statement_markdown`` and
    ``build_acknowledgment_text``; this plain-text form is not written to disk.
    """
    models = visible_models(form)
    roles = disclosed_roles(form)
    lines = [
        "Model Influence Statement",
        "",
        "Responsibility Statement",
        RESPONSIBILITY_STATEMENT,
        "",
        f"Work title: {value_or_unknown(form.get('workTitle'))}",
        f"Authors: {value_or_unknown(form.get('authors'))}",
        "Did you use a machine-learning model in the creation of this work? "
        f"{form.get('usedModel', 'unknown')}",
        "",
    ]

    if form.get("usedModel") == "no":
        lines.extend(
            [
                "No machine-learning model was used in the creation of this work.",
                f"Signed by: {value_or_unknown(form.get('noModelSignature'))}",
                f"Date: {value_or_unknown(form.get('noModelDate'))}",
            ]
        )
        return "\n".join(lines)

    scope = (
        "one model" if form.get("disclosureScope") == "single" else "multiple models"
    )
    lines.extend([f"Disclosure scope: {scope}", "", "Model Information", ""])

    for index, model in enumerate(models, start=1):
        lines.append(f"Model Entry {index}")
        lines.append(f"- Model name: {value_or_unknown(model.get('modelName'))}")
        lines.append(
            f"- Author or organization: {value_or_unknown(model.get('author'))}"
        )
        lines.append(f"- Version: {value_or_unknown(model.get('version'))}")
        lines.append(
            f"- Description or training-data link: {value_or_unknown(model.get('descriptionLink'))}"
        )
        lines.append(f"- Model license: {value_or_unknown(model.get('license'))}")
        lines.append(
            f"- Task performed in this work: {value_or_unknown(model.get('task'))}"
        )
        lines.append(f"- CO2 emissions: {value_or_unknown(model.get('co2Emissions'))}")
        lines.append(
            f"- Link to paper or documentation: {value_or_unknown(model.get('paperLink'))}"
        )
        lines.append(f"- Base model: {value_or_unknown(model.get('baseModel'))}")
        lines.append(f"- PID: {value_or_unknown(model.get('pid'))}")
        lines.append("")

    lines.extend(
        [
            "Training Data Disclosure",
            f"- Publicly available open-source code: {form.get('trainingOpenSource', 'unknown')}",
            f"- Proprietary code: {form.get('trainingProprietary', 'unknown')}",
            f"- Data subject to license restrictions: {form.get('trainingLicensed', 'unknown')}",
            "",
            f"Roles played by the model: {', '.join(roles) if roles else 'unknown'}",
            "",
            f"Additional disclosure: {value_or_unknown(form.get('whatElse'))}",
            f"Voluntary critical prompt disclosure: {form.get('shareCriticalPrompt', 'no')}",
        ]
    )
    if form.get("shareCriticalPrompt") == "yes":
        lines.append(
            f"Critical prompt or prompt summary: {value_or_unknown(form.get('criticalPrompt'))}"
        )
    lines.extend(
        [
            f"Ethical considerations: {value_or_unknown(form.get('ethics'))}",
            "",
            f"Signed by: {value_or_unknown(form.get('finalSignature'))}",
            f"Date: {value_or_unknown(form.get('finalDate'))}",
        ]
    )
    return "\n".join(lines)


def _core_disclosure_header(form: dict[str, Any]) -> list[str]:
    """Work metadata and Q1 line opening the Core Disclosure section."""
    return [
        "## Core Disclosure",
        "",
        f"- Work title: `{value_or_unknown(form.get('workTitle'))}`",
        f"- Authors: `{value_or_unknown(form.get('authors'))}`",
        "- Did you use a machine-learning model in the creation of this work? "
        f"`{form.get('usedModel', 'unknown')}`",
    ]


def build_statement_markdown(form: dict[str, Any]) -> str:
    """Markdown statement with section headings per example-influence-statement.md."""
    models = visible_models(form)
    roles = disclosed_roles(form)
    lines = [
        "# Model Influence Statement",
        "",
        "## Responsibility Statement",
        "",
        RESPONSIBILITY_STATEMENT,
        "",
        *_core_disclosure_header(form),
    ]

    if form.get("usedModel") == "no":
        lines.extend(
            [
                "",
                "> No machine-learning model was used in the creation of this work.",
                "",
                f"- Signature: `{value_or_unknown(form.get('noModelSignature'))}`",
                f"- Date: `{value_or_unknown(form.get('noModelDate'))}`",
            ]
        )
        return "\n".join(lines)

    scope = (
        "one model" if form.get("disclosureScope") == "single" else "multiple models"
    )
    lines.extend([f"- Disclosure scope: `{scope}`", "", "## Model Information", ""])

    for index, model in enumerate(models, start=1):
        lines.extend(
            [
                f"### Model Entry {index}",
                "",
                f"- Model name: `{value_or_unknown(model.get('modelName'))}`",
                f"- Author or organization: `{value_or_unknown(model.get('author'))}`",
                f"- Version: `{value_or_unknown(model.get('version'))}`",
                f"- Description or training-data link: "
                f"`{value_or_unknown(model.get('descriptionLink'))}`",
                f"- Model license: `{value_or_unknown(model.get('license'))}`",
                f"- Task performed in this work: `{value_or_unknown(model.get('task'))}`",
                f"- CO2 emissions: `{value_or_unknown(model.get('co2Emissions'))}`",
                f"- Link to paper or documentation: `{value_or_unknown(model.get('paperLink'))}`",
                f"- Base model: `{value_or_unknown(model.get('baseModel'))}`",
                f"- PID: `{value_or_unknown(model.get('pid'))}`",
                "",
            ]
        )

    lines.extend(
        [
            "## Training Data Disclosure",
            "",
            f"- Publicly available open-source code: `{form.get('trainingOpenSource', 'unknown')}`",
            f"- Proprietary code: `{form.get('trainingProprietary', 'unknown')}`",
            f"- Data subject to license restrictions: `{form.get('trainingLicensed', 'unknown')}`",
            "",
            "## Roles Played by the Model",
            "",
        ]
    )
    if roles:
        lines.extend(f"- {role}" for role in roles)
    else:
        lines.append("- unknown")
    lines.extend(
        [
            "",
            "## Additional Disclosure",
            "",
            value_or_unknown(form.get("whatElse")),
            "",
            "## Critical Prompt Disclosure",
            "",
            f"- Voluntary critical prompt disclosure: `{form.get('shareCriticalPrompt', 'no')}`",
        ]
    )
    if form.get("shareCriticalPrompt") == "yes":
        lines.append(
            f"- Critical prompt or prompt summary: `{value_or_unknown(form.get('criticalPrompt'))}`"
        )
    lines.extend(
        [
            "",
            "## Ethical Considerations",
            "",
            value_or_unknown(form.get("ethics")),
            "",
            "## Final Certification",
            "",
            f"- Signature: `{value_or_unknown(form.get('finalSignature'))}`",
            f"- Date: `{value_or_unknown(form.get('finalDate'))}`",
        ]
    )
    return "\n".join(lines)


def build_acknowledgment_text(form: dict[str, Any]) -> str:
    """One-paragraph acknowledgment summary per upstream buildAcknowledgmentText."""
    work_title = value_or_empty(form.get("workTitle")) or "this work"

    if form.get("usedModel") == "no":
        return (
            f'The authors of "{work_title}" report that no machine-learning model was '
            "used in the creation of this work."
        )

    models = visible_models(form)
    roles = disclosed_roles(form)
    model_parts: list[str] = []
    for model in models:
        model_name = value_or_empty(model.get("modelName")) or "an unspecified model"
        details = [
            value_or_empty(model.get("author")),
            f"version {value_or_empty(model.get('version'))}"
            if value_or_empty(model.get("version"))
            else "",
        ]
        details = [d for d in details if d]
        model_parts.append(
            f"{model_name} ({', '.join(details)})" if details else model_name
        )
    model_summary = "; ".join(model_parts)
    task_summary = "; ".join(
        value_or_empty(m.get("task")) for m in models if value_or_empty(m.get("task"))
    )

    training_values = (
        form.get("trainingOpenSource", "unknown"),
        form.get("trainingProprietary", "unknown"),
        form.get("trainingLicensed", "unknown"),
    )
    training_sentence = ""
    if any(value != "unknown" for value in training_values):
        open_source, proprietary, licensed = training_values
        training_sentence = (
            "The statement reports training exposure as publicly available open-source code "
            f"({open_source}), proprietary code ({proprietary}), and data subject to license "
            f"restrictions ({licensed})."
        )

    sentences = [
        (
            f"The authors disclose the use of {model_summary or 'an unspecified model'} "
            f'in the creation of "{work_title}".'
        ),
        f"Reported CRediT-aligned roles included {', '.join(roles)}." if roles else "",
        f"Disclosed uses included {task_summary}." if task_summary else "",
        training_sentence,
    ]

    what_else = value_or_empty(form.get("whatElse"))
    if what_else and value_or_unknown(what_else).lower() != "unknown":
        sentences.append(f"Additional disclosed context: {what_else}.")
    if form.get("shareCriticalPrompt") == "yes":
        sentences.append(
            "A critical prompt or prompt summary was also voluntarily disclosed."
        )
    ethics = value_or_empty(form.get("ethics"))
    if ethics and value_or_unknown(ethics).lower() != "unknown":
        sentences.append(f"Ethical considerations noted: {ethics}.")

    return " ".join(s for s in sentences if s)


def validate_form_data(data: dict[str, Any]) -> bool:
    if "usedModel" not in data:
        print("Error: Missing required key 'usedModel'", file=sys.stderr)
        return False
    if data["usedModel"] not in ("yes", "no"):
        print("Error: usedModel must be 'yes' or 'no'", file=sys.stderr)
        return False
    if data["usedModel"] == "yes":
        models = data.get("models")
        if not isinstance(models, list) or not models:
            print(
                "Error: usedModel is 'yes' but 'models' is missing or empty",
                file=sys.stderr,
            )
            return False
    return True


def save_statement(data: dict[str, Any], output_dir: str = ".") -> tuple[str, str, str]:
    """Save JSON, markdown statement, and acknowledgment text with timestamps."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = build_safe_name(str(data.get("workTitle", "")))

    json_path = output_path / f"model_influence_statement_{timestamp}.json"
    md_path = output_path / f"{safe_name}-statement_{timestamp}.md"
    ack_path = output_path / f"{safe_name}-acknowledgment_{timestamp}.txt"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(build_statement_markdown(data))

    with open(ack_path, "w", encoding="utf-8") as f:
        f.write(build_acknowledgment_text(data))

    return str(json_path), str(md_path), str(ack_path)


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: save_statement.py <json_data> [output_dir]",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        data = json.loads(sys.argv[1])
    except json.JSONDecodeError as exc:
        print(f"Error: Invalid JSON data: {exc}", file=sys.stderr)
        sys.exit(1)

    if not validate_form_data(data):
        sys.exit(1)

    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    try:
        json_path, md_path, ack_path = save_statement(data, output_dir)
        print(
            json.dumps(
                {
                    "status": "success",
                    "json_file": json_path,
                    "statement_file": md_path,
                    "acknowledgment_file": ack_path,
                    "message": "Model influence statement saved successfully",
                },
                indent=2,
            )
        )
    except OSError as exc:
        print(f"Error saving statement: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
