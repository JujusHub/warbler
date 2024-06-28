from flask import Flask, render_template, redirect, url_for, session, flash
from flask_login import login_required, current_user
from forms import EditProfileForm
from models import db, User, Message, Likes

app = Flask(__name__)

@app.route('/warbles/<int:message_id>/like', methods=['POST'])
@login_required
def like_warble(message_id):
    message = Message.query.get_or_404(message_id)
    if message.user_id == current_user.id:
        flash("You cannot like your own warble.", 'danger')
        return redirect(url_for('homepage'))

    like = Likes(user_id=current_user.id, message_id=message_id)
    db.session.add(like)
    db.session.commit()
    flash('Warble liked!', 'success')
    return redirect(url_for('homepage'))

@app.route('/warbles/<int:message_id>/unlike', methods=['POST'])
@login_required
def unlike_warble(message_id):
    like = Likes.query.filter_by(user_id=current_user.id, message_id=message_id).first()
    if like:
        db.session.delete(like)
        db.session.commit()
        flash('Warble unliked!', 'success')
    return redirect(url_for('homepage'))

@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user_id = session['user_id']
    user = User.query.get_or_404(user_id)
    form = EditProfileForm(obj=user)

    if form.validate_on_submit():
        if bcrypt.check_password_hash(user.password, form.password.data):
            user.username = form.username.data
            user.email = form.email.data
            user.image_url = form.image_url.data
            user.header_image_url = form.header_image_url.data
            user.bio = form.bio.data
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('show_user', user_id=user.id))
        else:
            flash('Incorrect password.', 'danger')
            return redirect(url_for('homepage'))

    return render_template('users/edit.html', form=form, user=user)

@app.route('/users/<int:user_id>/likes')
@login_required
def liked_warbles(user_id):
    user = User.query.get_or_404(user_id)
    liked_messages = Message.query.join(Likes, (Likes.message_id == Message.id)).filter(Likes.user_id == user.id).all()
    return render_template('users/liked_warbles.html', user=user, messages=liked_messages)
