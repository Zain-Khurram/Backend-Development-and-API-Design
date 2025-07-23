#web application framework that is used to create web application instances 
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
import os

#creates the flask application instance 
app = Flask(__name__)
#creates the API instance from the Flask application instance
api = Api(app)
#configures the SQLAlchemy database URI for the application instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
#Initializes the SQLAlchemy ORM with the Flask app.
db = SQLAlchemy(app)
#Initializes HTTP Basic Authentication.
auth = HTTPBasicAuth()

#defines a database table using a python class. Videomodel becomes the table in the SQLite database.
class VideoModel(db.Model):
    #defining columns of the table, id is the primary key
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    #method used to define how an instance of videomodel is printed 
    def __repr__(self):
        return f"Video(name = {self.name}, views = {self.views}, likes = {self.likes})"

#initiliaze parser for POST requests (when creating a new video/instance of VideoModel)
video_post_args = reqparse.RequestParser()
#defining required argument for POST request. Data type validation and error messages
video_post_args.add_argument("name", type =str, help = 'Name of the video is required', required = True)
video_post_args.add_argument("views", type =int, help = 'Views of the video is required', required = True)
video_post_args.add_argument("likes", type =int, help = 'Likes of the video is required', required = True)

#initiliaze parser for PUT requests (when updating a already existing video/instance of VideoModel)
video_put_args = reqparse.RequestParser()
#defining argument for POST request. arguments are optional for partial updates 
video_put_args.add_argument("name", type =str, help = 'Name of the video')
video_put_args.add_argument("views", type =int, help = 'Views of the video')
video_put_args.add_argument("likes", type =int, help = 'Likes of the video')

#defining the fields that will be returned in the response
resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

#authentication setup 
users = {os.getenv('USER'): os.getenv('PASSWORD')}

#validates provided credentials
@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username
    return None

class Video(Resource):
    @auth.login_required
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video ID does not exist")
        return result

    @auth.login_required
    @marshal_with(resource_fields)
    def post(self, video_id):
        args = video_post_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video ID already exists")
        video = VideoModel(id = video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201
    
    @auth.login_required
    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video ID does not exist")

        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']

        db.session.commit()
        return result, 200
    
    @auth.login_required
    def delete(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video ID does not exist")
        db.session.delete(result)
        db.session.commit()
        return '', 201

api.add_resource(Video, '/video/<int:video_id>')

if __name__ == '__main__':
    app.run(debug=True)
