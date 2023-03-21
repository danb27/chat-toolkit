class SpeakingRateError(ValueError):
    def __init__(self):
        super().__init__("Speaking rate must be > 0")
