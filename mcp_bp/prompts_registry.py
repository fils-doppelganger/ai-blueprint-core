"""Loads prompt personas from ``./prompts`` and prepares them for MCP.

Each prompt is exposed by name. When invocation arguments are supplied, a
short instruction block is *prepended* to the persona body (the persona files
themselves contain no placeholder syntax), so a client can, for example,
target a specific URL or repository.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .content import read_prompt_file


@dataclass(frozen=True)
class PromptArg:
    name: str
    description: str
    required: bool = False


@dataclass(frozen=True)
class PromptSpec:
    """Declarative description of a registered prompt."""

    name: str
    filename: str
    title: str
    description: str
    args: list[PromptArg] = field(default_factory=list)


# Registry of prompt personas living in ./prompts ------------------------

PROMPT_SPECS: list[PromptSpec] = [
    PromptSpec(
        name="fair_assessment_interview",
        filename="fairAssessmentInterview.md",
        title="FAIR Assessment Interview",
        description=(
            "Structured 6-phase interview that assesses a repository's "
            "alignment with the NIAID Blueprint and produces a gap report."
        ),
    ),
    PromptSpec(
        name="fair_self_assessment",
        filename="contextPrompt.md",
        title="FAIR Self-Assessment (verbose)",
        description=(
            "Consultant persona that walks pillar-by-pillar through the "
            "Blueprint to assess current practices."
        ),
    ),
    PromptSpec(
        name="fair_self_assessment_short",
        filename="contextPromptShort.md",
        title="FAIR Self-Assessment (concise)",
        description="Concise version of the pillar-by-pillar self-assessment.",
    ),
    PromptSpec(
        name="fair_web_assessor",
        filename="fairAssessorAgentOpenCode.md",
        title="FAIR Web Resource Assessor",
        description=(
            "Fetches a web resource and scores it against the Blueprint. "
            "Provide a target URL (and optionally an alternate Blueprint URL)."
        ),
        args=[
            PromptArg("url", "The web resource URL to assess.", required=True),
            PromptArg(
                "blueprint_url",
                "Alternate Blueprint URL to assess against.",
                required=False,
            ),
        ],
    ),
    PromptSpec(
        name="work_plan_interview",
        filename="workPlanInterview.md",
        title="Work Plan Intake Interview",
        description=(
            "Intake interview that ends in a FAIRification Work Plan. "
            "Optionally provide the target repository name."
        ),
        args=[
            PromptArg(
                "repo_name",
                "Name of the target repository for the Work Plan.",
                required=False,
            ),
        ],
    ),
]

PROMPT_SPECS_BY_NAME: dict[str, PromptSpec] = {s.name: s for s in PROMPT_SPECS}


def _instruction_block(spec: PromptSpec, values: dict[str, str | None]) -> str:
    """Build a short instruction block from supplied argument values."""

    provided = {
        arg.name: values.get(arg.name)
        for arg in spec.args
        if values.get(arg.name)
    }
    if not provided:
        return ""

    lines = ["> **Session parameters for this run:**"]
    for name, value in provided.items():
        label = name.replace("_", " ").title()
        lines.append(f"> - {label}: {value}")
    lines.append(
        "> Use the parameters above as the authoritative inputs for this "
        "session, overriding any example values that appear below."
    )
    return "\n".join(lines) + "\n\n---\n\n"


def render_prompt(name: str, **values: str | None) -> str:
    """Return the prompt body, optionally prefixed with an instruction block."""

    spec = PROMPT_SPECS_BY_NAME.get(name)
    if spec is None:
        raise ValueError(f"Unknown prompt: {name!r}")

    body = read_prompt_file(spec.filename)
    block = _instruction_block(spec, values)
    return f"{block}{body}".strip() + "\n"


def list_prompt_specs() -> list[dict[str, object]]:
    """Return a serializable summary of all registered prompts."""

    return [
        {
            "name": spec.name,
            "title": spec.title,
            "description": spec.description,
            "filename": spec.filename,
            "arguments": [
                {
                    "name": arg.name,
                    "description": arg.description,
                    "required": arg.required,
                }
                for arg in spec.args
            ],
        }
        for spec in PROMPT_SPECS
    ]
