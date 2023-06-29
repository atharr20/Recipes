from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import users_model



class Party:
    DB= 'recipes1'

    def __init__(self, data):
        self.id= data['id']
        self.what= data['what']
        self.location= data['location']
        self.date= data['date']
        self.all_ages= data['all_ages']
        self.description= data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']


    @staticmethod
    def validate_party(new_party):
        is_valid = True
        if len(new_party['what']) <3:
            flash('What field must be at least 3 characters long')
            is_valid = False
        is_valid = True
        if len(new_party['location']) <3:
            flash('Location must be at least 3 characters long')
            is_valid = False
        if len(new_party['date'])<1:
            flash('Date field is required')
            is_valid = False
        if 'all_ages' not in new_party:
            flash('All ages is required')
            is_valid = False
        if len(new_party['description']) <4:
            flash('Description must be 4 or more characters long')
            is_valid= False
        
        return is_valid

    
    @classmethod
    def create_party(cls, data):
        query="""
        INSERT INTO parties (what, location, date, all_ages, description,user_id)
        VALUES (%(what)s, %(location)s, %(date)s, %(all_ages)s, %(description)s, %(user_id)s);
        """

        result=connectToMySQL(cls.DB).query_db(query, data)

        return result
    
    @classmethod
    def get_all_parties(cls):
        query="""
        SELECT * FROM parties
        JOIN users ON users.id=parties.user_id;
        """

        result=connectToMySQL(cls.DB).query_db(query)
    
        all_parties=[]

        for row in result:

            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at'],
            }
            one_party=cls(row)
            one_party.party_poster= users_model.User(user_data)
            all_parties.append(one_party)
        return all_parties
    
    @classmethod
    def get_one_party(cls, data):
        query="""
            SELECT * FROM parties
            JOIN users ON users.id = parties.user_id
            WHERE parties.id = %(party_id)s ;
        """

        result= connectToMySQL(cls.DB).query_db(query, data)

        one_party= cls(result[0])

        user_data = {
                'id': result[0]['users.id'],
                'first_name': result[0]['first_name'],
                'last_name': result[0]['last_name'],
                'email': result[0]['email'],
                'password': result[0]['password'],
                'created_at': result[0]['users.created_at'],
                'updated_at': result[0]['users.updated_at']
            }
        
        one_party.party_poster = users_model.User(user_data)
        return one_party
    
    @classmethod
    def update_party(cls, data):
        query= """
        UPDATE parties
        SET what = %(what)s, location= %(location)s, date= %(date)s, 
        all_ages= %(all_ages)s, description = %(description)s 
        WHERE id = %(party_id)s;
        """

        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def destroy(cls, data):
        query="""
        DELETE FROM parties
        WHERE id= %(party_id)s;
        """
        return connectToMySQL(cls.DB).query_db(query, data)