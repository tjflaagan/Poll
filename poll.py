from flask import Flask, render_template, Response, request, redirect, url_for, jsonify, session
from models import db, Options, Topics, Polls
import random, string


# WTF Form imports
from flask_wtf import Form
from wtforms import StringField, FieldList, FormField
from flask_migrate import Migrate
# Supporting
from supporting import GetPoll

poll = Flask(__name__)

# load config from the config file we created earlier
poll.config.from_object('config')

# initialize and create the database
db.init_app(poll)
db.create_all(app=poll)
migrate = Migrate(poll, db)

# Home route
@poll.route('/')
def home():
	return render_template('index.html')

# Creation routes
@poll.route('/create', methods=['GET','POST'])
def create():
	if request.method == "GET":	
		topic_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
		topic_temp = Topics(topic_id) 
		db.session.add(topic_temp)
		db.session.commit()
		session['topic_id'] = topic_id
	else:
		topic_id = session.get('topic_id')
	
	return render_template("create.html", topic_id=topic_id, options={})

@poll.route('/_add_option')
def add_option():
    new_option = request.args.get('new_option', type=str)
    topic_id = request.args.get('topic_id', type=str)
    topic = Topics.query.filter_by(title=topic_id).first()

    option_temp = Options(new_option)
    db.session.add(option_temp)
    db.session.commit()
    poll_temp = Polls(topic.id, option_temp.id)
    db.session.add(poll_temp)
    db.session.commit()
    
    all_options = Polls.query.filter_by(topic_id=topic.id).all()
    ret_options = {}
    for i in all_options:
        ret_options["id"] = i.id
        ret_options["name"] = i.option.name

    return jsonify(result=ret_options)

# Poll taking routes
@poll.route('/take', methods=['GET','POST'])
def take():
    form = GetPoll()
    return render_template("take_poll.html", form=form)

@poll.route('/show_poll', methods=['GET', 'POST'])
def show_poll():

    if("poll_id" in request.form):
        poll_id = request.form["poll_id"]
        topic_id = Topics.query.filter_by(title=str(poll_id)).first()
        options = Polls.query.filter_by(topic_id=str(topic_id.id)).all()
        return render_template("show_poll.html", id=poll_id, options=options)
    else:
        selected_options = request.form.getlist("options")
        for i in selected_options:
            p = Polls.query.get(i)
            p.vote_count += 1
            db.session.commit()
        return redirect(url_for("home"))

# Poll results routes
@poll.route("/results", methods=['GET','POST'])
def results():
    form = GetPoll()
    return render_template("results.html", form=form)

@poll.route("/show_results", methods=['GET', 'POST'])
def show_results():
    poll_id = request.form["poll_id"]
    topic_id = Topics.query.filter_by(title=str(poll_id)).first()
    options = Polls.query.filter_by(topic_id=str(topic_id.id)).all()
    return render_template("show_results.html", id=poll_id, options=options)

@poll.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    poll.run()