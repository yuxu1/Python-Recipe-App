# Imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import Integer, String

# Create engine object that connects to database
engine = create_engine("mysql://cf-python:password@localhost/task_database")

# Generate a declarative base class (to inherit additional properties from SQLAlchemy)
Base = declarative_base()

# Create session object to use for making changes to database
Session = sessionmaker(bind=engine)
session = Session()

# Declare Recipe model (inherit from Base class)
class Recipe(Base):
    __tablename__ = "final_recipes"
    # Table Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    # Method to show quick representation of recipe
    def __repr__(self):
        return f"Recipe ID: {self.id} - {self.name} - Difficulty: {self.difficulty}"
    
    # Method that prints a well-formatted version of the recipe
    def __str__(self):
        output = "-"*40 + "\nName: " + self.name + "\n" + "-"*40 + \
            "\nCooking Time (in minutes): " + str(self.cooking_time) + \
            "\nDifficulty Level: " + self.difficulty + "\nIngredients:"
        for ingredient in self.return_ingredients_as_list():
            output += "\n\t" + ingredient
        return output

    # Method to calculate difficulty of a recipe based on number of ingredients and cooking time
    def calc_difficulty(self):
        num_of_ingredients = len(self.return_ingredients_as_list())
        if self.cooking_time < 10 and num_of_ingredients < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and num_of_ingredients >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and num_of_ingredients < 4:
            self.difficulty = "Intermediate"
        elif self.cooking_time >= 10 and num_of_ingredients >= 4:
            self.difficulty = "Hard"
        return self.difficulty

    # Method that retrieves ingredients string as a list
    def return_ingredients_as_list(self):
        if not self.ingredients:
            return []
        else:
            return self.ingredients.split(", ")

# Create tables of all the defined models (Recipe)
Base.metadata.create_all(engine)

# Main Operations - 5 Functions
# Function 1 - Create a new recipe
def create_recipe():
    # Header
    print("")
    print("="*40)
    print("*** CREATE A NEW RECIPE ***")
    print("="*40)
    print("")

    # Collect recipe name from user & validate input
    while True:
        name = input("Enter a name for the recipe: ")
        if len(name) < 1 or len(name) > 50:
            print("Please enter a recipe name between 1 - 5 characters!")
        else: break

    # Collect cooking time from user & validate input
    while True:
        cooking_time_input = input("Enter the cooking time of the recipe(in minutes): ")
        # Check if something is inputted
        if len(cooking_time_input) == 0:
            print("Please enter a time (a rough estimate is fine)!")
        # Check if input is a number
        elif not cooking_time_input.isnumeric():
            print("Please input numbers only!")
        # Convert input into an integer after validation
        else:
            cooking_time = int(cooking_time_input)
            break

    # Collect amd validate ingredients input from user
    ingredients = []
    while True:
        num_of_ingredients = input("How many ingredients would you like to input? ")
        if not num_of_ingredients.isnumeric:
            print("Please enter a number!")
        elif int(num_of_ingredients) <= 0:
            print("Please enter a positive number!")
        # Collect ingredients from user 1 by 1, appending to list
        else:
            for item in range(int(num_of_ingredients)):
                ingredient_entry = input("Please enter an ingredient: ")
                if ingredient_entry != "":
                    ingredients.append(ingredient_entry)
            break
    # Combine ingredients in list into one string
    ingredients = ", ".join(ingredients)

    # Create new recipe object using the user inputs
    recipe_entry = Recipe(
        name = name,
        ingredients = ingredients,
        cooking_time = cooking_time,
    )
    recipe_entry.calc_difficulty()
    session.add(recipe_entry)
    session.commit()
    print("\nRecipe successfully added!")

# Function 2 - View all recipes in table
def view_all_recipes():
    # Header
    print("")
    print("="*40)
    print("*** ALL RECIPES ***")
    print("="*40)
    print("")

    # Retrieve and display all recipes unless none were created
    all_recipes = session.query(Recipe).all()
    if all_recipes:
        for recipe in all_recipes:
            print(recipe)
    else:
        print("No recipes were found. Please create one!")
        return

# Function 3 - Search recipes by ingredient(s)
def search_by_ingredients():
    # Header
    print("")
    print("="*40)
    print("*** SEARCH RECIPES BY INGREDIENTS ***")
    print("="*40)
    print("")

    # If no entries exist, notify user and exit function
    if session.query(Recipe).count() < 1:
        print("There are no recipes found! Please create one to start searching!")
        return
    
    results = session.query(Recipe.ingredients).all()
    all_ingredients = []
    # Loop through all ingredients and add ingredients to all_ingredients (avoid duplicates)
    for row in results:
        # Split up ingredients from each recipe's ingredients list(combined string)
        split_ingredients = row[0].split(", ")
        for ingredient in split_ingredients:
            # Convert all ingredients to lowercase for more standardized comparison
            formatted_ingredient = ingredient.lower()
            # Add ingredient to list if not already on the list
            if formatted_ingredient not in all_ingredients:
                all_ingredients.append(formatted_ingredient)

    # Display all unique ingredients with a number displayed next to each ingredient
    ingredients_numbered = list(enumerate(all_ingredients))
    print("All Ingredients:")
    for ingredient in ingredients_numbered:
        print(ingredient)

    # Allow user to pick 1 or more numbers from enumerated list (ingredient(s) to search for)
    try:
        indexes = input("Enter the ingredient number(s) you want to search for (seperated with a space): ").split(" ")
        search_ingredients = []
        # Match user selection(s) to the corresponding ingredient names
        for index in indexes:
            search_index = int(index)
            search_ingredients.append(ingredients_numbered[search_index][1])
    except ValueError:
        print("Only whole numbers are allowed.")
    except IndexError:
        print("One or more of your inputs is not an option on the list.")
    except:
        print("An unexpected error has occurred.")
    
    # List containing search conditions created for each search ingredient
    conditions = []
    for ingredient in search_ingredients:
        like_term = f"%{ingredient}%"
        conditions.append(Recipe.ingredients.like(like_term))

    # Retrieve & display recipes from database that match the search conditions
    filtered_recipes = session.query(Recipe).filter(*conditions).all()
    if not filtered_recipes:
        print("\nThere are no recipes containing those ingredients.\n")
    else:
        print("="*40)
        print(f"Recipes Containing {search_ingredients}:")
        print("="*40)
    for recipe in filtered_recipes:
        print(recipe)

