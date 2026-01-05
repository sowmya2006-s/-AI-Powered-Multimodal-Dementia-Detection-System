import random

class AudioMemorySession:
    def __init__(self, audio_pool, used_audio=None):
        self.audio_pool = audio_pool
        self.used_audio = set(used_audio or [])

    def generate_round(self, delay_seconds):
        available = list(set(self.audio_pool) - self.used_audio)

        if len(available) < 4:
            raise ValueError("Insufficient unique audio")

        target = random.choice(available)
        self.used_audio.add(target)

        distractors = random.sample(
            list(set(available) - {target}), 3
        )

        options = distractors + [target]
        random.shuffle(options)

        return {
            "target": target,
            "options": options,
            "delay": delay_seconds,
            "used_audio": list(self.used_audio)
        }
