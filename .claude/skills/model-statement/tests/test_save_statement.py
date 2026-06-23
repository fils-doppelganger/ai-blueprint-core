"""Tests for model influence statement builders."""

from __future__ import annotations

import json
import sys
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from save_statement import (  # noqa: E402
    RESPONSIBILITY_STATEMENT,
    build_acknowledgment_text,
    build_statement_markdown,
    build_statement_text,
    save_statement,
    visible_models,
)

EXAMPLE_YES_FORM = {
    "workTitle": "Model Influence Statement",
    "authors": "Pengyin Shan, Simon Thill",
    "usedModel": "yes",
    "disclosureScope": "single",
    "models": [
        {
            "modelName": "GPT",
            "author": "OpenAI",
            "version": "5.4",
            "descriptionLink": "public internet and partner data",
            "license": "Unknown",
            "task": "Generate the code for this web app and documentation",
            "co2Emissions": "unknown",
            "paperLink": "https://deploymentsafety.openai.com/gpt-5-4-thinking/introduction",
            "baseModel": "Unknown",
            "pid": "unknown",
        }
    ],
    "trainingOpenSource": "unknown",
    "trainingProprietary": "unknown",
    "trainingLicensed": "unknown",
    "roles": [
        "Software",
        "Validation",
        "Visualization",
        "Methodology",
        "Writing - original draft",
    ],
    "customRoles": "",
    "whatElse": "The models mentioned above are used to create this web app",
    "shareCriticalPrompt": "no",
    "criticalPrompt": "",
    "ethics": "unknown",
    "finalSignature": "Pengyin Shan",
    "finalDate": "2026-04-15",
}

EXAMPLE_NO_FORM = {
    "workTitle": "Manual Analysis Study",
    "authors": "Jane Doe",
    "usedModel": "no",
    "noModelSignature": "Jane Doe",
    "noModelDate": "06/22/2026",
}


def test_responsibility_statement_is_verbatim() -> None:
    text = build_statement_text(EXAMPLE_YES_FORM)
    assert RESPONSIBILITY_STATEMENT in text


def test_yes_path_contains_required_sections() -> None:
    text = build_statement_text(EXAMPLE_YES_FORM)
    assert "Work title: Model Influence Statement" in text
    assert (
        "Did you use a machine-learning model in the creation of this work? yes" in text
    )
    assert "Disclosure scope: one model" in text
    assert "Model Entry 1" in text
    assert "- Model name: GPT" in text
    assert "- Author or organization: OpenAI" in text
    assert "- Version: 5.4" in text
    assert "- Description or training-data link:" in text
    assert "- Model license: Unknown" in text
    assert "- Task performed in this work:" in text
    assert "- CO2 emissions: unknown" in text
    assert "- Link to paper or documentation:" in text
    assert "- Base model: Unknown" in text
    assert "- PID: unknown" in text
    assert "Training Data Disclosure" in text
    assert "Roles played by the model:" in text
    assert "Writing - original draft" in text
    assert "Signed by: Pengyin Shan" in text


def test_no_path_short_circuit() -> None:
    text = build_statement_text(EXAMPLE_NO_FORM)
    assert "No machine-learning model was used in the creation of this work." in text
    assert "Signed by: Jane Doe" in text
    assert "Training Data Disclosure" not in text


def test_visible_models_respects_single_scope() -> None:
    multi = {
        **EXAMPLE_YES_FORM,
        "disclosureScope": "single",
        "models": [{"modelName": "A"}, {"modelName": "B"}],
    }
    assert len(visible_models(multi)) == 1


def test_markdown_yes_path_has_work_metadata_and_sections() -> None:
    md = build_statement_markdown(EXAMPLE_YES_FORM)
    assert "# Model Influence Statement" in md
    assert "## Responsibility Statement" in md
    assert "## Core Disclosure" in md
    assert "- Work title: `Model Influence Statement`" in md
    assert "- Authors: `Pengyin Shan, Simon Thill`" in md
    assert "## Model Information" in md
    assert "### Model Entry 1" in md
    assert "## Training Data Disclosure" in md
    assert "## Roles Played by the Model" in md
    assert "## Critical Prompt Disclosure" in md
    assert "## Final Certification" in md


def test_markdown_no_path_has_work_metadata_and_inline_certification() -> None:
    md = build_statement_markdown(EXAMPLE_NO_FORM)
    assert "- Work title: `Manual Analysis Study`" in md
    assert "- Authors: `Jane Doe`" in md
    assert "> No machine-learning model was used in the creation of this work." in md
    assert "- Signature: `Jane Doe`" in md
    assert "- Date: `06/22/2026`" in md
    assert "## Final Certification" not in md
    assert "## Model Information" not in md


def test_acknowledgment_yes_path() -> None:
    ack = build_acknowledgment_text(EXAMPLE_YES_FORM)
    assert 'in the creation of "Model Influence Statement"' in ack
    assert "Reported CRediT-aligned roles included" in ack
    assert "Writing - original draft" in ack


def test_acknowledgment_omits_training_sentence_when_all_unknown() -> None:
    # EXAMPLE_YES_FORM has all three training fields set to "unknown".
    ack = build_acknowledgment_text(EXAMPLE_YES_FORM)
    assert "training exposure" not in ack


def test_acknowledgment_includes_training_sentence_when_disclosed() -> None:
    form = {**EXAMPLE_YES_FORM, "trainingOpenSource": "yes"}
    ack = build_acknowledgment_text(form)
    assert "training exposure as publicly available open-source code" in ack


def test_acknowledgment_no_path() -> None:
    ack = build_acknowledgment_text(EXAMPLE_NO_FORM)
    assert (
        'The authors of "Manual Analysis Study" report that no machine-learning model'
        in ack
    )


def test_save_statement_writes_three_files(tmp_path: Path) -> None:
    json_path, md_path, ack_path = save_statement(EXAMPLE_YES_FORM, str(tmp_path))
    assert Path(json_path).exists()
    assert Path(md_path).exists()
    assert Path(ack_path).exists()

    saved = json.loads(Path(json_path).read_text(encoding="utf-8"))
    assert saved["usedModel"] == "yes"
    md_content = Path(md_path).read_text(encoding="utf-8")
    assert "- Work title: `Model Influence Statement`" in md_content
    assert "- Authors: `Pengyin Shan, Simon Thill`" in md_content
    assert len(Path(ack_path).read_text(encoding="utf-8")) > 50
