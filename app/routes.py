from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.utils import secure_filename
import pandas as pd
import os

from .models import User
from .forms import UserForm, UploadForm
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    users = User.query.all()
    return render_template('index.html', users=users)

@main.route('/add_user', methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data)
        db.session.add(new_user)
        db.session.commit()
        flash('User added successfully!', 'success')
        return redirect(url_for('main.home'))
    return render_template('add_user.html', form=form)

@main.route('/map')
def map():
    return render_template('map.html')

@main.route('/upload', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join('uploads', filename)
            file.save(filepath)
            recommendations = process_excel(filepath)
            return render_template('recommendations.html', recommendations=recommendations)
    return render_template('upload.html', form=form)

def process_excel(filepath):
    df = pd.read_excel(filepath)

    recommendations = []
    for index, row in df.iterrows():
        stock_actual = row['STOCK ACTUAL']
        pendiente_entrega = row['PENDIENTE DE ENTREGA']
        demanda_promedio = row['DEMANDA PROMEDIO']
        desviacion_estandar = row['DESVIACION ESTANDAR']

        # Aplicar fórmula (ejemplo básico)
        reorder_point = demanda_promedio + (2 * desviacion_estandar)
        total_stock = stock_actual + pendiente_entrega
        if total_stock < reorder_point:
            recommendation = 'Pedir'
        else:
            recommendation = 'No Pedir'

        recommendations.append({
            'CODIGO': row['CODIGO'],
            'NOMBRE PRODUCTO': row['NOMBRE PRODUCTO'],
            'RECOMMENDATION': recommendation
        })

    return recommendations
