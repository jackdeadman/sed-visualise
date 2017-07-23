class RemoveShortEvents:

    def __init__(self, minimum_event_duration=0.1):
        self.minimum_event_duration = minimum_event_duration

    def __call__(self, event_segments):
        results = []
        for start, end in event_segments:
            if end-start >= self.minimum_event_duration:
                results.append((start, end))

        return results
