class Goal:
    def __init__(self, title, description):
        self.title = title
        self.description = description

    def __str__(self):
        return f"Goal(title={self.title}, description={self.description})"