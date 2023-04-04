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

    # Print the recipe ingredients and quantities and round the quantities to 2 decimals
    print(f"Ingredients for {recipe_name} ({servings} servings):")
    for ingredient in recipe_ingredients:
        print(f"- {ingredient[0]} ({round(ingredient[2], 2)} {ingredient[1]})")



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


print("All recipes:")
print_all_recipes()
print("************")
# Ask the user for the recipe name and servings
recipe_name = input("Enter the recipe name: ")
servings = int(input("Enter the number of servings: "))
# Call the function to retrieve the ingredients for a recipe
get_recipe_ingredients(recipe_name, servings)


