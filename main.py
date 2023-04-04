import psycopg2
import tkinter as tk

# Connect to the database
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

    # Close the cursor
    cur.close()

    # Return the recipe ingredients and quantities
    return recipe_ingredients

# Define a function to display a recipe's ingredients in a listbox
def display_recipe_ingredients():
    # Get the recipe name and servings from the entry widgets
    recipe_name = recipe_name_entry.get()
    servings = int(servings_entry.get())

    # Get the recipe ingredients and quantities
    recipe_ingredients = get_recipe_ingredients(recipe_name, servings)

    # Clear the listbox
    ingredients_listbox.delete(0, tk.END)

    # Add the recipe ingredients and quantities to the listbox
    for ingredient in recipe_ingredients:
        ingredients_listbox.insert(tk.END, f"{ingredient[0]}: {ingredient[2]} {ingredient[1]}")

# Define a function to search for existing recipes using full text search
def search_recipes():
    # Get the search query from the entry widget
    search_query = search_entry.get()

    # Open a cursor to execute SQL queries
    cur = conn.cursor()

    # Search for recipes using full text search
    cur.execute("""
        SELECT name
        FROM recipes
        WHERE to_tsvector('english', name) @@ to_tsquery('english', %s)
    """, (search_query,))

    # Get the search results and display them in the listbox
    search_results = cur.fetchall()
    recipes_listbox.delete(0, tk.END)
    for result in search_results:
        recipes_listbox.insert(tk.END, result[0])

    # Close the cursor
    cur.close()

# Create the main window
root = tk.Tk()
root.title("Recipe Calculator")

# Create the frame for the recipe name and servings
recipe_frame = tk.Frame(root)
recipe_frame.pack(side=tk.TOP, padx=10, pady=10)

# Create the entry widget for the recipe name
recipe_name_label = tk.Label(recipe_frame, text="Recipe Name:")
recipe_name_label.pack(side=tk.LEFT)
recipe_name_entry = tk.Entry(recipe_frame)
recipe_name_entry.pack(side=tk.LEFT, padx=5)
recipe_name_entry.focus_set()

# Create the entry widget for the servings
servings_label = tk.Label(recipe_frame, text="Servings:")
servings_label.pack(side=tk.LEFT, padx=10)
servings_entry = tk.Entry(recipe_frame)
servings_entry.pack(side=tk.LEFT)

# Create the button to display the recipe's ingredients
calculate_button = tk.Button(root, text="Calculate Ingredients", command=display_recipe_ingredients)