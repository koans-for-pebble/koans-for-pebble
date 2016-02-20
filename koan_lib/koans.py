class Koans:
    def __init__(self):
        import collections
        self.koans = collections.OrderedDict()
            # Any koan must be built, and a build error immediately fails.
            # However, more tests can be defined here.
            # For example, emu-(aplite|basalt|chalk).
            # Basically, the first test is building
        self.koans['about-types'] = {'tests': [
        {
            'name': 'emu-aplite',
            'assertions': [
                'about-types-ints',
                'about-types-chars',
                'about-types-int-arrays',
                'about-types-strings'
            ]
        }]}
        self.koans['about-math'] = {'tests': [
        {
            'name': 'emu-aplite',
            'assertions': [
                'about-math-addition',
                'about-math-multiplication',
                'about-math-division',
                'about-math-increment',
                'about-math-decrement'
            ]
        }]}

    def getKoanDir(self, koan):
        import os
        return os.path.join('koans', koan)

    def unsolveAll(self):
        import os
        for koan in self.koans.keys():
            if os.path.exists(os.path.join(self.getKoanDir(koan), 'SOLVED')):
                os.unlink(os.path.join(self.getKoanDir(koan), 'SOLVED'))

    def isSolved(self, koan):
        import os
        return os.path.exists(os.path.join(self.getKoanDir(koan), 'SOLVED'))

    def setSolved(self, koan):
        import os
        with open(os.path.join(self.getKoanDir(koan), 'SOLVED'), 'w') as fh:
            fh.write('')

    def getNextSolvable(self):
        next = None
        for koan in self.koans.keys():
            if not self.isSolved(koan):
                next = koan
                break
        return next

    def getSolvable(self):
        solvable = []
        for koan in self.koans.keys():
            if not self.isSolved(koan):
                solvable.append(koan)
        return solvable

    def getSolvedAmount(self):
        solved = 0
        for koan in self.koans.keys():
            if self.isSolved(koan):
                solved += 1
            else:
                break
        return solved, len(self.koans)

    def getTests(self, koan):
        return self.koans[koan]['tests']
