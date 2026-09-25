"""
08 — @environment
Concept : env vars from your shell VANISH on a remote worker.
          @environment captures a value at launch and injects it into the step.
Use case: same deploy flow pointing at staging vs prod model registry

Run (staging): python flows/08_model_deploy_env.py run
Run (prod)   : MODEL_ENV=prod python flows/08_model_deploy_env.py run
   Windows PowerShell:  $env:MODEL_ENV="prod"; python flows/08_model_deploy_env.py run
"""

import os

from metaflow import FlowSpec, environment, step


class ModelDeployFlow(FlowSpec):
    """Same flow targets staging or prod based on env at launch time."""

    # os.getenv() here runs on YOUR machine, at launch.
    # @environment then injects the captured value into the task, wherever it runs.
    @environment(vars={"MODEL_REGISTRY": os.getenv("MODEL_ENV", "staging")})
    @step
    def start(self):
        self.registry = os.getenv("MODEL_REGISTRY")
        print(f"Assume churn model pushed to registry: {self.registry}")
        print("This works IDENTICALLY on a laptop or a remote AWS Batch worker.")
        self.next(self.end)

    @step
    def end(self):
        print(f"Deploy flow done. Target was: {self.registry}")


if __name__ == "__main__":
    ModelDeployFlow()
