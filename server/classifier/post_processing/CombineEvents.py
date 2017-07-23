class CombineEvents:

    def __init__(self, minimum_event_gap=0.1):
        self.minimum_event_gap = minimum_event_gap

    def __call__(self, event_segments):
        # event_results_1 = []
        # for event in event_segments:
        #     if event[1]-event[0] >= 0.1:
        #         event_results_1.append((event[0], event[1]))
        #
        # event_segments = event_results_1

        if len(event_segments):
            # 2. remove small gaps between events
            event_results = []

            # Load first event into event buffer
            buffered_event_onset = event_segments[0][0]
            buffered_event_offset = event_segments[0][1]
            for i in range(1, len(event_segments)):
                if event_segments[i][0] - buffered_event_offset > self.minimum_event_gap:
                    # The gap between current event and the buffered is bigger than minimum event gap,
                    # store event, and replace buffered event
                    event_results.append((buffered_event_onset, buffered_event_offset))
                    buffered_event_onset = event_segments[i][0]
                    buffered_event_offset = event_segments[i][1]
                else:
                    # The gap between current event and the buffered is smalle than minimum event gap,
                    # extend the buffered event until the current offset
                    buffered_event_offset = event_segments[i][1]

            # Store last event from buffer
            event_results.append((buffered_event_onset, buffered_event_offset))

            return event_results
        else:
            return event_segments
