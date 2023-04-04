import psycopg2

# Connect to the database and the right schema
conn = psycopg2.connect(
    host="localhost",
    database="Traiteur Ronny",
    user="postgres",
    password="kaas1212"
)

# Define a function to retrieve a recipe's ingredients
def get_recipe_ingredients(recipe_name, servings):
    # Open a cursor to execute SQL queries
    cur = conn.cursor()

    # Get the recipe ID for the given recipe name
    cur.execute("SELECT id FROM recipes WHERE name = %s", (recipe_name,))
    recipe_id = cur.fetchone()

    if recipe_id is None:
        print(f"No recipe found with the name '{recipe_name}'")
        return

    # Get the recipe ingredients and quantities

    cur.execute("""
        SELECT i.name, i.unit, ri.quantity * %s / r.servings
        FROM ingredients i
        JOIN recipe_ingredients ri ON i.id = ri.ingredient_id
        JOIN recipes r ON ri.recipe_id = r.id
        WHERE r.id = %s
    """, (servings, recipe_id))

    recipe_ingredients = cur.fetchall()

    # Print the recipe ingredients and quantities and round the quantities to 2 decimals and convert grams to kilograms
    for ingredient in recipe_ingredients:
        if ingredient[1] == "g" or ingredient[1] == "grams":
            print(f"{ingredient[0]}: {round(ingredient[2]/1000, 2)} kg")
        else:
            print(f"{ingredient[0]}: {round(ingredient[2], 2)} {ingredient[1]}")
    # Convert ml to liters
    for ingredient in recipe_ingredients:
        if ingredient[1] == "ml" or ingredient[1] == "milliliter":
            print(f"{ingredient[0]}: {round(ingredient[2]/1000, 2)} l")
        else:
            print(f"{ingredient[0]}: {round(ingredient[2], 2)} {ingredient[1]}")

    # Close the cursor
    cur.close()




#Print all recipe names from the database
def print_all_recipes():
    # Open a cursor to execute SQL queries
    cur = conn.cursor()
    # Get all the recipes
    cur.execute("SELECT name FROM recipes")
    all_recipes = cur.fetchall()
    # Close the cursor
    cur.close()
    # Print all the recipes
    for recipe in all_recipes:
        print(recipe[0])
#Create a function that adds a new recipe to the database and adds the ingredients to the database if they don't exist yet
def add_recipe(recipe_name, servings, ingredients):
    # Open a cursor to execute SQL queries
    cur = conn.cursor()
    # Check if the recipe already exists
    cur.execute("SELECT id FROM recipes WHERE name = %s", (recipe_name,))
    recipe_id = cur.fetchone()
    if recipe_id is None:
        # Add the recipe to the database
        cur.execute("INSERT INTO recipes (name, servings) VALUES (%s, %s)", (recipe_name, servings))
        # Get the recipe ID for the given recipe name
        cur.execute("SELECT id FROM recipes WHERE name = %s", (recipe_name,))
        recipe_id = cur.fetchone()
        # Add the ingredients to the database if they don't exist yet
        for ingredient in ingredients:
            cur.execute("SELECT id FROM ingredients WHERE name = %s", (ingredient[0],))
            ingredient_id = cur.fetchone()
            if ingredient_id is None:
                cur.execute("INSERT INTO ingredients (name, unit) VALUES (%s, %s)", (ingredient[0], ingredient[1]))
                cur.execute("SELECT id FROM ingredients WHERE name = %s", (ingredient[0],))
                ingredient_id = cur.fetchone()
            # Add the ingredients to the recipe_ingredients table
            cur.execute("INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES (%s, %s, %s)", (recipe_id, ingredient_id, ingredient[2]))
        # Commit the changes to the database
        conn.commit()
        # Close the cursor
        cur.close()
        print("Recipe added!")
    else:
        print("This recipe already exists!")
#Create a new example recipe and add it to the database
add_recipe("Pasta Carbonara", 4, [("Pasta", "grams", 500), ("Eggs", "pieces", 2), ("Bacon", "grams", 100), ("Parmesan", "grams", 50), ("Black Pepper", "grams", 5), ("Salt", "grams", 5)])

#TEST
print("All recipes:")
print_all_recipes()
print("************")
# Ask the user for the recipe name and servings
recipe_name = input("Enter the recipe name: ")
servings = int(input("Enter the number of servings: "))
# Call the function to retrieve the ingredients for a recipe
get_recipe_ingredients(recipe_name, servings)


