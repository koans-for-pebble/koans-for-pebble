class Wisdom:
    def __init__(self):
        self.wisdoms = [
            'Code is only as strong as its weakest link.',
            'Documentation is paramount.',
            'Classes are overrated.',
            'When you\'re stuck, ask #pebble-koans. (pebbledev.slack.com)',
            'Anything that is created must inevitably be destroyed.\n'
            'Anything that is allocated must inevitably be freed.',
            'When a heap gets too full, it\'s your fault.',
        ]
        self.failures = [
            'When you lose, you win experience.',
            'When you can\'t win, you can sleep over it.',
            'When you still can\'t win, you can ask for help.',
            'Each failure broadens your senses.',
            'A failure doesn\'t a failure make.',
            'Go squash the bug.',
        ]
        self.experiences = [
            'When the apprentice beats the master, he becomes the master.',
            'Even the master has a long path ahead of himself.',
        ]

    def getWisdom(self):
        import random
        return random.choice(self.wisdoms)

    def getFailure(self):
        import random
        return random.choice(self.failures)

    def getExperience(self):
        import random
        return random.choice(self.experiences)
