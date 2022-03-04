from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
from flask_app.models import plant
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def __eq__(self, other) -> bool:
        return self.id == other.id and type(self) is type(other)

# Not in use right now -- for home page
    # @classmethod
    # def get_all_users_with_all_plants(cls, data): #is a one to many but modeled like a many to many
    #     query = "SELECT * FROM users JOIN plants ON users.id = user_id;"
    #     results = connectToMySQL('project').query_db(query, data)
    #     if results:
    #         all_users = []
    #         for row in results:
    #             user = cls(row)
    #             if user not in all_users:
    #                 user.plants_created = []
    #                 for plant_row in results:
    #                     if plant_row['user_id'] == user.id:
    #                         plant_data = {
    #                             **plant_row,
    #                             'id': plant_row['plants.id'],
    #                             'created_at': plant_row['plants.created_at'],
    #                             'updated_at': plant_row['plants.updated_at']
    #                         }
    #                         one_plant = plant.Plant(plant_data)
    #                         user.plants_created.append(one_plant)
    #                 all_users.append(user)
                    
    @classmethod
    def get_one_user_with_all_plants(cls, data):
        query = "SELECT * FROM users LEFT JOIN plants ON users.id = user_id WHERE users.id = %(id)s;"
        results = connectToMySQL('project').query_db(query, data)
        if results:
            user = cls(results[0])
            user.plants_created = []
            for row in results:
                plant_data = {
                    **row,
                    'id': row['plants.id'],
                    'created_at': row['plants.created_at'],
                    'updated_at': row['plants.updated_at']
                }
                plants = plant.Plant(plant_data)
                user.plants_created.append(plants)
            return user



    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, email, password, created_at, updated_at) VALUES ( %(first_name)s, %(email)s, %(password)s, NOW(), NOW() );"
        return connectToMySQL('project').query_db(query, data)





    # Validations
    @staticmethod
    def validate_reg(user):
        print(user)
        is_valid = True
        if len(user['first_name']) <3:
            flash("Name must be atleast 3 characters.", 'reg')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email address', 'reg')
            is_valid = False
        if len(user['password']) < 8:
            flash('Password must be at least 8 characters long.', 'reg')
            is_valid = False
        if user['password'] != (user['password_confirm']):
            flash('Password does not match', 'reg')
            is_valid = False
        return is_valid

    @classmethod
    def validate_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('project').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])
