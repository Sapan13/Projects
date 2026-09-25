"""
05 — CONFIG
Concept : Config() loads a YAML at launch time; dot-access inside the flow
Use case: same recommender flow, staging vs production settings

Run (staging): python flows/05_reco_config.py run
Run (prod)   : python flows/05_reco_config.py --config config data/prod_config.yml run

Note the syntax: --config <config-name> <path>, and it comes BEFORE `run`.
      "config" here is the attribute name below, not a literal keyword.
"""

import yaml
from metaflow import Config, FlowSpec, step


class RecoModelFlow(FlowSpec):
    """All hyperparameters live in reviewable YAML, not in code."""

    config = Config("config", default="data/model_config.yml", parser=yaml.safe_load)

    @step
    def start(self):
        print(f"Environment : {self.config.environment}")
        print(f"Model       : {self.config.model}")
        print(f"lr={self.config.learning_rate}, epochs={self.config.epochs}")
        self.next(self.end)

    @step
    def end(self):
        # Assume a two-tower recommender trained here with the config above.
        ctr = 0.031
        verdict = "SHIP" if ctr > self.config.min_ctr_threshold else "HOLD"
        print(f"Assume recommender trained -> CTR {ctr} "
              f"vs threshold {self.config.min_ctr_threshold} -> {verdict}")


if __name__ == "__main__":
    RecoModelFlow()
