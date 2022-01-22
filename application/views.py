from flask import Blueprint, render_template, request, flash, jsonify, Markup, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, BodyImage, Note
from . import db
import json
import os

views = Blueprint('views', __name__)

# Home
@views.route('/')
def home():
  posts = Post.query.all()
  return render_template("home.html", user=current_user, posts=posts)

# Blog
@views.route('/blog')
def blog():
  posts = Post.query.all()
  return render_template("blog.html", user=current_user, posts=posts)

# Projects
@views.route('/projects')
def projects():
  return render_template("projects.html", user=current_user)

# About
@views.route('/about')
def about():
  return render_template("about.html", user=current_user)

# Wall
@views.route('/wall', methods=['GET', 'POST'])
@login_required
def wall():
  if request.method == 'POST':
    note = request.form.get('note')

    if len(note) < 1:
      flash('Note is too short!', category='error')
    else:
      new_note = Note(data=note, user_id=current_user.id)
      db.session.add(new_note)
      db.session.commit()
      flash('Note added!', category='success')

  return render_template("wall.html", user=current_user)

# Delete note
@views.route('/delete-note', methods=['POST'])
def delete_note():
  note = json.loads(request.data)
  noteId = note['noteId']
  note = Note.query.get(noteId)
  if note:
    if note.user_id == current_user.id:
      db.session.delete(note)
      db.session.commit()
  
  return jsonify({})

# Create post
@views.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():

  post_id = Post.query.order_by(Post.id.desc()).first()
  if post_id:
      post_id = str(int(post_id.id) + 1)
  else:
      post_id = "1"

  # if request.method == "GET":
      
  # else:   
  if request.method == 'POST':
    title = request.form.get('title')
    content = request.form.get('content')
    snippet = request.form.get('snippet')

    feature_image = request.files["feature_image"]
    if feature_image.filename != "":
        # image folder and save location need to be usable from top level of directory
        img_folder = os.path.join("application", "static", "post_imgs", post_id)
        if not os.path.exists(img_folder):
            os.makedirs(img_folder)
        feature_image.save(os.path.join(img_folder, feature_image.filename))
        # 'feature_image_path' assumes we're in the 'templates' directory
        feature_image_path = os.path.join("static", "post_imgs", post_id, feature_image.filename)
    else:
        feature_image_path = None

    feature_video_link = request.form["feature_video_link"]

    post_url = title.replace(" ", "-").lower()

    if not title or not content:
      flash('Please enter title and content.', category='error')
      return render_template("create-post.html", user=current_user) 
    else:
      post = Post(title=title, content=content, snippet=snippet, feature_image_path=feature_image_path, feature_video_link=feature_video_link, post_url=post_url, author=current_user.id)
      db.session.add(post)

    for img in request.files.getlist("body_imgs"):
      if img.filename != "":
          # image folder and save location need to be usable from top level of directory
          img_folder = os.path.join("application", "static", "post_imgs", post_id)
          if not os.path.exists(img_folder):
              os.makedirs(img_folder)
          img.save(os.path.join(img_folder, img.filename))
          # img_path assumes we're in the 'templates' directory
          img_path = os.path.join("static", "post_imgs", post_id, img.filename)
          img_data = BodyImage(post_id=post_id, img_path=img_path)
          db.session.add(img_data)
      
    db.session.commit()
    flash('Post created', category='success')
  else:
    return render_template("create-post.html", user=current_user) 
    
  return redirect(url_for('views.blog'))

# Post
@views.route('/post/<post_url>', methods=["GET"])
def post(post_url):
  post = Post.query.filter_by(post_url=post_url).first()
  imgs = BodyImage.query.filter_by(post_id=post.id).all()
  print(imgs)
  
  content = Markup(post.content).format(imgs=imgs)
  print(content)
  return render_template("post.html", post=post, content=content)

# Delete post
@views.route('/delete-post/<id>', methods=['GET','POST'])
@login_required
def delete_post(id):
  post = Post.query.filter_by(id=id).first()
  
  if not post:
    flash("Post does not exist.", category='error')
  else:
      db.session.delete(post)
      db.session.commit()
      flash("Post deleted.", category='success')

  return redirect(url_for('views.blog'))

# Edit post
@views.route("/edit-post/<id>", methods=["GET", "POST"])
@login_required
def edit_post(id):
    post = Post.query.filter_by(id=id).first()

    post_id = post.id#Post.query.order_by(Post.id.desc()).first()
    # if post_id:
    #     post_id = str(int(post_id.id) + 1)
    # else:
    #     post_id = "1"
    
    if request.method == "GET":
      return render_template("edit-post.html", post=post, user=current_user)
    else:
      post.title = request.form.get('title')
      post.content = request.form.get('content')
      post.snippet = request.form.get('snippet')

      feature_image = request.files["feature_image"]
      if feature_image.filename != "":
          # image folder and save location need to be usable from top level of directory
          img_folder = os.path.join("application", "static", "post_imgs", post_id)
          if not os.path.exists(img_folder):
              os.makedirs(img_folder)
          feature_image.save(os.path.join(img_folder, feature_image.filename))
          # 'feature_image_path' assumes we're in the 'templates' directory
          feature_image_path = os.path.join("static", "post_imgs", post_id, feature_image.filename)
      else:
          feature_image_path = None
      
      post.feature_image_path = feature_image_path

      post.feature_video_link = request.form["feature_video_link"]

      post.post_url = post.title.replace(" ", "-").lower()

      # if not title or not content:
      #   flash('Please enter title and content.', category='error')
      # else:
      #   post = Post(id=post_id, title=title, content=content, snippet=snippet, feature_image_path=feature_image_path, feature_video_link=feature_video_link, post_url=post_url, author=current_user.id)
      #   db.session.add(post)

      for img in request.files.getlist("body_imgs"):
        if img.filename != "":
            # image folder and save location need to be usable from top level of directory
            img_folder = os.path.join("application", "static", "post_imgs", post_id)
            if not os.path.exists(img_folder):
                os.makedirs(img_folder)
            img.save(os.path.join(img_folder, img.filename))
            # img_path assumes we're in the 'templates' directory
            img_path = os.path.join("static", "post_imgs", post_id, img.filename)
            img_data = BodyImage(post_id=post_id, img_path=img_path)
            db.session.add(img_data)
        
      db.session.commit()
      flash('Post edited', category='success')
    
    #return render_template("home.html", user=current_user)
    return redirect(url_for('views.blog'))