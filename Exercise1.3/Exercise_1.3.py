# Initialize two empty lists
recipes_list = []
ingredients_list = []

# Define custom take_recipe function that takes input from user
def take_recipe():
    name = input("Enter a name for the recipe: ")
    cooking_time = int(input("Enter the cooking time for the recipe in minutes: "))
    ingredients = list(input("Enter the ingredients needed (separated by commas): ").split(', '))
    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients
    }
    return recipe

# Prompt to ask user how many recipes to input
n = int(input("Enter how many recipes you would like to input: "))

# Iterate loop through number of recipes to be inputted
for i in range(n):
    recipe = take_recipe()
    # Check if each ingredient is already in ingredients_list (if not,add it)
    for ingredient in recipe["ingredients"]:
        if not ingredient in ingredients_list:
            ingredients_list.append(ingredient)
    # Store return output (dictionary)
    recipes_list.append(recipe)

# Iterate through list of recipes and rates difficulty level of each
for recipe in recipes_list:
    cooking_time = recipe["cooking_time"]
    number_of_ingredients = len(recipe["ingredients"])
    difficulty = ""

    if cooking_time < 10 and number_of_ingredients < 4:
        recipe["difficulty"] = "Easy"
    elif cooking_time < 10 and number_of_ingredients >= 4:
        recipe["difficulty"] = "Medium"
    elif cooking_time >= 10 and number_of_ingredients < 4:
        recipe["difficulty"] = "Intermediate"
    elif cooking_time >= 10 and number_of_ingredients >= 4:
        recipe["difficulty"] = "Hard"

    # Display each recipe
    print("Recipe:", recipe["name"])
    print("Cooking Time (min):", recipe["cooking_time"])
    print("Ingredients:")
    for ingredient in recipe["ingredients"]:
        print(ingredient)
    print("Difficulty level:", recipe["difficulty"])
    print("")

# Display all ingredients across all recipes in alphabetical order
print("Ingredients Available Across All Recipes")
print("----------------------------------------")
ingredients_list.sort()
for ingredient in ingredients_list:
    print(ingredient)