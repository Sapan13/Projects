"""
02 — ARTIFACTS
Concept : anything assigned to self.* is versioned and travels between steps
Use case: tracking a UPI fraud model's AUC across the pipeline

Run:  python flows/02_fraud_artifacts.py run
Then: python flows/02_fraud_artifacts.py dump <run-id>/end
"""

from metaflow import FlowSpec, step


class FraudModelArtifacts(FlowSpec):
    """Metrics flow through steps as versioned artifacts."""

    @step
    def start(self):
        self.dataset_rows = 500_000      # artifact 1
        self.baseline_auc = 0.81         # artifact 2 (last month's model)
        print(f"UPI txns loaded: {self.dataset_rows:,}, baseline AUC: {self.baseline_auc}")
        self.next(self.train)

    @step
    def train(self):
        # Assume XGBoost trained here on amount, hour, device, merchant.
        self.new_auc = self.baseline_auc + 0.03   # -> 0.84
        print(f"Assume XGBoost trained -> new AUC = {self.new_auc:.2f}")
        self.next(self.end)

    @step
    def end(self):
        # `start` ran in a different process, yet its artifacts are still here.
        verdict = "PROMOTE" if self.new_auc > self.baseline_auc else "KEEP OLD"
        print(f"Baseline {self.baseline_auc} vs New {self.new_auc:.2f} -> {verdict}")


if __name__ == "__main__":
    FraudModelArtifacts()
