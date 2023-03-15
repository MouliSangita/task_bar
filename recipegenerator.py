import requests
import tkinter as tk
from tkinter import messagebox


class RecipeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recipe Finder")
        self.root.geometry("500x500")

        # Create GUI elements
        self.search_label = tk.Label(text="Search for a recipe:")
        self.search_label.pack()

        self.search_entry = tk.Entry()
        self.search_entry.pack()

        self.search_button = tk.Button(text="Search")
        self.search_button.pack()
        self.search_button.bind("<Button-1>", self.search_recipes)

        self.recipe_listbox = tk.Listbox()
        self.recipe_listbox.pack(fill=tk.BOTH, expand=True)
        self.recipe_listbox.bind("<Double-Button-1>", self.display_recipe)

        self.recipe_details_label = tk.Label(text="")
        self.recipe_details_label.pack(fill=tk.BOTH, expand=True)

        # API endpoint for recipe search
        self.api_endpoint = "https://api.spoonacular.com/recipes/complexSearch"

        # Your Spoonacular API key
        self.api_key = "ccdf89c1cd12407b8f8c14fa3442e9b5"

        self.recipes = []

    def search_recipes(self, event):
        # Fetch recipes from Spoonacular API
        query = self.search_entry.get()
        if query == "":
            return

        url = f"{self.api_endpoint}?apiKey={self.api_key}&query={query}"
        response = requests.get(url)
        if response.status_code != 200:
            messagebox.showerror("Error", "Unable to fetch recipes")
            return

        # Display recipes in listbox
        self.recipes = response.json()["results"]
        self.recipe_listbox.delete(0, tk.END)
        for recipe in self.recipes:
            self.recipe_listbox.insert(tk.END, recipe["title"])

    def display_recipe(self, event):
        # Check if any item is selected in the listbox
        if len(self.recipe_listbox.curselection()) == 0:
            return

        # Fetch detailed recipe information from Spoonacular API
        index = self.recipe_listbox.curselection()[0]
        recipe_id = self.recipes[index]["id"]
        url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={self.api_key}"
        response = requests.get(url)
        if response.status_code != 200:
            messagebox.showerror("Error", "Unable to fetch recipe details")
            return

        # Display recipe details in label
        recipe = response.json()
        details = f"Title: {recipe['title']}\n\n"
        details += f"Ingredients:\n"
        for ingredient in recipe["extendedIngredients"]:
            if 'originalString' in ingredient:
                details += f"- {ingredient['originalString']}\n"
            else:
                details += f"- {ingredient['name']}\n"
        details += f"\nTime: {recipe['readyInMinutes']} minutes\n"
        details += f"Serving size: {recipe['servings']}\n\n"
        details += f"Steps:\n"
        for i, step in enumerate(recipe["analyzedInstructions"][0]["steps"]):
            details += f"{i + 1}. {step['step']}\n\n"

        # Use after() to update the GUI in the main thread
        self.root.after(0, lambda: self.recipe_details_label.configure(text=details))


if __name__ == "__main__":
    root = tk.Tk()
    app = RecipeApp(root)
    root.mainloop()
