from flask import jsonify, request, session, make_response
from app import db
from . import main_bp
from app.models.User import User, Post, followers


@main_bp.route("/all-posts")
def get_all_posts():
    # get current user
    current_user_id = session.get('user_id')
    if current_user_id is None:
        return make_response({
            "error": "Unauthorized"
        }, 401)
    current_user = User.query.filter_by(id=current_user_id).first()

    # get all posts of followed and unfollowed authors
    query_posts = Post.query.order_by(Post.timestamp.desc()).limit(20).all()
    posts = []
    for query_post in query_posts:
        query_post_info = query_post.get_info()
        author = User.query.filter_by(id=query_post_info["author"]["id"]).first()
        is_author_current_user = current_user_id == query_post_info["author"]["id"]
        post = {
            "postId": query_post_info["postId"],
            "author": {
                'id': query_post_info["author"]["id"],
                'username': query_post_info["author"]["username"]
            },
            "body": query_post_info["body"],
            "timestamp": query_post_info["timestamp"].strftime("%x"),
            "is_following": current_user.is_following(author),
            "is_author_current_user": is_author_current_user
        }
        posts.append(post)
    print(current_user.is_following(current_user))
    return jsonify({
        'posts': posts
    })


@main_bp.route("/followed-posts")
def get_followed_posts():

    followed_posts = User.followed_posts()
    print(followed_posts)
    return


@main_bp.route("/my-profile")
def get_my_profile():
    # get current user
    current_user_id = session.get('user_id')
    if current_user_id is None:
        return make_response({
            "error": "Unauthorized"
        }, 401)
    current_user = User.query.filter_by(id=current_user_id).first()

    query_posts = current_user.posts.order_by(Post.timestamp.desc()).limit(10).all()
    posts = []
    for query_post in query_posts:
        query_post_info = query_post.get_info()
        post = {
            "postId": query_post_info["postId"],
            "body": query_post_info["body"],
            "timestamp": query_post_info["timestamp"].strftime("%x")
        }
        posts.append(post)

    return jsonify({
        "username": current_user.username,
        "bio": current_user.about_me,
        "posts": posts
    })


@main_bp.route('/user-profile/<user_id>')
def get_user_profile(user_id):
    # get current user
    current_user_id = session.get('user_id')
    if current_user_id is None:
        return make_response({
            "error": "Unauthorized"
        }, 401)
    current_user = User.query.filter_by(id=current_user_id).first()

    # get user profile from id
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return make_response({
            "error": "no such user with that id"
        }, 401)

    # get user posts
    query_posts = user.posts.order_by(Post.timestamp.desc()).limit(10).all()
    posts = []
    for query_post in query_posts:
        query_post_info = query_post.get_info()
        post = {
            "postId": query_post_info["postId"],
            "author": {
               "username": query_post_info["author"]["username"]
            },
            "body": query_post_info["body"],
            "timestamp": query_post_info["timestamp"].strftime("%x")
        }
        posts.append(post)

    return jsonify({

        "username": user.username,
        "bio": user.about_me,
        "is_following": current_user.is_following(user),
        "posts": posts
    })


@main_bp.route("/add-post", methods=["POST"])
def add_post():
    # get current user
    current_user_id = session.get('user_id')
    if current_user_id is None:
        return make_response({
            "error": "Unauthorized"
        }, 401)
    current_user = User.query.filter_by(id=current_user_id).first()

    # add post
    post_body = request.json["body"]
    new_post = Post(body=post_body, author=current_user)
    db.session.add(new_post)
    db.session.commit()

    return jsonify({
        "msg": "posts added"
    })


@main_bp.route("/follow/<user_id>", methods=["POST"])
def follow_user(user_id):
    # get current user
    current_user_id = session.get('user_id')
    if current_user_id is None:
        return make_response({
            "error": "Unauthorized"
        }, 401)
    current_user = User.query.filter_by(id=current_user_id).first()

    # make sure no self follow
    if current_user_id == user_id:
        return jsonify({
            "msg": "must not follow self"
        })

    # get user to follow
    user_to_follow = User.query.filter_by(id=user_id).first()
    if user_to_follow is None:
        return make_response({
            "error": "no such user with that id"
        }, 401)
    current_user.follow(user_to_follow)
    print("current user with id " + str(current_user_id) + " followed user with id " + str(user_id))
    return jsonify({
        "msg": "followed successfully!"
    })


@main_bp.route('/unfollow/<user_id>', methods=["POST"])
def unfollow_user(user_id):
    # get current user
    current_user_id = session.get('user_id')
    if current_user_id is None:
        return make_response({
            "error": "Unauthorized"
        }, 401)
    current_user = User.query.filter_by(id=current_user_id).first()

    # make sure no self follow
    if current_user_id == user_id:
        return jsonify({
            "msg": "must not unfollow self"
        })

    # get user to unfollow
    user_to_unfollow = User.query.filter_by(id=user_id).first()
    if user_to_unfollow is None:
        return make_response({
            "error": "no such user with that id"
        }, 401)
    current_user.unfollow(user_to_unfollow)
    print("current user with id " + str(current_user_id) + " unfollowed user with id " + str(user_id))
    return jsonify({
        "msg": "unfollowed successfully!"
    })
