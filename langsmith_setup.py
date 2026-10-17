"""
langsmith_setup.py – Creates the LangSmith dataset from labeled tickets
and runs evaluation experiments against it.

Usage:
  python langsmith_setup.py --action create_dataset
  python langsmith_setup.py --action run_experiment --model primary
  python langsmith_setup.py --action run_experiment --model cheap
  python langsmith_setup.py --action compare
"""

from __future__ import annotations

import argparse
import json
import time
from typing import Any, Dict, List

from langsmith import Client
from langsmith.evaluation import evaluate

import config
from crew import run_triage
from data.labeled_dataset import LABELED_TICKETS
from evaluators import classification_accuracy, groundedness, reply_quality


# ---------------------------------------------------------------------------
# Dataset management
# ---------------------------------------------------------------------------

def create_dataset(client: Client) -> str:
    """Upload the labeled tickets to LangSmith as a dataset."""
    # Check if dataset already exists
    datasets = list(client.list_datasets(dataset_name=config.DATASET_NAME))
    if datasets:
        print(f"[Dataset] '{config.DATASET_NAME}' already exists. Deleting and recreating.")
        client.delete_dataset(dataset_id=datasets[0].id)

    dataset = client.create_dataset(
        dataset_name=config.DATASET_NAME,
        description="80 labeled support tickets for triage evaluation (classification, reply quality, groundedness).",
    )

    examples = []
    for ticket in LABELED_TICKETS:
        examples.append(
            {
                "inputs": {"ticket_text": ticket["text"]},
                "outputs": {
                    "expected_category": ticket["expected_category"],
                    "expected_priority": ticket["expected_priority"],
                    "reference_reply": ticket["reference_reply"],
                },
            }
        )

    client.create_examples(
        inputs=[e["inputs"] for e in examples],
        outputs=[e["outputs"] for e in examples],
        dataset_id=dataset.id,
    )

    print(f"[Dataset] Created '{config.DATASET_NAME}' with {len(examples)} examples.")
    return dataset.id


# ---------------------------------------------------------------------------
# Target function (wraps crew.run_triage for LangSmith evaluate)
# ---------------------------------------------------------------------------

def _make_target(use_cheap_model: bool):
    def target(inputs: Dict[str, Any]) -> Dict[str, Any]:
        result = run_triage(inputs["ticket_text"], use_cheap_model=use_cheap_model)
        return result
    return target


# ---------------------------------------------------------------------------
# Run experiment
# ---------------------------------------------------------------------------

def run_experiment(client: Client, use_cheap_model: bool = False) -> None:
    model_tag = "cheap_model" if use_cheap_model else "primary_model"
    experiment_prefix = f"triage-{model_tag}"

    print(f"[Experiment] Running '{experiment_prefix}' against '{config.DATASET_NAME}'...")

    results = evaluate(
        _make_target(use_cheap_model),
        data=config.DATASET_NAME,
        evaluators=[classification_accuracy, reply_quality, groundedness],
        experiment_prefix=experiment_prefix,
        metadata={
            "model": config.CHEAP_MODEL if use_cheap_model else config.PRIMARY_MODEL,
            "confidence_threshold": config.CONFIDENCE_THRESHOLD,
            "top_k_retrieval": 4,
        },
        max_concurrency=1,  # Sequential to respect rate limits
    )

    print(f"[Experiment] Completed. View results in LangSmith project '{config.LANGCHAIN_PROJECT}'.")
    return results


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LangSmith dataset and experiment manager")
    parser.add_argument(
        "--action",
        choices=["create_dataset", "run_experiment", "compare"],
        required=True,
    )
    parser.add_argument("--model", choices=["primary", "cheap"], default="primary")
    args = parser.parse_args()

    client = Client(api_key=config.LANGCHAIN_API_KEY)

    if args.action == "create_dataset":
        create_dataset(client)

    elif args.action == "run_experiment":
        use_cheap = args.model == "cheap"
        run_experiment(client, use_cheap_model=use_cheap)

    elif args.action == "compare":
        print("[Compare] Running primary model experiment...")
        run_experiment(client, use_cheap_model=False)
        print("[Compare] Running cheap model experiment...")
        run_experiment(client, use_cheap_model=True)
        print(
            f"[Compare] Both experiments complete. "
            f"Compare in LangSmith at: https://smith.langchain.com/projects/{config.LANGCHAIN_PROJECT}"
        )
