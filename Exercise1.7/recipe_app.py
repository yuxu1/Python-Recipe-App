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
    print("*** CREATE A NEW RECIPE ***")
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
    print("")
    print("="*40)
    print("*** SEARCH RECIPES BY INGREDIENTS ***")
    print("="*40)
    print("")
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

def edit_recipe():
    print("")
    print("="*40)
    print("*** EDIT A RECIPE ***")
    print("="*40)
    print("")
    if session.query(Recipe).count() < 1:
        print("There are no recipes found! Please create one now!")
        return
    results = session.query(Recipe).with_entities(Recipe.id, Recipe.name).all()
    ids_list = []
    print("\nAVAILABLE RECIPES")
    print("-"*40)
    for result in results:
        print(result)
        ids_list.append(result[0])

    try:
        recipe_id = int(input("Enter the ID of the recipe you want to update: "))
    except:
        print("Input is invalid.")
        return
    
    if recipe_id not in ids_list:
        print("Recipe ID not found.")
        return

    recipe_to_edit = session.query(Recipe).filter(Recipe.id == recipe_id).one()
    print("Available for Modification:")
    print(f"\t1 - Name: {recipe_to_edit.name}")
    print(f"\t2 - Ingredients: {recipe_to_edit.ingredients}")
    print(f"\t3 - Cooking Time: {recipe_to_edit.cooking_time}")

    try:
        attribute = input("What would you like to update for this recipe? Enter 1, 2, or 3: ")
        updated_value = input("What should it be changed to? ")
    except ValueError:
        print("One of more of your inputs is not in the right format")
        return
    except:
        print("An unexpected error occurred.")
        return

    # Update name
    if attribute == "1":
        session.query(Recipe).filter(Recipe.id == recipe_id).update(Recipe.name: updated_value)
        print("Recipe name updated to", updated_value)
    
    # Update ingredients
    elif attribute == "2":
        session.query(Recipe).filter(Recipe.id == recipe_id).update(Recipe.ingredients: updated_value)

        recipe_ingredients = tuple(recipe_to_edit.ingredients.split(", "))

        # Recalculate difficulty level & update in database
        updated_difficulty = calc_difficulty(recipe_to_edit.cooking_time, recipe_ingredients)
        session.query(Recipe).filter(Recipe.id == recipe_id).update(Recipe.difficulty: updated_difficulty)

        print("Ingredients have been updated:")
        for ingredient in recipe_ingredients:
            print(" - " + ingredient)
        print("Difficulty Automatically Updated to:", updated_difficulty)

    # Update cooking time
    elif attribute == "3":
        updated_cooking_time = int(updated_value)
        session.query(Recipe).filter(Recipe.id == recipe_id).update(Recipe.cooking_time: updated_cooking_time)
        # Retrieve recipe details
        recipe_ingredients = tuple(recipe_to_edit.ingredients.split(", "))

        # Recalculate difficulty level & update in database
        updated_difficulty = calc_difficulty(recipe_to_edit.cooking_time, recipe_ingredients)
        session.query(Recipe).filter(Recipe.id == recipe_id).update(Recipe.difficulty: updated_difficulty)
        print("Cooking Time updated to", updated_value, "minutes.")
        print("Difficulty Automatically Updated to:", updated_difficulty)

    else:
        print("Error - no valid option was inputted. Please try again.")
    
    session.commit()

def delete_recipe():
    print("")
    print("="*40)
    print("*** DELETE A RECIPE ***")
    print("="*40)
    print("")
    if session.query(Recipe).count() < 1:
        print("There are no recipes found!")
        return
    results = session.query(Recipe).with_entities(Recipe.id, Recipe.name).all()
    ids_list = []
    print("\nAVAILABLE RECIPES")
    print("-"*40)
    for result in results:
        print(result)
        ids_list.append(result[0])

    try:
        recipe_id = int(input("Enter the ID of the recipe you want to delete: "))
        if recipe_id not in ids_list:
             print("Recipe ID not found.")
            return
        confirm = input("Are you sure you want to delete this recipe? Enter 'yes' or 'no': ")
        if confirm.lower() == "yes":
            recipe_to_delete = session.query(Recipe).filter(Recipe.id == recipe_id).one()
            session.delete(recipe_to_delete)
            session.commit()
        elif confirm.lower() == "no":
            print("Recipe deletion cancelled.")
            return
        else:
            print("Please confirm with a 'yes' or 'no'.")
    except ValueError:
        print("Input is invalid.")
    except:
        print("An unexpected error occurred.")

# Main Menu
def main_menu():
    choice = ""
    # Loop runing the main menu;continues to loop through until user selects 'quit'
    while (choice != 'quit'):
        print("")
        print("="*40)
        print("MAIN MENU")
        print("="*40)
        print("What would you like to do?")
        print("\t1. Create a new recipe")
        print("\t2. View all recipes")
        print("\t3. Search for recipes by ingredients")
        print("\t4. Edit a recipe")
        print("\t5. Delete a recipe")
        print("\tType 'quit' to exit the program.")
        choice = input("Your choice: ")

        if choice == "1":
            create_recipe()
        elif choice == "2":
            view_all_recipes()
        elif choice == "3":
            search_by_ingredients()
        elif choice == "4":
            edit_recipe()
        elif choice == "5":
            delete_recipe()
        elif choice.lower() == "quit":
            print("Exiting program now...")
            print("Thank you for using. See you again soon.")
            session.close()
            engine.dispose()
        else:
            print("That is not a valid option.\n")