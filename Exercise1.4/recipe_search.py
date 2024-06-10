import pickle

# Function to display a recipe
def display_recipe(recipe):
    print("")
    print("Name:", recipe["name"])
    print("Cooking Time (minutes):", recipe["cooking_time"])
    print("Ingredients:")
    for ingredient in recipe["ingredients"]:
        print(ingredient)
    print("Difficulty Level:", recipe["difficulty"])
    print("")

# Function to search for an ingredient in given data
def search_ingredient(data):
    # Create and display new enumerated list of all_ingredients (2-item types)
    available_ingredients = list(enumerate(data["all_ingredients"]))
    print("All Ingredients:")
    for ingredient in available_ingredients:
        print(ingredient)

    # Allow user to pick a number from enumerated list (ingredient to search for)
    try:
        index = int(input("Enter the ingredient number you want to search for: "))
        ingredient_searched = available_ingredients[index][1]
    except ValueError:
        print("Only whole numbers are allowed.")
    except IndexError:
        print("The number you entered is not an option on the list.")
    except:
        print("An unknown error has occurred.")
    # Look through all recipes and display the ones that contain the searched ingredient
    else:
        for recipe in data["recipes_list"]:
            if ingredient_searched in recipe["ingredients"]:
                display_recipe(recipe)

# Prompt user to enter a filename (binary file)
filename = input("Enter the filename where you are storing the recipes(without extension): ") + ".bin"

# Open the file and load contents
try:
    file = open(filename, 'rb')
    data = pickle.load(file)
# Error when a file with given name is not found
except FileNotFoundError:
    print("No file was found with that name!")
# Handles other exceptions
except:
    print("An unknown error has occurred!")
# Close the file after data is loaded and pass data to search_ingredient()
else:
    file.close()
    search_ingredient(data)