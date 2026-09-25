"""
01 — LINEAR FLOW
Concept : the basic DAG — start -> ... -> end, chained with self.next()
Use case: Swiggy's daily delivery-ETA model retrain

Run:  python flows/01_swiggy_eta.py run
"""

from metaflow import FlowSpec, step


class SwiggyETAPipeline(FlowSpec):
    """Linear pipeline: the daily delivery-ETA model retrain."""

    @step
    def start(self):
        # Every flow MUST have a step called `start`.
        # In prod: pull yesterday's delivery records from the warehouse.
        self.n_records = 2_000_000
        print(f"[INGEST] Loaded {self.n_records:,} delivery records (order -> doorstep)")
        self.next(self.clean)

    @step
    def clean(self):
        print("[CLEAN] Dropped cancelled orders, imputed missing rain flag")
        self.next(self.train)

    @step
    def train(self):
        # Assume a Gradient Boosted Tree trained here on
        # distance, restaurant prep-time, rain, rider availability.
        print("[TRAIN] Assume GBT trained: features = [distance_km, prep_time, rain, riders]")
        self.next(self.end)

    @step
    def end(self):
        # Every flow MUST have a step called `end`. It takes no self.next().
        print("[EVAL] Assume MAE evaluated = 3.2 minutes -> ship if < 4.0  OK")


if __name__ == "__main__":
    SwiggyETAPipeline()
