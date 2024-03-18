from flask_app import app 
from flask import render_template, redirect, session, flash, request
from flask_app.models import recipe
from flask_app.models.user import User

@app.route('/recipes')
def show_all_recipes():
    if 'user_id' not in session:
        return redirect ('/')
    data = {
        'id': session['user_id']
    }
    user = User.get_by_id(data)
    recipes = recipe.Recipe.get_all_recipes_with_host()
    return render_template("recipes.html", recipes= recipes, user= user)

@app.route('/recipes/new')
def new_recipe():
    if 'user_id' not in session:
        return redirect ('/')
    return render_template("create_recipes.html")

@app.route('/recipes/new', methods=['POST'])
def create_recipe():
    if recipe.Recipe.create_recipe(request.form):
        return redirect('/recipes')
    return redirect('/recipes/new')

#read recipe controller 
@app.route('/recipes/view/<int:id>')
def view_recipe(id):
    if 'user_id' not in session:
        return redirect ('/')
    data = {
        'id': session['user_id']
    }
    user = User.get_by_id(data)
    this_recipe = recipe.Recipe.get_recipe_by_id_w_host(id)
    return render_template("view_recipe.html", recipe= this_recipe, user=user)

#update recipe controller
@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect ('/logout')
    this_recipe = recipe.Recipe.get_recipe_by_id_w_host(id)
    return render_template("edit_recipe.html", recipe= this_recipe)

@app.route('/recipes/edit', methods=['POST'])
def update_recipe():
    if recipe.Recipe.update_recipe(request.form):
        return redirect('/recipes')
    return redirect(f"/recipes/edit/{request.form['id']}")


#delete recipe controller
@app.route('/recipes/delete/<int:id>')
def delete_recipe(id):
    recipe.Recipe.delete_recipe_by_id(id)
    return redirect('/recipes')
   