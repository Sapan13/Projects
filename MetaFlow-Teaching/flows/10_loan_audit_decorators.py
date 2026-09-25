"""
10 — CUSTOM DECORATORS & FLOW MUTATORS
Concept : @user_step_decorator is a generator — code before yield runs
          pre-step, code after runs post-step.
          FlowMutator attaches that decorator to EVERY step automatically.
Use case: BFSI compliance — every model step must be audit-logged

Run:  python flows/10_loan_audit_decorators.py run
"""

import time

from metaflow import FlowMutator, FlowSpec, step, user_step_decorator


@user_step_decorator
def audit(step_name, flow, inputs=None, attributes=None):
    """Compliance wrapper: timestamped entry/exit for every step."""
    t0 = time.time()
    print(f"[AUDIT] >> {step_name} started")
    yield                      # <-- the actual step body runs HERE
    print(f"[AUDIT] << {step_name} finished in {time.time() - t0:.2f}s")


class audited_flow(FlowMutator):
    """Attach @audit to every step in the flow, so nobody has to remember to."""

    def mutate(self, mutable_flow):
        for _, s in mutable_flow.steps:
            s.add_decorator(audit)


@audited_flow
class LoanModelFlow(FlowSpec):
    """Every step below is auto-audit-logged. Zero copy-paste."""

    @step
    def start(self):
        print("Loan applications loaded")
        self.next(self.train)

    @step
    def train(self):
        # Assume a credit-scoring model trained here.
        print("Assume credit-scoring model trained here")
        self.next(self.end)

    @step
    def end(self):
        print("Model artifacts archived for the auditor")


if __name__ == "__main__":
    LoanModelFlow()
