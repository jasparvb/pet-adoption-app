"""Adoption Agency application."""

from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, Pet
from forms import AddPetForm

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:41361@localhost/adoption_agency"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

db.drop_all()
db.create_all()

@app.route("/")
def home():
    """Shows list of pets"""
    pets = Pet.query.all()
    return render_template("home.html", pets=pets)

##############################################################################################
# PETS
##############################################################################################

@app.route("/users/")
def list_users():
    """List users"""
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show info on a single user."""
    user = User.query.get_or_404(user_id)
    return render_template("user.html", user=user)

@app.route("/add", methods=['GET', 'POST'])
def add_user():
    """Add pet and redirect to home"""
    form = AddPetForm()

    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data

        pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes)

        db.session.add(pet)
        db.session.commit()
        flash(f"Added {name}")
        return redirect("/")

    else:
        return render_template("add-pet.html", form=form)

@app.route("/users/<int:user_id>/edit", methods=['GET', 'POST'])
def edit_user(user_id):
    """Edit info of a single user"""
    user = User.query.get_or_404(user_id)
    if request.method == 'GET':
        return render_template("edit-user.html", user=user)
    else:
        user.first_name = request.form['first-name']
        user.last_name = request.form['last-name']
        user.image_url = request.form['image-url'] if request.form['image-url'] else None

        if user.first_name and user.last_name:
            db.session.add(user)
            db.session.commit()

            return redirect("/users")
        else:
            flash('Name fields cannot be blank')
            return render_template("edit-user.html")

@app.route("/users/<int:user_id>/delete", methods=['POST'])
def delete_user(user_id):
    """Delete the user"""
    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect("/users")

##############################################################################################
# POSTS
##############################################################################################

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show info on a single post."""
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", post=post)

@app.route("/users/<int:user_id>/posts/new", methods=['GET', 'POST'])
def add_post(user_id):
    """Show add a post form and handle post submission"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    if request.method == 'GET':
        return render_template("add-post.html", user=user, tags=tags)
    else:
        title = request.form['title']
        content = request.form['content']
        post_tags = request.form.getlist('tags')

        if title and content:
            post = Post(title=title, content=content, user_id=user_id)
            for post_tag in post_tags:
                tag = Tag.query.filter_by(name=post_tag).one()
                post.tags.append(tag)
            db.session.add(post)
            db.session.commit()

            return redirect(f"/users/{user_id}")
        else:
            flash('Title and content cannot be blank')
            return render_template("add-post.html", user=user, tags=tags)

@app.route("/posts/<int:post_id>/edit", methods=['GET', 'POST'])
def edit_post(post_id):
    """Show edit a post form and handle editing post"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    if request.method == 'GET':
        return render_template("edit-post.html", post=post, tags=tags)
    else:
        post.title = request.form['title']
        post.content = request.form['content']
        post_tags = request.form.getlist('tags')
        if post.title and post.content:
            post.tags = []
            for post_tag in post_tags:
                tag = Tag.query.filter_by(name=post_tag).one()
                post.tags.append(tag)
            db.session.add(post)
            db.session.commit()

            return redirect(f"/posts/{post_id}")
        else:
            flash('Title and content cannot be blank')
            return render_template("edit-post.html", post=post, tags=tags)

@app.route("/posts/<int:post_id>/delete", methods=['POST'])
def delete_post(post_id):
    """Delete the post"""
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

##############################################################################################
# TAGS
##############################################################################################

@app.route("/tags/")
def list_tags():
    """Return list of tags"""
    tags = Tag.query.all()
    return render_template("tags.html", tags=tags)

@app.route("/tags/<int:tag_id>")
def show_tag(tag_id):
    """Show info on a single tag."""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tag.html", tag=tag)

@app.route("/tags/new", methods=['GET', 'POST'])
def add_tag():
    """Add tag and redirect to tag list"""
    if request.method == 'GET':
        return render_template("add-tag.html")
    else:
        name = request.form['name']

        tags = [t.name for t in Tag.query.all()]
        if name in tags:
            flash('That tag already exists')
            return render_template("add-tag.html")
        if name:
            tag = Tag(name=name)
            db.session.add(tag)
            db.session.commit()

            return redirect("/tags")
        else:
            flash('Name field cannot be blank')
            return render_template("add-tag.html")


@app.route("/tags/<int:tag_id>/edit", methods=['GET', 'POST'])
def edit_tag(tag_id):
    """Edit info of a single tag"""
    tag = Tag.query.get_or_404(tag_id)
    if request.method == 'GET':
        return render_template("edit-tag.html", tag=tag)
    else:
        name = request.form['name']

        tags = [t.name for t in Tag.query.all()]
        if name in tags and name != tag.name:
            flash('That tag already exists')
            return render_template("edit-tag.html", tag=tag)
        if name:
            tag.name = name
            db.session.add(tag)
            db.session.commit()

            return redirect("/tags")
        else:
            flash('Name field cannot be blank')
            return render_template("edit-tag.html", tag=tag)

@app.route("/tags/<int:tag_id>/delete", methods=['POST'])
def delete_tag(tag_id):
    """Delete the tag"""
    Tag.query.filter_by(id=tag_id).delete()
    db.session.commit()

    return redirect("/tags")
