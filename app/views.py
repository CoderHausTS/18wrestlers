from flask import render_template, flash, redirect, url_for, request
from flask_security import login_required, current_user, Security, SQLAlchemyUserDatastore, \
    user_registered, AnonymousUser
from app import app, models, db
from .forms import EditForm, PostForm, PostEditForm, ExtendedRegisterForm
from datetime import datetime
from .models import Post

#setup security dude
user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore, register_form=ExtendedRegisterForm)

#follow ourself
def follow_me(self, user, confirm_token, **extra):
    user.follow(user)
user_registered.connect(follow_me, app)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
# @login_required
def index(page=1):
    user = current_user

    # if user.is_anonymous:
    posts = models.Post.get_all_posts().paginate(page, app.config['POSTS_PER_PAGE'], False)

    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts)


@app.route('/delete/<int:id>')
@login_required
def delete(id):
    post = Post.query.get(id)
    if post is None:
        flash('Post not found')
        return redirect(url_for('index'))
    if post.author.id != current_user.id:
        flash('You cannot do that')
        return redirect(url_for('index'))
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted')
    return redirect(url_for('index'))


@app.route('/user/<nickname>', methods=['GET', 'POST'])
@app.route('/user/<nickname>/<int:page>', methods=['GET', 'POST'])
@login_required
def user(nickname, page=1):
    # we need a case insensitive query here.
    user = models.User.query.filter(models.User.nickname.ilike(nickname)).first()
    if user == None:
        flash('User {} not found.'.format(nickname))
        return redirect(url_for('index'))

    #
    # user = current_user
    #
    form = PostForm(request.form)
    if request.method == 'POST' and form.validate():
        print(form.post)
        post = Post(body=form.post.data, timestamp=datetime.utcnow(), author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('user', nickname=current_user.nickname))

    posts = user.followed_posts().paginate(page, app.config['POSTS_PER_PAGE'], False)
    # posts = user.posts.order_by(Post.timestamp.desc())
    # posts = posts.paginate(page, app.config['POSTS_PER_PAGE'], False)

    return render_template('user.html',
                           user=user,
                           posts=posts,
                           form=form)


@app.route('/follow/<nickname>')
@login_required
def follow(nickname):
    followed_user = models.User.query.filter(models.User.nickname.ilike(nickname)).first()
    if followed_user is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    if followed_user == current_user:
        flash('You can\'t follow yourself!')
        return redirect(url_for('user', nickname=nickname))
    u = current_user.follow(followed_user)
    if u is None:
        flash('Cannot follow ' + nickname + '.')
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You are now following ' + nickname + '!')
    return redirect(url_for('user', nickname=nickname))


@app.route('/unfollow/<nickname>')
@login_required
def unfollow(nickname):
    unfollowed_user = models.User.query.filter(models.User.nickname.ilike(nickname)).first()
    if unfollowed_user is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    if unfollowed_user == current_user:
        flash('You can\'t unfollow yourself!')
        return redirect(url_for('user', nickname=nickname))
    u = current_user.unfollow(unfollowed_user)
    if u is None:
        flash('Cannot unfollow ' + nickname + '.')
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You have stopped following ' + nickname + '.')
    return redirect(url_for('user', nickname=nickname))


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm(request.form, current_user.nickname)
    # we need to check if the request is of type post
    # this means taht we are trying to change the data

    if request.method == 'POST' and form.validate_nickname():
        # our form data comes as a immutable object
        # grab our new stuff and pop it, along with other current_user data
        # into the database
        current_user.nickname = request.form['nickname']
        current_user.about_me = request.form['about_me']
        db.session.add(current_user)
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('edit'))
    else:
        # if we're just doing a get, grab the data from current_user
        form.nickname.data = current_user.nickname
        form.about_me.data = current_user.about_me
    return render_template('edit.html', form=form)


@app.route('/post/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def post_edit(id):

    post = Post.query.get(id)

    if post is None:
        print('the post wasnt found')
        flash('Post not found')
        return redirect(url_for('index'))
    if post.author.id != current_user.id:
        flash('You cannot do that')
        return redirect(url_for('index'))
    # add actions here
    form = PostEditForm(request.form, post.body)
    if request.method == 'POST':

        # our form data comes as a immutable object
        # grab our new stuff and pop it, along with other current_user data
        # into the database
        post.body = request.form['body']
        post.timestamp = datetime.utcnow()

        db.session.add(post)
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('index'))
    else:
        # if we're just doing a get, grab the data from current_user
        # print('this should just show the post')
        form.body.data = post.body
    return render_template('post_edit.html', form=form)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
