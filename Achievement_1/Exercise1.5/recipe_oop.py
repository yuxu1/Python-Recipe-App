class Recipe:

    all_ingredients = []

    def __init__(self, name):
        self.name = name
        self.ingredients = []
        self.cooking_time = 0
        self.difficulty = ""
    
    def calculate_difficulty(self):
        if self.cooking_time < 10 and len(self.ingredients) < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and len(self.ingredients) >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and len(self.ingredients) < 4:
            self.difficulty = "Intermediate"
        elif self.cooking_time >= 10 and len(self.ingredients) >= 4:
            self.difficulty = "Hard"

    def get_name(self):
        return self.name

    def get_cooking_time(self):
        return self.cooking_time

    def get_ingredients(self):
        return self.ingredients
    
    def get_difficulty(self):
        if self.difficulty == "":
            self.calculate_difficulty()
        return self.difficulty
    
    def set_name(self, name):
        self.name = name
    
    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time

    def add_ingredients(self, *ingredients):
        self.ingredients.extend(ingredients)
        self.update_all_ingredients()
    
    def update_all_ingredients(self):
        for item in self.ingredients:
            if item not in Recipe.all_ingredients:
                Recipe.all_ingredients.append(item)

    def search_ingredient(self, ingredient):
        return ingredient in self.ingredients

    def __str__(self):
        output = "------------------------------" + \
            "\nName: " + self.name + \
            "\n------------------------------" + \
            "\nCooking Time (in minutes): " + str(self.cooking_time) + \
            "\nDifficulty Level: " + self.get_difficulty() + \
            "\nIngredients: \n"
        for ingredient in self.ingredients:
            output += " - " + ingredient + "\n"
        return output

def recipe_search(data, search_term):
    print("==============================")
    print("Recipes That Contain " + search_term)
    print("==============================")
    recipes_found = 0
    for recipe in data:
        if recipe.search_ingredient(search_term):
            print(recipe)
            recipes_found += 1
    if recipes_found == 0:
        print("Did not find any recipes that use " + search_term)

# Main Code
tea = Recipe("Tea")
tea.add_ingredients("Tea Leaves", "Sugar", "Water")
tea.set_cooking_time(5)

coffee = Recipe("Coffee")
coffee.add_ingredients("Coffee Powder", "Sugar", "Water")
coffee.set_cooking_time(5)

cake = Recipe("Cake")
cake.add_ingredients("Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "milk")
cake.set_cooking_time(50)

banana_smoothie = Recipe("Banana Smoothie")
banana_smoothie.add_ingredients("Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes")
banana_smoothie.set_cooking_time(5)

recipes_list = [tea, coffee, cake, banana_smoothie]

print("==============================")
print("RECIPES LIST")
print("==============================")
for recipe in recipes_list:
    print(recipe)

recipe_search(recipes_list, "Water")
recipe_search(recipes_list, "Sugar")
recipe_search(recipes_list, "Bananas")