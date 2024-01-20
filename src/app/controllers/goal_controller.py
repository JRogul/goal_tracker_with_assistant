from app.models.goal import Goal

class GoalController:
    def __init__(self):
        self.goals = []

    def add_goal(self, title, description):
        new_goal = Goal(title, description)
        self.goals.append(new_goal)
        return new_goal

    def get_goals(self):
        return self.goals