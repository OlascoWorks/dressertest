from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from .models import Cloth, User, Log, Combination
from . import db
import base64
import random

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
@login_required
def home():
    uncommitted_cloths = Cloth.query.filter_by(user_id=current_user.id, isCommitted=False).all()
    uncommitted_cloths.reverse()

    return render_template('base.html', user=current_user, unc_cloths=uncommitted_cloths)

@views.route('/profile')
@login_required
def profile():
    no_pic = True
    if current_user.profile_pic != None:
        no_pic = False
    combos = Combination.query.all()
    combos.reverse()
    cloths = len(Cloth.query.filter_by(user_id=current_user.id).all())
    unc_cloths = len(Cloth.query.filter_by(user_id=current_user.id, isCommitted=False).all())
    comm_cloths = len(Cloth.query.filter_by(user_id=current_user.id, isCommitted=True).all())
    tops = len(Cloth.query.filter_by(user_id=current_user.id, type='top').all())
    bottoms = len(Cloth.query.filter_by(user_id=current_user.id, type='bottom').all())

    possible_combos = len(Cloth.query.filter_by(user_id=current_user.id, type='top', isCommitted=True).all())*len(Cloth.query.filter_by(user_id=current_user.id, type='bottom', isCommitted=True).all())
    available_combos = possible_combos - len(combos)
    blacklisted_combos = len(Combination.query.filter_by(user_id=current_user.id, isBlacklisted=True).all())
    used_combos = len(Combination.query.filter_by(user_id=current_user.id, isBlacklisted=False).all())

    return render_template('profile.html',
                           user=current_user, no_pic=no_pic, cloths=cloths, unc_cloths=unc_cloths, comm_cloths=comm_cloths, tops=tops, bottoms=bottoms, combos=combos, possible_combos=possible_combos, available_combos=available_combos, blacklisted_combos=blacklisted_combos, used_combos=used_combos)

@views.route('/new_cloth', methods=['GET', 'POST'])
@login_required
def new_cloth():
    if request.method == 'POST':
        # retrieve the cloth name and description from the form data
        name = request.form.get('name')
        description = request.form.get('description')
        image = request.files['image'].read()
        encoded_image = base64.b64encode(image).decode('utf-8')
        isCommit = request.form.get('commit')
        cloth_type = request.form.get('type')
        
        if Cloth.query.filter_by(name=name).first():
            flash('Name already exists, make it unique!', category='error')
        else:
            # create a new Cloth object and save it to the database
            if isCommit:
                new_cloth = Cloth(name=name, description=description, image=encoded_image, isCommitted=True, type=cloth_type, user_id=current_user.id)
            else:
                new_cloth = Cloth(name=name, description=description, image=encoded_image, isCommitted=False, type=cloth_type, user_id=current_user.id)
            db.session.add(new_cloth)
            db.session.commit()
            new_log = Log(name=name, event='cloth create', user_id=current_user.id)
            db.session.add(new_log)
            db.session.commit()

            clothExists = Cloth.query.filter_by(description=description).first()
            if clothExists and clothExists.name != name:

                flash('This cloth has the same description as another', category='warning')
            else:
                flash('Cloth created successfuuly', category='success')
            return redirect(url_for('views.home'))

    return render_template('new_cloth.html', user=current_user)


@views.route('/backend/cloth/do-something/<int:id>')
@login_required
def cloth_gateway(id):
    cloth = Cloth.query.filter_by(id=id, user_id=current_user.id).first()
    action = request.args.get('action')
    if action == 'commit':
        cloth.isCommitted = True
        db.session.commit()
        new_log = Log(name=cloth.name, event='update', user_id=current_user.id)
        db.session.add(new_log)
        db.session.commit()
        flash(f'{cloth.name} has been committed successfully', category='success')
        return redirect(url_for('views.home'))
    elif action == 'delete':
        db.session.delete(cloth)
        db.session.commit()
        new_log = Log(name=cloth.name, event='delete', user_id=current_user.id)
        db.session.add(new_log)
        db.session.commit()
        flash(f'{cloth.name} has been deleted successfully', category='success')
        return redirect(url_for('views.home'))
    
