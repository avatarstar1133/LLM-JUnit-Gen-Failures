import argparse
import csv
import json
from pathlib import Path

from prompt_builder import build_generation_prompt, load_prompt_template


def load_config(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_dataset(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    config = load_config(args.config)
    rows = load_dataset(config["dataset"]["subset_file"])
    template = load_prompt_template(config["prompt_file"])

    print(f"Experiment: {config['experiment_name']}")
    print(f"Problems loaded: {len(rows)}")
    print(f"Repair rounds: {config['repair_rounds']}")

    for problem in rows:
        prompt = build_generation_prompt(template, problem)
        print("\n" + "=" * 72)
        print(problem.get("problem_id"), problem.get("task_category", ""))

        if args.dry_run:
            print(prompt)
            continue

        # TODO after protocol freeze:
        # 1. Select ChatGPT/Gemini provider.
        # 2. Save raw response verbatim.
        # 3. Extract JUnit without manual editing.
        # 4. Compile.
        # 5. If compile fails, perform exactly one repair request.
        # 6. Recompile once, then run if compilable.
        # 7. Append result to results/experiment_results.csv.
        raise NotImplementedError("Full runner is intentionally a skeleton until protocol freeze.")


if __name__ == "__main__":
    main()
