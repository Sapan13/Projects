"""
12 — BONUS: EVERYTHING TOGETHER
Combines IncludeFile + Parameter + foreach + join + card in one realistic flow.
Reads the real CSV, filters against the blocklist, "trains" per device type.

Run:
python flows/12_fraud_end_to_end.py run \
    --txns data/upi_txns.csv \
    --blocklist data/blocked_merchants.txt \
    --min-amount 1000
"""

import csv
import io

from metaflow import FlowSpec, IncludeFile, Parameter, card, current, step
from metaflow.cards import Markdown, Table


class UPIFraudEndToEnd(FlowSpec):
    """A small but complete fraud pipeline."""

    txns = IncludeFile("txns", is_text=True, help="UPI transactions CSV")
    blocklist = IncludeFile("blocklist", is_text=True, help="Blocked merchant IDs")
    min_amount = Parameter("min-amount", default=1000, type=int,
                           help="Ignore txns below this amount")

    @step
    def start(self):
        # self.txns is the CSV TEXT — parse it with io.StringIO
        rows = list(csv.DictReader(io.StringIO(self.txns)))
        blocked = set(self.blocklist.split())

        self.rows = [r for r in rows if int(r["amount"]) >= self.min_amount]
        self.flagged = [r for r in self.rows if r["merchant_id"] in blocked]

        print(f"Total txns        : {len(rows)}")
        print(f"Above Rs {self.min_amount}    : {len(self.rows)}")
        print(f"Blocked merchant  : {len(self.flagged)}")

        self.devices = sorted({r["device"] for r in self.rows})
        self.next(self.train_per_device, foreach="devices")

    @step
    def train_per_device(self):
        self.device = self.input
        subset = [r for r in self.rows if r["device"] == self.device]
        frauds = sum(int(r["is_fraud"]) for r in subset)
        # Assume a device-specific fraud model trained here.
        self.stats = {"n": len(subset), "frauds": frauds}
        print(f"Assume model trained for device={self.device} "
              f"-> {len(subset)} txns, {frauds} frauds")
        self.next(self.join)

    @step
    def join(self, inputs):
        self.report = {i.device: i.stats for i in inputs}
        self.merge_artifacts(inputs, exclude=["device", "stats"])
        self.next(self.end)

    @card(type="blank")
    @step
    def end(self):
        rows = [
            [device, stats["n"], stats["frauds"]]
            for device, stats in self.report.items()
        ]
        current.card.append(Markdown("# UPI Fraud — Per-Device Report"))
        current.card.append(
            Table(data=rows, headers=["Device", "Txns", "Frauds"])
        )
        current.card.append(
            Markdown(f"Flagged (blocked merchant): **{len(self.flagged)}**")
        )

        print("Per-device report:", self.report)
        print("View card: python flows/12_fraud_end_to_end.py card view end")


if __name__ == "__main__":
    UPIFraudEndToEnd()