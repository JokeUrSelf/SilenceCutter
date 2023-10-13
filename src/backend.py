def render(data) -> None:
    arr = [[]]

    def end_time_span():
        if arr[-1]: arr.append([])

    def start_time_span(a, b):
        arr[-1].append(a)
        arr[-1].append(b)

    def add_to_current_time_span(v):
        if arr[-1]:
            arr[-1][1] = v
        else:
            start_time_span(v, v)

    volume_range = data.audio.volume_range
    seconds_per_sample = 1 / data.audio.fps

    for x in volume_range:
        if x > data.audio.pivot_volume:
            add_to_current_time_span(seconds_per_sample)
        else:
            end_time_span()
        seconds_per_sample += seconds_per_sample