@views.route('/edit/cloth/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    cloth = Cloth.query.filter_by(id=id).first()
    if request.method == 'POST':
        cloth.name = request.form.get('name')
        cloth.description = request.form.get('description')
        isCommit = request.form.get('commit')
        if isCommit:
            cloth.isCommitted = True
        else:
            cloth.isCommitted = False
        cloth.type = request.form.get('type')

        db.session.commit()
        new_log = Log(name=cloth.name, event='update', user_id=current_user.id)
        db.session.add(new_log)
        db.session.commit()
        flash('New changes added', category='success')
        return redirect(url_for('views.home'))

    return render_template('edit.html', user=current_user, cloth=cloth)

@views.route('/log/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def log_gateway(id):
    action = request.args.get('action')
    if action == 'delete':
        log = Log.query.filter_by(user_id=current_user.id, id=id).first()
        db.session.delete(log)
        db.session.commit()
        return redirect(url_for('views.history'))
    elif action == 'delete_all':
        logs = Log.query.filter_by(user_id=current_user.id).all()
        for log in logs:
            db.session.delete(log)
        db.session.commit()
        return redirect(url_for('views.history'))

@views.route('/history')
@login_required
def history():
    logs = Log.query.filter_by(user_id=current_user.id).all()
    logs.reverse()

    return render_template('history.html', user=current_user, logs=logs)

@views.route('/backend/combo/do-something/<int:id>')
@login_required
def combo_gateway(id):
    combo = Combination.query.filter_by(id=id, user_id=current_user.id).first()
    action = request.args.get('action')
    if action == 'blacklist':
        combo.isBlacklisted = True
        db.session.commit()
        new_log = Log(event='combo update', user_id=current_user.id)
        db.session.add(new_log)
        db.session.commit()
        flash(f'combo has been blacklisted successfully', category='success')
        return redirect(url_for('views.profile'))
    elif action == 'unblacklist':
        combo.isBlacklisted = False
        db.session.commit()
        new_log = Log(event='combo update', user_id=current_user.id)
        db.session.add(new_log)
        db.session.commit()
        flash(f'combo has been un-blacklisted successfully', category='success')
        return redirect(url_for('views.profile'))
    elif action == 'delete':
        db.session.delete(combo)
        db.session.commit()
        new_log = Log(event='combo delete', user_id=current_user.id)
        db.session.add(new_log)
        db.session.commit()
        flash(f'combo has been deleted successfully', category='success')
        return redirect(url_for('views.profile'))
    
@views.route('/generate/template')
@login_required
def generate_template():

    return render_template('generate_template.html', user=current_user)

@views.route('/generate')
@login_required
def generate():
    tops = Cloth.query.filter_by(user_id=current_user.id, type='top', isCommitted=True).all()
    bottoms = Cloth.query.filter_by(user_id=current_user.id, type='bottom', isCommitted=True).all()
    possible_combos = len(tops)*len(bottoms)
    available_combos = possible_combos - len(Combination.query.all())
    count = 0
    for top in tops:
        print(top.name)

    if len(tops) < 1 or len(bottoms) < 1:
        flash('There are not enough cloths. Create more or commit existing', category='warning')
        return redirect(url_for('views.generate_template'))
    else:
        combo_list = []
        top = random.choice(tops)
        bottom = random.choice(bottoms)
        comboExists = Combination.query.filter_by(top=top.name, bottom=bottom.name, user_id=current_user.id).first()
        combo_list.append([top,bottom])
        if comboExists:
            for t in tops:
                for b in bottoms:
                    if [t, b] not in combo_list:
                        combo_list.append([t, b])

            while count < available_combos and len(combo_list) < available_combos:
                top = random.choice(tops)
                bottom = random.choice(bottoms)
                comboExists = Combination.query.filter_by(top=top.name, bottom=bottom.name, user_id=current_user.id).first()
                if comboExists:
                    combo_list.append([top, bottom])

                if [top, bottom] in combo_list:
                    count+= 1
                else:
                    count = 0
                    break

            if count == available_combos and comboExists:
                flash('There are no more possible combinations. Create more cloth or commit existing', category='warning')
                return redirect(url_for('views.generate_template'))

    return render_template('generate.html', user=current_user, top=top, bottom=bottom)

@views.route('/combo/gateway/<int:top_id>/<int:bottom_id>')
@login_required
def combo_create_gateway(top_id, bottom_id):
    top = Cloth.query.filter_by(id=top_id).first()
    bottom = Cloth.query.filter_by(id=bottom_id).first()
    action = request.args.get('action')
    if action == 'use':
        new_combo = Combination(top=top.name, bottom=bottom.name, isBlacklisted=False, user_id=current_user.id)
        db.session.add(new_combo)
        db.session.commit()
        new_log = Log(event='combo create', user_id=current_user.id)
        db.session.add(new_log)
        db.session.commit()
        flash('Combination generated', category='success')
        return redirect(url_for('views.home'))
    elif action == 'blacklist':
        new_combo = Combination(top=top.name, bottom=bottom.name, isBlacklisted=True, user_id=current_user.id)
        db.session.add(new_combo)
        db.session.commit()
        new_log = Log(event='combo create', user_id=current_user.id)
        db.session.add(new_log)
        db.session.commit()
        flash('This combination would not be suggested again', category='info')
        return redirect(url_for('views.generate'))

@views.route('/about')
def about():
    return render_template('about.html', user=current_user)