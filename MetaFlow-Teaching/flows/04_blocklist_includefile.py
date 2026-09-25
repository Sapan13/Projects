"""
04 — INCLUDEFILE
Concept : IncludeFile does the open() + .read() for you.
          self.blocklist is a STRING of the file's contents, NOT a path.
Use case: freezing the fraud merchant blocklist into the run (audit lineage)

Run:  python flows/04_blocklist_includefile.py run --blocklist data/blocked_merchants.txt

Then prove the run kept its own copy:
      rm data/blocked_merchants.txt
      python -c "from metaflow import Flow; print(Flow('BlocklistFlow').latest_run.data.blocklist)"
"""

from metaflow import FlowSpec, IncludeFile, step


class BlocklistFlow(FlowSpec):
    """Freeze the merchant blocklist into the run."""

    # This ONE line replaces:  with open(path) as f: blocklist = f.read()
    # The name "blocklist" is what creates the CLI flag --blocklist
    blocklist = IncludeFile("blocklist", is_text=True,
                            help="One blocked merchant ID per line")

    @step
    def start(self):
        # Proof that self.blocklist is the file's TEXT, not its path:
        print("type(self.blocklist) =", type(self.blocklist))
        print("self.blocklist       =", repr(self.blocklist))

        # From here it's ordinary Python string work.
        self.merchants = self.blocklist.split()
        print("self.merchants       =", self.merchants)
        self.next(self.end)

    @step
    def end(self):
        # Assume every incoming UPI txn is scored against this list here.
        print(f"Assume fraud model scored txns against {len(self.merchants)} blocked merchants")
        print("Auditor asks 'what data?' -> it's stored inside the run itself  OK")


if __name__ == "__main__":
    BlocklistFlow()
