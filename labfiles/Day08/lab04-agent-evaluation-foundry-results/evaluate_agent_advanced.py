"""
Advanced Azure AI Foundry Agent Evaluation Lab

Evaluates an existing Credit Risk Assessment Agent using a JSONL test
dataset and built-in Azure AI evaluators.

Main flow:
0. Load config, then ask for a unique name (checked against Foundry).
1. Upload the test dataset (reused if the file has not changed).
2. Configure built-in evaluators.
3. Create the evaluation.
4. Run it against the existing agent.
5. Monitor the run, print the portal URL, save a versioned local summary.

Run from the lab root folder:

    python evaluate_agent_advanced.py

Full technical logs (with tracebacks) go to results/logs/.
"""

import hashlib
import json
import logging
import os
import re
import sys
import time
from datetime import datetime, timezone
from itertools import islice
from pathlib import Path

import openai
from dotenv import load_dotenv
from azure.core.exceptions import (
    ClientAuthenticationError,
    HttpResponseError,
    ResourceNotFoundError,
)
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import TestingCriterionAzureAIEvaluator
from openai.types.eval_create_params import DataSourceConfigCustom


# ---------------------------------------------------------------------------
# Paths and settings
# ---------------------------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent
DATASET_PATH = ROOT_DIR / "data" / "credit_risk_test_queries.jsonl"
RESULTS_DIR = ROOT_DIR / "results"
LOGS_DIR = RESULTS_DIR / "logs"

MIN_NAME_LENGTH = 7
NAME_PATTERN = re.compile(r"^[a-z0-9_-]+$")
POLL_SECONDS = 5
MAX_EVALS_TO_CHECK = 1000
TERMINAL_STATUSES = {"completed", "failed", "canceled", "cancelled"}

log = logging.getLogger("eval_lab")


# ---------------------------------------------------------------------------
# Logging: clean messages on screen, full detail in a log file
# ---------------------------------------------------------------------------

def setup_logging() -> Path:
    """Console shows plain messages; the log file keeps everything."""

    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOGS_DIR / f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    log.setLevel(logging.DEBUG)
    log.handlers.clear()
    log.propagate = False

    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter("%(message)s"))

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s")
    )

    log.addHandler(console)
    log.addHandler(file_handler)
    return log_file


def explain_error(exc: Exception) -> str:
    """Turn a known error into a plain-language hint. Empty if unknown."""

    text = str(exc).lower()

    if isinstance(exc, ClientAuthenticationError) or isinstance(
        exc, openai.AuthenticationError
    ):
        return (
            "Azure login failed or expired. Run 'az login' with the lab "
            "account, then try again."
        )

    if isinstance(exc, openai.PermissionDeniedError) or "403" in text:
        return (
            "Your account lacks permission on this project. Ask for the "
            "'Azure AI User' role on the Foundry project."
        )

    if "model resources are not found" in text:
        return (
            "Foundry cannot find your model deployment. Set "
            "AZURE_AI_MODEL_DEPLOYMENT_NAME in .env to the exact "
            "Deployment name from Foundry > Models + endpoints "
            "(the deployment name, not the model name)."
        )

    if isinstance(exc, (ResourceNotFoundError, openai.NotFoundError)) or (
        "404" in text
    ):
        return (
            "Resource not found. Check AZURE_AI_PROJECT_ENDPOINT in .env. "
            "It must look like "
            "https://<account>.services.ai.azure.com/api/projects/<project>. "
            "If you used AGENT_NAME, make sure that agent exists."
        )

    if isinstance(exc, FileNotFoundError):
        return "A required file is missing. Check the path in the message."

    if isinstance(exc, ValueError) and "environment variable" in text:
        return "Open the .env file in the lab root folder and fill in the value."

    if isinstance(exc, openai.APIConnectionError):
        return "Could not reach Azure. Check your internet connection or VPN."

    return ""


# ---------------------------------------------------------------------------
# Environment configuration
# ---------------------------------------------------------------------------

def require_env(name: str) -> str:
    """Return a required environment variable or fail with a clear message."""

    value = (os.getenv(name) or "").strip().strip('"').strip("'")

    if not value:
        raise ValueError(
            f"Missing required environment variable: {name}. "
            f"Add it to the .env file in the lab root folder."
        )

    return value


