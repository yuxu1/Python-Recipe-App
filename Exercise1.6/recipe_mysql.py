# Connect script to MySQL server
# Import module
import mysql.connector

# Initialize connection object 'conn'
conn = mysql.connector.connect(
    host='localhost',
    user='cf-python',
    passwd='password'
)

# Initialize cursor object from conn
cursor = conn.cursor()

# Create & access database (avoid duplicate)
cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
cursor.execute("USE task_database")

# Create Recipes table (avoid duplicate)
cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    ingredients VARCHAR(225),
    cooking_time INT,
    difficulty VARCHAR(20)
)''')

# Main Menu
def main_menu(conn, cursor):
    choice = ""
    # Loop runing the main menu;continues to loop through until user selects 'quit'
    while (choice != 'quit'):
        print("")
        print("=======================================")
        print("MAIN MENU")
        print("=======================================")
        print("What would you like to do?")
        print("   1. Create a new recipe")
        print("   2. Search for a recipe by ingredient")
        print("   3. Update an existing recipe")
        print("   4. Delete a recipe")
        print("   Type 'quit' to exit the program.")
        choice = input("Your choice: ")

        if choice == "1":
            create_recipe(conn, cursor)
        elif choice == "2":
            search_recipe(conn, cursor)
        elif choice == "3":
            update_recipe(conn, cursor)
        elif choice == "4":
            delete_recipe(conn, cursor)
        elif choice.lower() == "quit":
            print("Exiting program now...")
            print("Thank you for using. See you again soon.")
            conn.close()
        else:
            print("That is not a valid option.\n")

# Calculate difficulty level of a recipe
def calc_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        difficulty = "Easy"
    elif cooking_time < 10 and len(ingredients) >= 4:
        difficulty = "Medium"
    elif cooking_time >= 10 and len(ingredients) < 4:
        difficulty = "Intermediate"
    elif cooking_time >= 10 and len(ingredients) >= 4:
        difficulty = "Hard"
    return difficulty

# Option 1 - create a recipe
def create_recipe(conn, cursor):
    print("")
    print("=======================================")
    print("CREATE A NEW RECIPE")
    print("=======================================")
    print("")

    name = input("Enter a name for the recipe: ")
    cooking_time = int(input("Enter the cooking time of the recipe(in minutes): "))
    ingredients = input("Enter needed ingredients(separated by commas and a space): ").split(", ")
    difficulty = calc_difficulty(cooking_time, ingredients)

    ingredients_joined = ", ".join(ingredients)

    insert_query = "INSERT INTO Recipes(name, ingredients, cooking_time, difficulty) VALUES(%s, %s, %s, %s)"
    cursor.execute(insert_query, (name, ingredients_joined, cooking_time, difficulty))
    conn.commit()
    print("Recipe successfully added.")

# Option 2 - search for a recipe
def search_recipe(conn, cursor):
    print("")
    print("=======================================")
    print("SEARCH RECIPES BY INGREDIENT")
    print("=======================================")
    print("")

    all_ingredients = []

    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall()

    # If Recipes table is empty, return to main menu
    if len(results) == 0:
        print("There are no recipes found yet. Please create one!")
        return

    # If there are results, add ingredients to all_ingredients list
    # Set to lowercase for equal comparison (avoid duplicates)
    for row in results:
        # split up ingredients string
        ingredients_list = row[0].split(", ")
        for ingredient in ingredients_list:
            formatted_ingredient = ingredient.lower()
            if formatted_ingredient not in all_ingredients:
                all_ingredients.append(formatted_ingredient)

    # Create and display new enumerated list of all_ingredients (2-item types)
    available_ingredients = list(enumerate(all_ingredients))
    print("All Ingredients:")
    for ingredient in available_ingredients:
        print(ingredient)

    # Allow user to pick a number from enumerated list (ingredient to search for)
    try:
        index = int(input("Enter the ingredient number you want to search for: "))
        search_ingredient = available_ingredients[index][1]
    except ValueError:
        print("Only whole numbers are allowed.")
    except IndexError:
        print("The number you entered is not an option on the list.")
    except:
        print("An unknown error has occurred.")
    # Look through all recipes and display the ones that contain the searched ingredient
    else:
        cursor.execute("SELECT * FROM Recipes WHERE ingredients LIKE %s", ("%" + search_ingredient + "%",))
        results = cursor.fetchall()
        print("=======================================")
        print("Recipes Containing", search_ingredient, ":")
        print("=======================================")
        for row in results:
            print("------------------------------")
            print("Name:", row[1])
            print("------------------------------")
            print("Ingredients:", row[2])
            print("Cooking Time(minutes):", row[3])
            print("Difficulty:", row[4])
            print("")

# Option 3 - Update an existing recipe
def update_recipe(conn, cursor):
    cursor.execute("SELECT * FROM Recipes")
    results = cursor.fetchall()

    # If no recipes inputted, return to main menu
    if len(results) == 0:
        print("There are no recipes to update. Please create one!")
        return

    # Header
    print("")
    print("=======================================")
    print("UPDATE A RECIPE")
    print("=======================================")

    print("Available Recipes:")
    print("------------------------------")
    for row in results:
        print("ID:", row[0])
        print("Name:", row[1])
        print("Ingredients:", row[2])
        print("Cooking Time(minutes):", row[3])
        print("Difficulty:", row[4])
        print("")

    # Collect user input - recipe & column to be updated,and new value for selected column
    selected_recipe_id = int(input("Enter the ID of the recipe you want to update: "))
    print("Available for Modification:")
    print("   A - Name")
    print("   B - Cooking Time")
    print("   C - Ingredients")
    selected_column = input("What would you like to update for this recipe? Enter 'A', 'B', or 'C': ")
    updated_value = input("What should it be changed to? ")

    # Update name
    if selected_column.upper() == "A":
        cursor.execute("UPDATE Recipes SET name = %s WHERE id = %s",
        (updated_value, selected_recipe_id))
        print("Recipe name updated to", updated_value)
    
    # Update cooking time
    elif selected_column.upper() == "B":
        updated_cooking_time = int(updated_value)
        cursor.execute("UPDATE Recipes SET cooking_time = %s WHERE id = %s",
        (updated_cooking_time, selected_recipe_id))
        # Retrieve recipe details
        cursor.execute("SELECT * FROM Recipes WHERE id = %s", (selected_recipe_id,))
        recipe_updating = cursor.fetchall()
        cooking_time = recipe_updating[0][3]
        recipe_ingredients = tuple(recipe_updating[0][2].split(", "))

        # Recalculate difficulty level & update in database
        updated_difficulty = calc_difficulty(cooking_time, recipe_ingredients)
        cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s",
        (updated_difficulty, selected_recipe_id))
        print("Cooking Time updated to", updated_value, "minutes.")
        print("Difficulty Automatically Updated to:", updated_difficulty)
    
    # Update ingredients
    elif selected_column.upper() == "C":
        cursor.execute("UPDATE Recipes SET ingredients = %s WHERE id = %s",
        (updated_value, selected_recipe_id))

        # Retrieve recipe details
        cursor.execute("SELECT * FROM Recipes WHERE id = %s", (selected_recipe_id,))
        recipe_updating = cursor.fetchall()
        cooking_time = recipe_updating[0][3]
        recipe_ingredients = tuple(recipe_updating[0][2].split(", "))

        # Recalculate difficulty level & update in database
        updated_difficulty = calc_difficulty(cooking_time, recipe_ingredients)
        cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s",
        (updated_difficulty, selected_recipe_id))

        print("Ingredients have been updated:")
        for ingredient in recipe_ingredients:
            print(" - " + ingredient)
        print("Difficulty Automatically Updated to:", updated_difficulty)

    else:
        print("Error - no valid option was inputted. Please try again.")
    
    conn.commit()

# Option 4 - delete a recipe
def delete_recipe(conn, cursor):
    cursor.execute("SELECT * FROM Recipes")
    results = cursor.fetchall()

    # If no recipes found, return to main menu
    if len(results) == 0:
        print("There are no recipes to be deleted. Please create one!")
        return

    # Header
    print("")
    print("=======================================")
    print("DELETE A RECIPE")
    print("=======================================")

    # Display all recipes
    print("")
    print("Available Recipes:")
    print("------------------------------")
    for row in results:
        print("ID:", row[0])
        print("Name:", row[1])
        print("Ingredients:", row[2])
        print("Cooking Time(minutes):", row[3])
        print("Difficulty:", row[4])
        print("")
    
    try:
        # User input for the recipe to delete
        selected_recipe_id = int(input("Enter the ID of the recipe you want to delete: "))
        # Confirm with user before moving forward with deletion
        confirm = input("Are you sure you want to delete this recipe? Enter 'Y' or 'N': ")
        if confirm.upper() == "Y":
            # Query to delete the row as specified by user
            cursor.execute("DELETE FROM Recipes WHERE id = %s", (selected_recipe_id, ))
            print("Recipe has been deleted successfully.")
            conn.commit()
        elif confirm.upper() == "N":
            print("Recipe deletion cancelled.")
            return
        else:
            print("Please confirm with a 'Y' for yes or 'N' for no")
    except ValueError:
        print("Only whole numbers are allowed")
    except:
        print("An unexpected error occurred")


# Main Code - load main menu
main_menu(conn, cursor)