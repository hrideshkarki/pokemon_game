
how to route to 

@app.route(‘/’)
def homePage():
	user  = 


	

index.html:

{% if current_user.is_authenticated %}
	<ul class="list-group">
	{% for u in users %}

	 	{% if u.id != current_user.id %}

 			 <li class="list-group-item”>{{. u.username }}</li>
</ul>
{%. ednfor %}
￼


how to like a post:

create a route

 /like/ <post-id>

to unlike

 @app.route(‘/like/ <post-id>’)



make table in db

class Like(db.model):
	id = db.Column(db.integer, primary_key = True)
	user_id = db.Column(db.Interger, db = ForeignKey(‘user_id’), nullable = False)
	post_id = db.Column(db.Interger, db = ForeignKey(‘user_id’), nullable = False)
	
	def __init__(self, user_id, post_id):
		self.user_id = user_id
		self.post_id = post_id
	def saveToDB(self):
        	db.session.add(self)
        	db.session.commit()

   	 def saveChanges(self):
        	db.session.commit


you can define your table name:

__tablename__ = ‘ownName’

class Coment(db.model):
	id = db.Column(db.integer, primary_key = True)
	user_id = db.Column(db.Interger, db = ForeignKey(‘user_id’), nullable = False)
	post_id = db.Column(db.Interger, db = ForeignKey(‘user_id’), nullable = False)
	meassage = db.Column(String(300), nullable = False)

--------------------------====================----------


add this on models.py 

likers = db.relationship("Like", lazy=True)

# add heart/filled in heart

{% if current_user in p.likers %}
                        <span class="my-heart material-symbols-outlined" style="font-variation-settings:'FILL' 1,'wght' 400,'GRAD' 0,'opsz' 48">
                            favorite
                            </span>
                        {% else %}
                        <span class="my-heart material-symbols-outlined">
                            favorite
                            </span>
                    {% endif %}



import like from models
@app.route('/post/like/<int:post_id>')
@login_required
def likePost(post_id):
    like = Like(current_user_id, pos_id)
    like.saveToDB()

    return redirect(url_for('showAllPost'))


@app.route('/post/unlike/<int:post_id>')
@login_required
def unlikePost(post_id):
    like = Like.query.get
    like.saveToDB()

    return redirect(url_for('showAllPost'))