def validate_endpoint(endpoint: str) -> None:
    """Catch the most common .env mistake before any network call."""

    if "/api/projects/" not in endpoint or "/openai/" in endpoint:
        raise ValueError(
            "AZURE_AI_PROJECT_ENDPOINT looks wrong: "
            f"{endpoint}\n"
            "  Expected: https://<account>.services.ai.azure.com"
            "/api/projects/<project>\n"
            "  Copy it from Foundry > your project > Overview."
        )


def build_clients():
    """Load configuration and create Foundry clients."""

    load_dotenv(ROOT_DIR / ".env")

    endpoint = require_env("AZURE_AI_PROJECT_ENDPOINT")
    validate_endpoint(endpoint)
    model_deployment = require_env("AZURE_AI_MODEL_DEPLOYMENT_NAME")
    agent_name = require_env("AGENT_NAME")

    project_client = AIProjectClient(
        endpoint=endpoint,
        credential=DefaultAzureCredential(),
        allow_preview=True,
    )

    return (
        project_client,
        project_client.get_openai_client(),
        model_deployment,
        agent_name,
    )


# ---------------------------------------------------------------------------
# Result versioning
# ---------------------------------------------------------------------------

def existing_versions(user_name: str) -> list:
    """Versions already used locally for this name."""

    pattern = re.compile(rf"^{re.escape(user_name)}_summary_v(\d+)\.json$")
    return [
        int(match.group(1))
        for path in RESULTS_DIR.glob(f"{user_name}_summary_v*.json")
        if (match := pattern.match(path.name))
    ]


def summary_path(user_name: str, version: int) -> Path:
    return RESULTS_DIR / f"{user_name}_summary_v{version}.json"


