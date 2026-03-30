import flask
from flask import jsonify, make_response, request

from data import db_session
from data.db_session import global_init, create_session
from data.jobs import Jobs

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs', methods=['POST'])
def create_news():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['id', 'team_leader', 'job', 'work_size', "collaborators", "start_date", "end_date", "is_finished"]):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    jobs = Jobs(
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished']
    )
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'id': jobs.id})


@blueprint.route('/api/jobs/<id>')
def get_news(id):
    global_init("db/blogs.db")
    db_sess = create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id)
    return jsonify(
        {
            'news':
                [item.to_dict(only=(
                    'id', 'team_leader', 'job', "work_size", "collaborators", "start_date", "end_date", "is_finished"))
                    for item in jobs]
        }
    )


@blueprint.route('/api/news/<id>', methods=['DELETE'])
def delete_news(news_id):
    db_sess = db_session.create_session()
    jobs = db_sess.get(Jobs, news_id)
    if not jobs:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})