# Function 4 - Edit an existing recipe
def edit_recipe():
    # Header
    print("")
    print("="*40)
    print("*** EDIT A RECIPE ***")
    print("="*40)
    print("")

    # If no entries created, notify user and exit function
    if session.query(Recipe).count() < 1:
        print("There are no recipes found! Please create one now!")
        return
    
    # Retrieve & display ID and name of all recipes in database
    results = session.query(Recipe).with_entities(Recipe.id, Recipe.name).all()
    ids_list = []
    print("AVAILABLE RECIPES")
    print("-"*40)
    for result in results:
        print(result)
        ids_list.append(result[0])

    # Allow user to select a recipe by inputting the corresponding ID
    try:
        recipe_id = int(input("Enter the ID of the recipe you want to update: "))
    except:
        print("Input is invalid.")
        return
    
    # Validate if ID matches a recipe
    if recipe_id not in ids_list:
        print("Recipe ID not found.")
        return

    # Retrieve the recipe selected by the user & display the editable attributes
    recipe_to_edit = session.query(Recipe).filter(Recipe.id == recipe_id).one()
    print("Available for Modification:")
    print(f"\t1 - Name: {recipe_to_edit.name}")
    print(f"\t2 - Ingredients: {recipe_to_edit.ingredients}")
    print(f"\t3 - Cooking Time: {recipe_to_edit.cooking_time}")

    # Allow user to select an attribute to edit & the new desired value
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
        if 0 < len(updated_value) <= 50:
            recipe_to_edit.name = updated_value
            print("Recipe name updated to", updated_value)
    
    # Update ingredients
    elif attribute == "2":
        recipe_to_edit.ingredients = updated_value
        recipe_ingredients = tuple(recipe_to_edit.ingredients.split(", "))
        # Recalculate difficulty level & update
        recipe_to_edit.calc_difficulty()
        # Notify user of successful update
        print("Ingredients have been updated:")
        for ingredient in recipe_ingredients:
            print(" - " + ingredient)
        print("Difficulty Automatically Updated to:", recipe_to_edit.difficulty)

    # Update cooking time
    elif attribute == "3":
        updated_cooking_time = int(updated_value)
        recipe_to_edit.cooking_time = updated_cooking_time
        recipe_ingredients = tuple(recipe_to_edit.ingredients.split(", "))
        # Recalculate difficulty level & update
        recipe_to_edit.calc_difficulty()
        # Notify user of successful update
        print("Cooking Time updated to", updated_value, "minutes.")
        print("Difficulty Automatically Updated to:", recipe_to_edit.difficulty)

    else:
        print("Error - no valid option was inputted. Please try again.")
    
    try:
        session.commit()
    except:
        session.rollback()

# Function 5 - delete a recipe
def delete_recipe():
    # Header
    print("")
    print("="*40)
    print("*** DELETE A RECIPE ***")
    print("="*40)
    print("")

    # If no entries exist, notify user & exit function
    if session.query(Recipe).count() < 1:
        print("There are no recipes found!")
        return
    
    # Retrieve & display ID and name of all recipes
    results = session.query(Recipe).with_entities(Recipe.id, Recipe.name).all()
    ids_list = []
    print("\nAVAILABLE RECIPES")
    print("-"*40)
    for result in results:
        print(result)
        ids_list.append(result[0])

    # Allow user to select a recipe through its ID
    try:
        recipe_id = int(input("Enter the ID of the recipe you want to delete: "))
        # Validate if ID inputted matches a recipe
        if recipe_id not in ids_list:
            print("Recipe ID not found.")
            return
        # Retrieve the recipe selected by user
        recipe_to_delete = session.query(Recipe).filter(Recipe.id == recipe_id).one()
        
        # User confirmation before actual deletion
        confirm = input("Are you sure you want to delete this recipe? Enter 'yes' or 'no': ")
        # If confirmed, continue with deletion
        if confirm.lower() == "yes":
            session.delete(recipe_to_delete)
            session.commit()
            print("\nRecipe successfully deleted")
            return
        # If not confirmed, cancel deletion and return to main menu
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

# Load main menu
main_menu()