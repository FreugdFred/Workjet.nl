from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from flask_login import current_user, login_required

from .Models import Blogformat, Likeformat, Dislikeformat
from website import db

from website.defs.Allforms import BlogForm
from website.defs.Admindecorator import admin_only
from website.defs.Jsonlanguage import get_json_language


blog_blueprint = Blueprint('Blog', __name__)
bloglike_blueprint = Blueprint('Bloglike', __name__)
blogget_blueprint = Blueprint('Blogget', __name__)
blogadminpost_blueprint = Blueprint('Blogadmin', __name__)
blogadmindelete_blueprint = Blueprint('Blogadmin', __name__)


@blog_blueprint.route('/blog', methods=['GET'])
@login_required
def blog():
    return render_template('Blog.html', user=current_user, language_dict=get_json_language())


@bloglike_blueprint.route('/blog/like/<post_id>/<like>', methods=['GET'])
@login_required
def bloglike(post_id, like):
    post = Blogformat.query.filter_by(id=post_id).first()

    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)

    like_post = Likeformat.query.filter_by(
        blog_id=post.id, likes=current_user.id).first()
    dislike_post = Dislikeformat.query.filter_by(
        blog_id=post.id, dislikes=current_user.id).first()

    # if user wants to like and has not already have a like, create one
    if like == 'like' and not like_post:
        judge_post = Likeformat(likes=current_user.id, blog_id=post.id)
        db.session.add(judge_post)

        # if user disliked before, delete that
        if dislike_post:
            db.session.delete(dislike_post)

    # if user wants to dislike and has not already have a dislike, create one
    if like == 'dislike' and not dislike_post:
        judge_post = Dislikeformat(dislikes=current_user.id, blog_id=post.id)
        db.session.add(judge_post)

        # if user liked before, delete that
        if like_post:
            db.session.delete(like_post)

    # if user wanted to delete
    if like == 'delete':
        if like_post:
            db.session.delete(like_post)

        elif dislike_post:
            db.session.delete(dislike_post)

    db.session.commit()
    return {'succes': '200'}


@blogget_blueprint.route('/blog/get', methods=['GET'])
@login_required
def blogget():
    pagenumber = request.args.get('pagenumber')
    query = db.session.query(Blogformat)

    try:
        pages_blogs = query.paginate(int(pagenumber), 10, False).items
    except TypeError:
        pages_blogs = query.paginate(1, 10, False).items

    page_blog_list = []

    for blog in pages_blogs:
        temp_dict = vars(blog)
        likes_count, dislikes_count = get_like_number(temp_dict['id'])

        temp_dict['likes'] = likes_count
        temp_dict['dislikes'] = dislikes_count
        del temp_dict['_sa_instance_state']

        temp_dict |= did_like(temp_dict['id'])

        page_blog_list.append(temp_dict)

    return jsonify(page_blog_list)


@blogadminpost_blueprint.route('/blog/post/admin', methods=['GET', 'POST'])
@login_required
@admin_only
def blogpostadmin():
    form = BlogForm()

    if form.validate_on_submit() and request.method == 'POST':
        post_blog_database(form)
        return redirect(url_for('blog.blog'))

    return render_template('Blogpost.html', user=current_user, form=form, language_dict=get_json_language())


@blogadmindelete_blueprint.route('/blog/delete/admin/<blog_id>', methods=['GET'])
@login_required
@admin_only
def blogdeleteadmin(blog_id):
    likes_post = Likeformat.query.filter_by(blog_id=blog_id).all()
    dislikes_post = Dislikeformat.query.filter_by(blog_id=blog_id).all()
    post = Blogformat.query.filter_by(id=blog_id).first()

    if likes_post:
        for likes in likes_post:
            db.session.delete(likes)

    if dislikes_post:
        for dislikes in dislikes_post:
            db.session.delete(dislikes)

    if post:
        db.session.delete(post)

    db.session.commit()

    return redirect(url_for('blogpostadmin.blogpostadmin'))


def get_like_number(blog_id):
    likes = Likeformat.query.filter_by(blog_id=blog_id).count()
    dislikes = Dislikeformat.query.filter_by(blog_id=blog_id).count()
    return likes, dislikes


def post_blog_database(form):
    post_title = form.post_title.data
    post_text = form.post_text.data
    post_creator = form.post_creator.data

    New_blog = Blogformat(post_title=post_title,
                          post_text=post_text, post_creator=post_creator)
    db.session.add(New_blog)
    db.session.commit()


def did_like(blog_id):
    if Likeformat.query.filter_by(blog_id=blog_id, likes=current_user.id).first():
        return {'did_like': 'like'}

    elif Dislikeformat.query.filter_by(blog_id=blog_id, dislikes=current_user.id).first():
        return {'did_like': 'dislike'}

    return {}


# bcfzzsjuiaujgwkdga@tcwlx.com
