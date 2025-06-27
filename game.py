class Game:
    def __init__(self, id):
        self.id = id
        self.p1Choices = []
        self.p2Choices = []
        self.p1Commit = None
        self.p2Commit = None

    def add_choice(self, player, choice):
        if player == 0:
            if choice not in self.p1Choices and len(self.p1Choices) < 2:
                self.p1Choices.append(choice)
        else:
            if choice not in self.p2Choices and len(self.p2Choices) < 2:
                self.p2Choices.append(choice)

    def commit_choice(self, player, choice):
        if player == 0:
            self.p1Commit = choice
        else:
            self.p2Commit = choice

    def both_chosen_two(self):
        return len(self.p1Choices) == 2 and len(self.p2Choices) == 2

    def both_committed(self):
        return self.p1Commit is not None and self.p2Commit is not None

    def winner(self):
        if not self.both_committed():
            return None

        p1 = self.p1Commit
        p2 = self.p2Commit

        if p1 == p2:
            return -1
        elif (p1 == "바위" and p2 == "가위") or \
             (p1 == "가위" and p2 == "보") or \
             (p1 == "보" and p2 == "바위"):
            return 0
        else:
            return 1

    def reset(self):
        self.p1Choices = []
        self.p2Choices = []
        self.p1Commit = None
        self.p2Commit = None

    def connected(self):
        return True
