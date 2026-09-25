"""
06 — STATIC BRANCHES (parallel + join)
Concept : self.next(a, b) forks; the join step receives `inputs`
Use case: champion vs challenger — DecisionTree vs LogisticRegression

Run:  python flows/06_credit_bakeoff.py run
Graph: python flows/06_credit_bakeoff.py show
"""

from metaflow import FlowSpec, step


class CreditRiskBakeoff(FlowSpec):
    """Two model families race in parallel; the join picks a winner."""

    @step
    def start(self):
        self.dataset = "loan_defaults_2026Q2"
        print("Loan-default dataset ready -> forking two trainers")
        self.next(self.train_tree, self.train_logreg)

    @step
    def train_tree(self):
        # Assume DecisionTree trained + cross-validated here.
        self.auc = 0.86
        print(f"Assume DecisionTree evaluated -> AUC {self.auc}")
        self.next(self.pick_winner)

    @step
    def train_logreg(self):
        # Assume LogisticRegression trained + cross-validated here.
        self.auc = 0.83
        print(f"Assume LogisticRegression evaluated -> AUC {self.auc}")
        self.next(self.pick_winner)

    @step
    def pick_winner(self, inputs):
        # BOTH branches wrote self.auc -> Metaflow refuses to guess.
        # You must resolve the conflict explicitly.
        self.winner = max(
            [("DecisionTree", inputs.train_tree.auc),
             ("LogisticRegression", inputs.train_logreg.auc)],
            key=lambda m: m[1],
        )
        # Carry forward all NON-conflicting artifacts (e.g. self.dataset)
        self.merge_artifacts(inputs, exclude=["auc"])
        self.next(self.end)

    @step
    def end(self):
        print(f"Dataset: {self.dataset}")
        print(f"CHAMPION -> {self.winner[0]} (AUC {self.winner[1]}) -> promote to prod")


if __name__ == "__main__":
    CreditRiskBakeoff()
