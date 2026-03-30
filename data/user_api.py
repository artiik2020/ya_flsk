import flask
from flask import jsonify, make_response, request

from data import db_session
from data.db_session import global_init, create_session
from data.users import User

blueprint = flask.Blueprint(
    'user_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/user', methods=['POST'])
def create_news():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['id', 'surname', 'name', 'age', "position", "speciality", "address", "email"]):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    users = User(
        id=request.json['id'],
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email']
    )
    db_sess.add(User)
    db_sess.commit()
    return jsonify({'id': User.id})


@blueprint.route('/api/user/<id>', methods=['GET'])
def get_news(id):
    global_init("db/blogs.db")
    db_sess = create_session()
    users = db_sess.query(User).filter(User.id == id)
    return jsonify(
        {
            'news':
                [item.to_dict(only=(
                    'id', 'team_leader', 'job', "work_size", "collaborators", "start_date", "end_date", "is_finished"))
                    for item in users]
        }
    )


@blueprint.route('/api/user/<id>', methods=['DELETE'])
def delete_news(news_id):
    db_sess = db_session.create_session()
    users = db_sess.get(User, news_id)
    if not users:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(users)
    db_sess.commit()
    return jsonify({'success': 'OK'})
