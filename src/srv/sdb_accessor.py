class SdbAccessor:
    process = None

    def run(self):
        pass

    def kill(self):
        pass

    def _run_subprocces(self):
        command = f"";
        # here we run sdb and redirect socket events to sdb event