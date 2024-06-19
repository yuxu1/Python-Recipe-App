from sqlalchemy import create_engine

engine = create_engine("mysql://cf-python:password@localhost/task_database")

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import column
from sqlalchemy.types import Integer, string

class Recipe(Base):
    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return f"Recipe ID: {self.id} - {self.name} - Difficulty: {self.difficulty}"
    
    def __str__(self):
        output = "-*40" + "\nName: " + self.name + "\n-*40\n" \
            "\nCooking Time (in minutes): " + str(self.cooking_time) + \
            "\nDifficulty Level: " + self.difficulty + "\nIngredients:"
        for ingredient in self.return_ingredients_as_list():
            output += "\n\t" + ingredient
        return output

    def calc_difficulty(cooking_time, ingredients):
        if cooking_time < 10 and len(ingredients) < 4:
            self.difficulty = "Easy"
        elif cooking_time < 10 and len(ingredients) >= 4:
            self.difficulty = "Medium"
        elif cooking_time >= 10 and len(ingredients) < 4:
            self.difficulty = "Intermediate"
        elif cooking_time >= 10 and len(ingredients) >= 4:
            self.difficulty = "Hard"
        return self.difficulty

    def return_ingredients_as_list(self):
        if not self.ingredients:
            return []
        else:
            return self.ingredients.split(", ")

Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

def create_recipe():
    print("")
    print("="*40)
    print("CREATE A NEW RECIPE")
    print("="*40)
    print("")

    while True:
        name = input("Enter a name for the recipe: ")
        if len(name) < 1 or len(name) > 50:
            print("Please enter a recipe name between 1 - 5 characters!")
        else: break

    while True:
        cooking_time_input = input("Enter the cooking time of the recipe(in minutes): ")
        if len(cooking_time_input) = 0:
            print("Please enter a time (a rough estimate is fine)!")
        elif not cooking_time.isnumeric():
            print("Please input numbers only!")
        else:
            cooking_time = int(cooking_time_input)
            break

    ingredients = []
    while True:
        num_of_ingredients = input("How many ingredients would you like to input? ")
        if not num_of_ingredients.isnumeric or int(num_of_ingredients) <= 0:
            print("Please enter a positive number!")
        for item in range(int(num_of_ingredients)):
            ingredient_entry = input("Please enter an ingredient: ")
            if ingredient_entry != "":
                ingredients.append(ingredient_entry)
            else: break
        ingredients = ", ".join(ingredients)

    recipe_entry = Recipe(
        name = name,
        ingredients = ingredients,
        cooking_time = cooking_time,
    )
    recipe_entry.calculate_difficulty()
    session.add(recipe_entry)
    session.commit()
    print("\nRecipe successfully added!")

def view_all_recipes():
    all_recipes = session.query(Recipe).all()
    if all_recipes:
        for recipe in all_recipes:
            print(recipe)
    else:
        print("No recipes were found. Please create one!")
        return

def search_by_ingredients():
    if session.query(Recipe).count() < 1:
        print("There are no recipes found! Please create one to start searching!")
        return
    results = session.query(Recipe.ingredients).all()
    all_ingredients = []
    for row in results:
        split_ingredients = row[0].split(", ")
        for ingredient in split_ingredients:
            formatted_ingredient = ingredient.lower()
            if formatted_ingredient not in all_ingredients:
                all_ingredients.append(formatted_ingredient)

    ingredients_numbered = list(enumerate(all_ingredients))
    print("All Ingredients:")
    for ingredient in ingredients_numbered:
        print("\t" + ingredient)

    # Allow user to pick a number from enumerated list (ingredient to search for)
    try:
        indexes = input("Enter the ingredient number(s) you want to search for (seperated with a space: ").split(" ")
        search_ingredients = []
        for index in indexes:
            search_index = int(index)
            search_ingredients.append(ingredients_numbered[search_index][1])
    except ValueError:
        print("Only whole numbers are allowed.")
    except IndexError:
        print("One or more of your inputs is not an option on the list.")
    except:
        print("An unexpected error has occurred.")
    
    conditions = []
    for ingredient in search_ingredients:
        like_term = f"%{ingredient}%"
        conditions.append(Recipe.ingredients.like(like_term))

    filtered_recipes = session.query(Recipe).filter(*conditions).all()
    if not filtered_recipes:
        print("\nThere are no recipes containing those ingredients.\n")
    else:
        print("="*40)
        print(f"Recipes Containing {search_ingredients}:")
        print("="*40)

    for recipe in filtered_recipes:
        print(recipe)

def edit_recipe()

def delete_recipe()