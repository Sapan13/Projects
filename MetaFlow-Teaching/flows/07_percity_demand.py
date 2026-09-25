"""
07 — FOREACH (dynamic fan-out)  ** the most-used pattern in industry **
Concept : self.next(step, foreach="list") spawns ONE TASK PER ITEM.
          Inside, self.input is this task's item.
Use case: one demand-forecast model per city

Run:  python flows/07_percity_demand.py run
Try : add 5 more cities to the list — zero other code changes
"""

from metaflow import FlowSpec, step


class PerCityDemandFlow(FlowSpec):
    """One forecasting model per city — 3 today, 300 next year, same code."""

    @step
    def start(self):
        self.cities = ["bangalore", "mumbai", "delhi"]
        print(f"Fanning out {len(self.cities)} parallel training tasks")
        # foreach takes the NAME of the artifact holding the list, as a string
        self.next(self.train_city_model, foreach="cities")

    @step
    def train_city_model(self):
        self.city = self.input          # self.input = THIS task's city
        # Assume a per-city demand model (e.g. LightGBM) trained here on
        # that city's order history, weather and festival calendar.
        self.mape = {"bangalore": 8.1, "mumbai": 9.4, "delhi": 7.6}[self.city]
        print(f"Assume model trained for {self.city} -> MAPE {self.mape}%")
        self.next(self.join)

    @step
    def join(self, inputs):
        # inputs is an iterable of the fanned-out tasks
        self.report = {i.city: i.mape for i in inputs}
        self.next(self.end)

    @step
    def end(self):
        print("City-wise model report:", self.report)
        best = min(self.report, key=self.report.get)
        print(f"Best performing city model: {best} ({self.report[best]}% MAPE)")
        print("Add 297 more cities -> change ONE list, zero code changes")


if __name__ == "__main__":
    PerCityDemandFlow()