def save_summary(path: Path, summary: dict) -> None:
    path.write_text(json.dumps(summary, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# Unique name (checked locally and against Foundry)
# ---------------------------------------------------------------------------

def name_used_in_foundry(openai_client, user_name: str) -> bool:
    """True if an evaluation named '<name>_vN - ...' already exists.

    If the check itself fails, warn and carry on rather than block the lab.
    """

    pattern = re.compile(rf"^{re.escape(user_name)}_v\d+ - ", re.IGNORECASE)

    try:
        for item in islice(openai_client.evals.list(limit=100), MAX_EVALS_TO_CHECK):
            if item.name and pattern.match(item.name):
                return True
    except Exception as exc:
        log.warning(
            "  Note: could not check Foundry for duplicate names "
            "(continuing without the check)."
        )
        log.debug("Duplicate-name check failed: %r", exc, exc_info=True)

    return False


def ask_for_name(openai_client) -> str:
    """Ask for a unique name until a valid, unused one is entered."""

    log.info("\n" + "=" * 60)
    log.info(" Credit Risk Agent Evaluation")
    log.info("=" * 60)
    log.info(
        "\nEnter a unique name for your evaluation run."
        "\nYou will use it later to find your run in Microsoft Foundry."
        f"\n\nRules: at least {MIN_NAME_LENGTH} characters, using letters, "
        "numbers, hyphens (-) or underscores (_). No spaces."
        "\nTip: add your initials or ID so nobody else picks the same name."
        "\nExample: uday-credit-01\n"
    )

    while True:
        try:
            name = input("Your unique name: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            log.info("\nCancelled. No evaluation was started.")
            sys.exit(1)

        if len(name) < MIN_NAME_LENGTH:
            log.info(
                f"  Too short: {len(name)} characters. "
                f"Use at least {MIN_NAME_LENGTH}.\n"
            )
            continue

        if not NAME_PATTERN.match(name):
            log.info(
                "  Use only letters, numbers, hyphens and underscores "
                "(no spaces or special characters).\n"
            )
            continue

        # Same name used before from this folder = your own re-run. Allowed.
        # Name found in Foundry but never used here = someone else's. Blocked.
        if not existing_versions(name) and name_used_in_foundry(
            openai_client, name
        ):
            log.info(
                f"  '{name}' is already used by another run in this project. "
                "Please pick a different name.\n"
            )
            continue

        log.info(f"  Using name: {name}")
        return name


# ---------------------------------------------------------------------------
# Dataset
# ---------------------------------------------------------------------------

def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def ensure_dataset(project_client):
    """Upload the dataset, or reuse it if this exact file is already there."""

    log.info("\n[1/5] Preparing credit-risk test dataset...")

    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Dataset file not found: {DATASET_PATH}")

    name = os.getenv("DATASET_NAME", "credit-risk-test-queries")
    version = file_hash(DATASET_PATH)

    try:
        dataset = project_client.datasets.get(name=name, version=version)
        log.info(f"  Dataset already uploaded, reusing: {name} v{version}")
        return dataset
    except ResourceNotFoundError:
        log.debug("Dataset %s v%s not found, uploading.", name, version)

    dataset = project_client.datasets.upload_file(
        name=name,
        version=version,
        file_path=str(DATASET_PATH),
    )
    log.info(f"  Dataset uploaded: {dataset.name} v{dataset.version}")
    return dataset


# ---------------------------------------------------------------------------
# Evaluation criteria
# ---------------------------------------------------------------------------

def create_testing_criteria(model_deployment):
    """Create built-in Azure AI evaluation criteria."""

    log.info("\n[2/5] Configuring evaluation criteria...")

    data_mapping = {
        "query": "{{item.query}}",
        "response": "{{sample.output_text}}",
    }
    judge_params = {"deployment_name": model_deployment}

    criteria = [
        TestingCriterionAzureAIEvaluator(
            type="azure_ai_evaluator",
            name="Coherence",
            evaluator_name="builtin.coherence",
            initialization_parameters=judge_params,
            data_mapping=data_mapping,
        ),
        TestingCriterionAzureAIEvaluator(
            type="azure_ai_evaluator",
            name="Violence",
            evaluator_name="builtin.violence",
            data_mapping=data_mapping,
        ),
        TestingCriterionAzureAIEvaluator(
            type="azure_ai_evaluator",
            name="Task Adherence",
            evaluator_name="builtin.task_adherence",
            initialization_parameters=judge_params,
            data_mapping=data_mapping,
        ),
    ]

    for criterion in criteria:
        log.info(f"  Added evaluator: {criterion.evaluator_name}")

    return criteria


# ---------------------------------------------------------------------------
# Create evaluation and run
# ---------------------------------------------------------------------------

def create_evaluation(openai_client, testing_criteria, label):
    """Create the Foundry evaluation, named '<name>_vN - ...'."""

    log.info("\n[3/5] Creating evaluation...")

    data_source_config = DataSourceConfigCustom(
        type="custom",
        item_schema={
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
        include_sample_schema=True,
    )

    evaluation = openai_client.evals.create(
        name=f"{label} - Credit Risk Agent Evaluation",
        data_source_config=data_source_config,
        testing_criteria=testing_criteria,
    )

    log.info(f"  Evaluation created: {evaluation.id}")
    return evaluation


def start_evaluation_run(openai_client, evaluation, dataset, agent_name, label):
    """Start an evaluation run against the existing agent."""

    log.info("\n[4/5] Starting evaluation run...")

    eval_run = openai_client.evals.runs.create(
        eval_id=evaluation.id,
        name=f"{label} - Credit Risk Agent Evaluation Run",
        data_source={
            "type": "azure_ai_target_completions",
            "source": {"type": "file_id", "id": dataset.id},
            "input_messages": {
                "type": "template",
                "template": [
                    {
                        "type": "message",
                        "role": "user",
                        "content": {
                            "type": "input_text",
                            "text": "{{item.query}}",
                        },
                    }
                ],
            },
            "target": {"type": "azure_ai_agent", "name": agent_name},
        },
    )

    log.info(f"  Evaluation run created: {eval_run.id}")
    return eval_run


# ---------------------------------------------------------------------------
# Monitor evaluation
# ---------------------------------------------------------------------------

def monitor_evaluation(openai_client, evaluation, eval_run, user_name, label):
    """Poll the run until it reaches a terminal state. Returns the run."""

    log.info("\n[5/5] Monitoring evaluation run (this can take a few minutes)...")

    last_status = None

    try:
        while True:
            run = openai_client.evals.runs.retrieve(
                run_id=eval_run.id,
                eval_id=evaluation.id,
            )

            if run.status != last_status:
                log.info(f"  Status: {run.status}")
                last_status = run.status

            if run.status in TERMINAL_STATUSES:
                return run

            time.sleep(POLL_SECONDS)
    except KeyboardInterrupt:
        log.info(
            "\nStopped watching. The run keeps going in Foundry. "
            f"Search for '{user_name}' under Evaluations to check it."
        )
        sys.exit(1)


def print_final_report(run, evaluation, eval_run, user_name, label, path):
    """Show the outcome and where to find results."""

    report_url = getattr(run, "report_url", None)
    result_counts = getattr(run, "result_counts", None)

    log.info("\n" + "=" * 60)
    if run.status == "completed":
        log.info(" Evaluation completed")
    else:
        log.info(f" Evaluation ended with status: {run.status}")
    log.info("=" * 60)
    log.info(f" Name          : {label}")
    log.info(f" Evaluation ID : {evaluation.id}")
    log.info(f" Run ID        : {eval_run.id}")
    log.info(f" Result counts : {result_counts}")
    log.info(f" Report URL    : {report_url}")

    error = getattr(run, "error", None)
    if run.status != "completed" and error:
        log.info(f" Error         : {error}")

    log.info("\nWhere to find your results:")
    log.info(f"  1. Local summary : results/{path.name}")
    log.info("  2. In detail     : Microsoft Foundry > Evaluations,")
    log.info(f"                     then search for: {user_name}")
    log.info(
        "\nRunning the script again with the same name saves a new file "
        "(_v1, _v2, _v3 ...) instead of overwriting."
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_lab() -> int:
    RESULTS_DIR.mkdir(exist_ok=True)

    project_client, openai_client, model_deployment, agent_name = build_clients()

    user_name = ask_for_name(openai_client)

    # Reserve the next version right away, so a crashed run still "uses" it
    # and the next run gets a fresh _vN in both the filename and Foundry.
    version = max(existing_versions(user_name), default=0) + 1
    label = f"{user_name}_v{version}"
    path = summary_path(user_name, version)

    summary = {
        "name": label,
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "started",
        "agent_name": agent_name,
        "use_case": "Credit Risk Assessment",
        "evaluators": [
            "builtin.coherence",
            "builtin.violence",
            "builtin.task_adherence",
        ],
    }
    save_summary(path, summary)
    log.info(f"\nThis run: {label}")
    log.debug("Summary file reserved: %s", path)

    try:
        dataset = ensure_dataset(project_client)
        summary.update(dataset=dataset.name, dataset_version=dataset.version)

        criteria = create_testing_criteria(model_deployment)
        evaluation = create_evaluation(openai_client, criteria, label)
        summary["evaluation_id"] = evaluation.id

        eval_run = start_evaluation_run(
            openai_client, evaluation, dataset, agent_name, label
        )
        summary["run_id"] = eval_run.id
        save_summary(path, summary)

        run = monitor_evaluation(
            openai_client, evaluation, eval_run, user_name, label
        )
    except Exception as exc:
        summary.update(status="error", error=str(exc))
        save_summary(path, summary)
        raise

    summary.update(
        completed_at_utc=datetime.now(timezone.utc).isoformat(),
        status=run.status,
        report_url=getattr(run, "report_url", None),
        result_counts=str(getattr(run, "result_counts", None)),
    )
    save_summary(path, summary)

    print_final_report(run, evaluation, eval_run, user_name, label, path)
    return 0 if run.status == "completed" else 1


def main() -> None:
    log_file = setup_logging()

    try:
        sys.exit(run_lab())
    except SystemExit:
        raise
    except Exception as exc:
        log.debug("Unhandled error", exc_info=True)

        log.error("\n" + "=" * 60)
        log.error(" Something went wrong")
        log.error("=" * 60)
        log.error(f" Error : {type(exc).__name__}")

        message = str(exc).strip() or "(no message)"
        for line in message.splitlines():
            log.error(f"         {line}")

        hint = explain_error(exc)
        if hint:
            log.error(f"\n How to fix:\n   {hint}")

        log.error(f"\n Full technical log: {log_file.relative_to(ROOT_DIR)}")
        sys.exit(1)


if __name__ == "__main__":
    main()