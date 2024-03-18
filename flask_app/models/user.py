from flask_app.config.mysqlconnection import connectToMySQL
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash 
from flask_app.models.recipe import Recipe

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data ['updated_at']
        self.recipe =[]
    @classmethod
    def create_user(cls, data):
        query = """
            INSERT INTO users (first_name, last_name, email, password)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
            ;"""
        return connectToMySQL("recipes_db").query_db(query,data)
    @classmethod
    def get_by_email(cls, data):
        query = """ 
            SELECT * FROM users 
            WHERE email = %(email)s
            ;"""
        results = connectToMySQL("recipes_db").query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_by_id(cls,data):
        query = """
            SELECT * FROM users 
            WHERE id = %(id)s
        ;"""
        result = connectToMySQL('recipes_db').query_db(query,data)
        print(result)
        return cls(result[0])
    
    @staticmethod
    def validate_register(user):
        is_valid = True
        query = """
            SELECT * FROM users 
            WHERE email = %(email)s
            ;"""
        results = connectToMySQL("recipes_db").query_db(query,user)
        if len(results) >= 1:
            flash ("Email already taken.","register")
            is_valid = False 
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!","register")
            is_valid = False
        if len(user['first_name']) < 2:
            flash("First Name must be at least 2 characters ","register")
            is_valid = False 
        if len(user['last_name']) < 2:
            flash("Last Name must be at least 2 characters ","register")
            is_valid = False 
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid = False 
        if user['password'] != user['confirm_password']:
            flash("Passwords must match", "register")
            is_valid = False
        return is_valid
    
    #parse user data`
    @classmethod
    def parse_user(cls, data):
        if 'users.id' in data:
            return(cls({
                'id' : data['users.id'],
                'first_name' : data['first_name'],
                'last_name' : data['last_name'],
                'email' : data['email'],
                'password' : data['password'],
                'created_at' : data['users.created_at'],
                'updated_at' : data['users.updated_at']
            }))
        return cls(data)