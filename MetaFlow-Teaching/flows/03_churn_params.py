"""
03 — PARAMETERS
Concept : Parameter() auto-generates CLI flags; frozen, read-only inside steps
Use case: tuning a churn model without editing pipeline code

Run:  python flows/03_churn_params.py run
      python flows/03_churn_params.py run --max-depth 12 --test-split 0.3
Help: python flows/03_churn_params.py run --help
"""

from metaflow import FlowSpec, Parameter, step


class ChurnModelFlow(FlowSpec):
    """Hyperparameters as CLI parameters — no code edits between experiments."""

    max_depth = Parameter("max-depth", default=5, type=int,
                          help="Decision Tree depth")
    test_split = Parameter("test-split", default=0.2, type=float,
                           help="Holdout fraction")

    @step
    def start(self):
        print(f"Training telecom churn model | depth={self.max_depth}, holdout={self.test_split}")
        self.next(self.end)

    @step
    def end(self):
        # Assume DT trained + evaluated here; deeper tree ~ tiny accuracy bump.
        acc = 0.78 + self.max_depth * 0.004
        print(f"Assume DecisionTree(depth={self.max_depth}) evaluated -> accuracy {acc:.3f}")


if __name__ == "__main__":
    ChurnModelFlow()
