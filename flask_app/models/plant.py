from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
from flask_app.models import user
import base64
from base64 import b64encode



class Plant:
    def __init__(self, data) :
        self.id = data['id']
        self.scientific_name = data['scientific_name']
        self.nickname = data['nickname']
        self.health = data['health']
        self.notes = data['notes']
        self.img = data['img']
        self.user_id = data['user_id']

    @staticmethod
    def render_picture(data):
        render_pic = base64.b64encode(data).decode('ascii')
        return render_pic

    @classmethod
    def get_one_plant_with_user(cls, data):
        query = "SELECT * FROM plants JOIN users ON user_id = users.id WHERE plants.id = %(id)s;"
        results = connectToMySQL('project').query_db(query, data)

        if results:
            row = results[0]
            # if type(row['img']) is bytes:
            #     print('type of row.img', type(row['img']))
            #     image = cls.render_picture(row['img'])
            #     row['img'] = image

            one_plant = cls(row)
            user_data = {
                **row,
                'id': row['users.id'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            one_plant.creator = user.User(user_data)
            return one_plant




    @classmethod
    def delete(cls,data):
        query = "DELETE FROM plants WHERE id = %(id)s;"
        return connectToMySQL('project').query_db(query,data)


    @classmethod
    def save(cls, data):
        image = cls.render_picture(data['img'])
        data['img'] = image
        query = "INSERT INTO plants (scientific_name, nickname, health, notes, img, created_at, updated_at, user_id) VALUES ( %(scientific_name)s, %(nickname)s, %(health)s, %(notes)s, %(img)s,  NOW(), NOW(), %(user_id)s);"
        return connectToMySQL('project').query_db(query, data)


    @classmethod
    def update(cls, data):
        image = cls.render_picture(data['img'])
        data['img'] = image
        query = "UPDATE plants SET scientific_name=%(scientific_name)s, nickname=%(nickname)s, health=%(health)s, notes=%(notes)s, img=%(img)s, created_at= NOW(), updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL('project').query_db(query, data)






# VALIDATIOINS
    @staticmethod
    def validate_plant(plant):
        print(plant)
        is_valid = True
        if len(plant['scientific_name']) <3:
            flash('Scientific name must be at least 3 characters long.', 'plant')
            is_valid = False
        if len(plant['nickname']) <3:
            flash('Nickname must be at least 3 characters long.', 'plant')
            is_valid = False
        if len(plant['notes']) <3:
            flash('Notes must be at least 3 characters long.', 'plant')
            is_valid = False
        return is_valid