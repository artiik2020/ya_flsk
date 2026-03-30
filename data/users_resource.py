from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from data import db_session
from data.regpars_user import parser
from data.users import User


def abort_if_User_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_User_not_found(user_id)
        session = db_session.create_session()
        user = session.get(User, user_id)
        return jsonify({'user': user.to_dict(only=(
            'id', 'surname', 'name', 'age', 'position', 'speciality', 'email', 'hashed_password', 'modified_date'))})

    def delete(self, user_id):
        abort_if_User_not_found(user_id)
        session = db_session.create_session()
        user = session.get(User, user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        user = session.query(User).all()
        return jsonify({'user': [item.to_dict(only=(
            'id', 'surname', 'name', 'age', 'position', 'speciality', 'email', 'hashed_password', 'modified_date')) for
            item in user]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            surname=args['surname'],
            name=args['name'],
            email=args['name'],
            age=args('age'),
            position=args('position'),
            speciality=args('speciality')
        )
        session.add(user)
        session.commit()
        return jsonify({'OK'})
