class User:
    def __init__(self, first_name: str, last_name: str, age: int):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
    
    def to_dict(self):
        return dict(
            first_name = self.first_name,
            last_name = self.last_name,
            age = self.age
        )
