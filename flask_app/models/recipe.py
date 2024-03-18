
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
from flask_app import app
from flask_app.models import user

class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.date = data['date']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data ['updated_at']
        self.host_id = data['user_id']
        self.host = None

    @classmethod
    def create_recipe(cls,data):
        if not cls.validate_recipe(data) : return False
        query = """
            INSERT INTO recipes 
            (name, description, instruction, date, under_30, user_id)
            VALUES
            (%(name)s,%(description)s,%(instruction)s,%(date)s,%(under_30)s, %(user_id)s)
            ;"""
        return connectToMySQL('recipes_db').query_db(query,data)
    
    #read recipe model
    @classmethod
    def get_all_recipes_with_host(cls):
        query = """
            SELECT * FROM recipes
            JOIN users 
            ON users.id = recipes.user_id
            ;"""
        results = connectToMySQL('recipes_db').query_db(query)
        recipes = []
        for recipes_data in results:
            this_recipe = cls(recipes_data)
            this_recipe.host = user.User.parse_user(recipes_data)
            recipes.append(this_recipe)
        return recipes
    
    @classmethod
    def get_recipe_by_id_w_host(cls, id):
        data = {'id' : id }
        query = """
            SELECT * FROM recipes
            JOIN users 
            ON users.id = recipes.user_id
            WHERE recipes.id = %(id)s
            ;"""
        result = connectToMySQL('recipes_db').query_db(query, data)
        this_recipe = cls(result[0])
        this_recipe.host = user.User.parse_user(result[0])
        return this_recipe

    #update recipe model 
    @classmethod
    def update_recipe(cls, data):
        if not cls.validate_recipe(data) : return False
        query = """
            UPDATE recipes
            SET
                name = %(name)s, 
                description = %(description)s,
                instruction = %(instruction)s,
                date = %(date)s,
                under_30 = %(under_30)s
            WHERE id = %(id)s
            ;"""
        connectToMySQL('recipes_db').query_db(query,data)
        return True


    #delee recipe model 
    @classmethod
    def delete_recipe_by_id(cls, id):
        data= {'id': id}
        query = " DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL('recipes_db').query_db(query,data)
       
    #Validation 
    @classmethod
    def validate_recipe(clas,data):
        is_valid = True
        if len(data['name']) < 3:
            flash("Name must be at least 3 characters.","create_recipe")
            is_valid = False 
        if len(data['instruction']) < 3:
            flash("instruction must be at least 3 characters.","create_recipe")
            is_valid = False 
        if len(data['description']) < 3:
            flash("Description must be at least 3 characters.","create_recipe")
            is_valid = False
        if not data['date']:
            flash("A date is required.","create_recipe")
            is_valid = False
        if "under_30" not in data:
            flash("Please select under or over 30 minutes.","create_recipe")
            is_valid = False 
        return is_valid 
       