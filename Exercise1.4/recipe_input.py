import pickle

# Function that takes input about recipe from user
def take_recipe():
    name = input("Enter a name for the recipe: ")
    cooking_time = int(input("Enter the cooking time in minutes: "))
    ingredients = list(input("Enter the ingredients needed (separated by commas): ").split(", "))
    difficulty = calc_difficulty(cooking_time, ingredients)
    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients,
        "difficulty": difficulty
    }
    return recipe

# Function to calculate difficulty level of a recipe based on cooking time and number of ingredients
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

# Prompt user to enter a filename (binary file)
filename = input("Enter the filename where you are storing the recipes(without extension): ") + ".bin"

# Open the file and load contents
# Expecting dictionary with 2 key-value pairs: recipes_list and all_ingredients
try:
    file = open(filename, 'rb')
    data = pickle.load(file)
# Error when a file with given name is not found-create a new dictionary
except FileNotFoundError:
    print("No file was found with that name!")
    data = {
        "recipes_list": [],
        "all_ingredients": []
    }
# Handles other exceptions - creates a new dictionary
except:
    print("An unknown error has occurred!")
    data = {
        "recipes_list": [],
        "all_ingredients": []
    }
else:
    file.close()
# Extract data into two separate lists
finally:
    recipes_list = data["recipes_list"]
    all_ingredients = data["all_ingredients"]

# Prompt to ask user how many recipes to input
n = int(input("Enter how many recipes you would like to input: "))

# Iterate over each recipe the user inputs
for i in range(n):
    recipe = take_recipe()
    # Check if each inputted ingredient is already in list of all ingredients (if not,add it)
    for ingredient in recipe["ingredients"]:
        if not ingredient in all_ingredients:
            all_ingredients.append(ingredient)
    # Store return output (dictionary)
    recipes_list.append(recipe)

# Update the data dictionary with newly added information
data = {
    "recipes_list": recipes_list,
    "all_ingredients": all_ingredients
}

# Open and write data to the user-defined binary file
with open(filename, 'wb') as updated_file:
    pickle.dump(data, updated_file)