class Pet:
    def __init__(self):
        # Empty constructor
        pass
    def __init__(self):
        self.name = ""
        self.pet_type = ""
        self.breed = ""
        self.gender = ""
        self.weight = 0.0
        self.color = ""
        self.age = 0

    def display_info(self):
        print(f"Name: {self.name}")
        print(f"Type: {self.pet_type}")
        print(f"Type: {self.breed}")
        print(f"Gender: {self.gender}")
        print(f"Weight: {self.weight} lb")
        print(f"Color: {self.color}")
        print(f"Age: {self.age} years")