from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from data import db_session
from data.regpars_jobs import parser
from data.jobs import Jobs


def abort_if_Jobs_not_found(jobs_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(jobs_id)
    if not jobs:
        abort(404, message=f"Jobs {jobs_id} not found")


class JobsResource(Resource):
    def get(self, jobs_id):
        abort_if_Jobs_not_found(jobs_id)
        session = db_session.create_session()
        jobs = session.get(Jobs, jobs_id)
        return jsonify({'jobs': jobs.to_dict(only=(
                    'id', 'team_leader', 'job', "work_size", "collaborators", "start_date", "end_date", "is_finished"))})

    def delete(self, jobs_id):
        abort_if_Jobs_not_found(jobs_id)
        session = db_session.create_session()
        jobs = session.get(Jobs, jobs_id)
        session.delete(jobs)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict(only=(
                    'id', 'team_leader', 'job', "work_size", "collaborators", "start_date", "end_date", "is_finished")) for
            item in jobs]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        jobs = Jobs(
            team_leader=args['team_leader'],
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args('collaborators'),
            start_date=args('start_date'),
            end_date=args('end_date'),
            is_finished=args('is_finished')
        )
        session.add(jobs)
        session.commit()
        return jsonify({'OK'})
