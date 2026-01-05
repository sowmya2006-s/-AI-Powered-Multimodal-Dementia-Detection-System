import random

class VisualMemorySession:
    def __init__(self, image_pool, used_images=None):
        self.image_pool = image_pool
        self.used_images = set(used_images or [])

    def generate_round(self, delay_seconds):
        available = list(set(self.image_pool) - self.used_images)

        if len(available) < 4:
            raise ValueError("Insufficient unique images")

        target = random.choice(available)
        self.used_images.add(target)

        distractors = random.sample(
            list(set(available) - {target}), 3
        )

        options = distractors + [target]
        random.shuffle(options)

        return {
            "target": target,
            "options": options,
            "delay": delay_seconds,
            "used_images": list(self.used_images)
        }
