"""
09 — @resources
Concept : declare CPU/memory PER STEP, not per pipeline.
          Locally it's a hint; on AWS Batch / Kubernetes it provisions hardware.
Use case: heavy feature-matrix step gets big memory, cheap steps stay cheap

Run:        python flows/09_feature_resources.py run
On cloud:   python flows/09_feature_resources.py run --with batch
"""

import numpy as np
from metaflow import FlowSpec, resources, step


class FeatureMatrixFlow(FlowSpec):
    """Only the heavy step asks for heavy hardware."""

    @step
    def start(self):
        # kept modest so it runs on any laptop; bump to 100_000 x 1_300 for ~1GB
        self.n_users, self.n_features = 20_000, 500
        print(f"Plan: {self.n_users:,} users x {self.n_features} features")
        self.next(self.build_features)

    @resources(cpu=2, memory=2048)     # only THIS step asks for 2 CPU / 2 GB
    @step
    def build_features(self):
        m = np.random.default_rng(42).random((self.n_users, self.n_features))
        print(f"Feature matrix built: {m.nbytes / 1024**2:.0f} MB in memory")
        # Assume a model trained on this matrix here (e.g. ALS recommender).
        self.checksum = float(np.sum(m))
        self.next(self.end)

    @step
    def end(self):
        print(f"Assume training done. Matrix checksum {self.checksum:,.0f}")
        print("On AWS Batch: run --with batch -> 2 GB provisioned for ONE step only")


if __name__ == "__main__":
    FeatureMatrixFlow()
