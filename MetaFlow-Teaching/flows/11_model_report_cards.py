"""
11 — @card
Concept : @card turns a step into a visual report you can open in a browser.
          - @card                -> auto-renders the step's artifacts
          - @card(type="blank")  -> you build it from components
Use case: a daily model report your PM can open — no notebook required

Run:  python flows/11_model_report_cards.py run
View: python flows/11_model_report_cards.py card view report
      python flows/11_model_report_cards.py card view start

NOTE: this file uses only card types BUILT INTO Metaflow ("default" and "blank"),
      so nothing extra to install. If you ever see
          "MetaflowCard named html not found"
      it means a flow asked for type="html", which is a separate plugin:
          pip install metaflow-card-html
"""

from metaflow import FlowSpec, card, current, step
from metaflow.cards import Artifact, Markdown, Table


class ModelReportFlow(FlowSpec):
    """Every run produces a report card a non-engineer can open."""

    @card                                   # default card: auto-shows artifacts
    @step
    def start(self):
        # Assume the ETA model was evaluated here on yesterday's holdout.
        self.mae_old = 3.9
        self.mae_new = 3.2
        self.model_name = "swiggy_eta_v7"
        print(f"Old MAE {self.mae_old} | New MAE {self.mae_new}")
        self.next(self.report)

    @card(type="blank")                     # empty canvas we fill ourselves
    @step
    def report(self):
        improved = self.mae_new < self.mae_old
        verdict = "PROMOTE" if improved else "HOLD"
        delta = self.mae_old - self.mae_new

        # current.card.append() adds one component to the page, in order.
        current.card.append(Markdown("# Swiggy ETA Model — Daily Report"))
        current.card.append(Markdown(f"Model: **{self.model_name}**"))

        current.card.append(
            Table(
                data=[
                    ["Previous model", f"{self.mae_old} min"],
                    ["New model", f"{self.mae_new} min"],
                    ["Improvement", f"{delta:.1f} min"],
                ],
                headers=["Metric", "Value"],
            )
        )

        current.card.append(Markdown(f"## Verdict: {verdict}"))
        current.card.append(Artifact(self.mae_new))

        self.verdict = verdict
        print(f"Report card built -> verdict {verdict}")
        self.next(self.end)

    @step
    def end(self):
        print(f"Final verdict: {self.verdict}")
        print("Now run:  python flows/11_model_report_cards.py card view report")


if __name__ == "__main__":
    ModelReportFlow()