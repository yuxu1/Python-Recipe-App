# Python Exercise 1.2

## Create a structure named recipe_1 that contains the following keys:
* name (str): Contains the name of the recipe
* cooking_time (int): Contains the cooking time in minutes
* ingredients (list): Contains a number of ingredients, each of the str data type

I will use a dictionary data structure for this purpose, because each recipe will contain data of different types and it would make sense to store the recipe’s properties as key-value pairs. The keys would be “name”, “cooking_time”, and “ingredients”, while the recipe name, cooking time in minutes, and a list of ingredients would be stored as the values. 

## Create an outer structure called all_recipes (holds all recipes)

For the outer structure (all_recipes), I will opt to use a list data structure. This would allow the most flexibility while being sequential in nature, allowing me to sort, append, and remove lists (individual recipes) as needed due to lists’ mutable nature.
