# Class to keep track of items to be purchased
class ShoppingList(object):
    def __init__(self, list_name):
        self.list_name = list_name
        self.shopping_list = []

    # Adds an item to shopping list if item isn't already there
    def add_item(self, item):
        if item not in self.shopping_list:
            self.shopping_list.append(item)
            print(item, "successfully added to shopping cart")
        else:
            print(item, "is already in shopping cart")
    
    # Removes an item from shopping list
    def remove_item(self, item):
        if item in self.shopping_list:
            self.shopping_list.remove(item)
            print(item, "successfully removed from shopping cart")
        else:
            print(item, "has not been added to shopping cart yet")

    # Prints contents of shopping list
    def view_list(self):
        print("Shopping List - ", self.list_name, ":")
        print("-------------------------------------------------------------")
        for item in self.shopping_list:
            print(item)

# Create new ShoppingList object
pet_store_list = ShoppingList("Pet Store Shopping List")

# Add items to list
pet_store_list.add_item("dog food")
pet_store_list.add_item("frisbee")
pet_store_list.add_item("bowl")
pet_store_list.add_item("collars")
pet_store_list.add_item("flea collars")

# Remove an item
pet_store_list.remove_item("flea collars")

# Try adding a duplicate item
pet_store_list.add_item("frisbee")

# Display shopping list
pet_store_list.view_list()