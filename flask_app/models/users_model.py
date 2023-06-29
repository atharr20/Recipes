from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re 
from flask_app.models import parties_model

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')



class User:
    DB= 'recipes1'

    def __init__(self, data):
        self.id= data['id']
        self.first_name= data['first_name']
        self.last_name= data['last_name']
        self.email= data['email']
        self.password= data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.parties= []

    @staticmethod
    def validate_user(new_user):
        is_valid = True
        if len(new_user['first_name']) <3:
            flash('First name must be at least 3 characters long')
            is_valid = False
        is_valid = True
        if len(new_user['last_name']) <3:
            flash('Last name must be at least 3 characters long')
            is_valid = False
        if not EMAIL_REGEX.match(new_user['email']):
            flash('Please enter a valid email')
            is_valid=False
        if len(new_user['password']) <4:
            flash('Password must be 4 or more characters long')
            is_valid= False
        if new_user['password']!= new_user['confirm_password']:
            flash('Passwords did not match')
            is_valid= False
        
        return is_valid




    @classmethod
    def Save_User(cls,data):
        query="""
        INSERT INTO users (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        """

        result=connectToMySQL(cls.DB).query_db(query, data)

        return result
    
    @classmethod
    def GetUserByID(cls, data):
        query="""
        SELECT * FROM users
        WHERE id = %(id)s;
        """

        result=connectToMySQL(cls.DB).query_db(query, data)

        return cls(result[0])
    

    @classmethod
    def GetUserByEmail(cls, data):
        query="""
        SELECT * FROM users 
        WHERE email= %(email)s;
        """
        result=connectToMySQL(cls.DB).query_db(query, data)

        if len(result)<1:
            return False
        return cls(result[0])
    
    @classmethod
    def GetMyParties(cls, data):
        query= """
        SELECT * FROM users
        JOIN parties ON users.id = parties.user_id
        WHERE users.id = %(user_id)s;
        """

        result= connectToMySQL(cls.DB).query_db(query, data)

        one_user= cls(result[0])

        for row in result:

            party_data= {
                'id': row['parties.id'],
                'what': row['what'],
                'location': row['location'],
                'date': row['date'],
                'all_ages': row['all_ages'],
                'description': row['description'],
                'created_at': row['parties.created_at'],
                'updated_at': row['parties.updated_at'],
                'user_id' : row['user_id']
            }
            one_user.parties.append(parties_model.Party(party_data))

        return one_user

