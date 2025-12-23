class Car:
    def __init__(self, model, year, color, for_sale): # constructor method to initialize object attributes
        self.model = model
        self.year = year
        self.color = color
        self.for_sale = for_sale

    def drive(self):
        print(f"The {self.model} is now driving.")
    
    def stop(self):
        print(f"The {self.model} has stopped.")

    def describe(self):
        print(f"Model: {self.model}, Year: {self.year}, Color: {self.color}, For Sale: {self.for_sale}")