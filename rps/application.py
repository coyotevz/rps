# -*- coding: utf-8 -*-

import locale
locale.setlocale(locale.LC_ALL, '')

from flask import Flask, request, url_for, render_template, redirect

from flask.ext.sqlalchemy import SQLAlchemy

from wtforms import StringField, HiddenField, SelectMultipleField
from wtforms import widgets
from wtforms.validators import DataRequired
from flask.ext.wtf import Form
from flask.ext.wtf.html5 import EmailField

from rps.cupon import Cupon


## Create app & configure

app = Flask(__name__)
try:
    app.config.from_object('localconfig.LocalConfig')
except ImportError:
    app.config.from_object('rps.config.DevelopmentConfig')


## Models
db = SQLAlchemy(app)

class Customer(db.Model):
    __tablename__ = 'customer'

    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.Integer, nullable=False, unique=True)

    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    birthday = db.Column(db.String)
    twitter = db.Column(db.String)

    especialidad = db.Column(db.String)

    matricula = db.Column(db.String)


## Forms

esp = [
    ('inst_dom', 'Instalaciones Domiciliarias'),
    ('inst_ind', 'Instalaciones Industirales'),
    ('gas_nat', 'Gas Natural'),
    ('desag', 'Desagüe'),
    ('ince', 'Incendio'),
    ('agua', 'Agua Fría y Caliente'),
    ('calef', 'Calefacción'),
    ('grif', 'Loza y Grifería'),
    ('reig', 'Riego'),
    ('pil', 'Piscinas'),
    ('otras', 'Otras'),
]

class Step1Form(Form):
    dni = StringField('DNI / LE / LC', validators=[DataRequired()])


class Step2Form(Form):
    dni = HiddenField()

    firstname = StringField('Nombre', validators=[DataRequired()])
    lastname = StringField('Apellido', validators=[DataRequired()])
    email = EmailField('E-mail')
    phone = StringField('Teléfono')
    birthday = StringField('Fecha Nac.')
    twitter = StringField('Twitter')

class Step3Form(Form):
    dni = HiddenField()
    firstname = HiddenField()
    lastname = HiddenField()
    email = HiddenField()
    phone = HiddenField()
    birthay = HiddenField()
    twitter = HiddenField()

    especialidad = SelectMultipleField(
            'Especialidades',
            choices=esp,
            option_widget=widgets.CheckboxInput(),
            widget=widgets.ListWidget(prefix_label=False),
    )

    matricula = StringField('Matricula')

class VerifyForm(Form):
    dni = HiddenField()
    firstname = HiddenField()
    lastname = HiddenField()
    email = HiddenField()
    phone = HiddenField()
    birthay = HiddenField()
    twitter = HiddenField()
    especialidad = HiddenField()
    matricula = HiddenField()

## Views

@app.route('/')
@app.route('/step1', methods=['GET', 'POST'])
def step1():
    form = Step1Form()
    if form.validate_on_submit():
        dni = form.dni.data
        c = Customer.query.filter(Customer.dni==form.dni.data).first()
        if c is None:
            return redirect('step2', code=307)
        else:
            return redirect(url_for('show_customer', id=c.id))
    return render_template('step1.html', form=form)

@app.route('/step2', methods=['GET', 'POST'])
def step2():
    form = Step2Form()
    if form.validate_on_submit():
        return redirect('step3', code=307)
    return render_template('step2.html', form=form)

@app.route('/step3', methods=['POST'])
def step3():
    form = Step3Form()
    return render_template('step3.html', form=form)

@app.route('/verify', methods=['POST'])
def verify():
    form = Step3Form()
    form.dni.data = form.dni.data.replace('.', '')
    form.firstname.data = form.firstname.data.capitalize()
    form.lastname.data = form.lastname.data.capitalize()
    return render_template('verify.html', form=form)

@app.route('/finish', methods=['POST'])
def finish():
    form = Step3Form()
    customer = Customer()
    form.especialidad.data = ', '.join(form.especialidad.data)
    form.populate_obj(customer)
    db.session.add(customer)
    db.session.commit()
    cupon = Cupon(customer)
    cupon.print(run_dry=True)
    return render_template('finish.html', customer=customer)

@app.route('/show/<id>')
def show_customer(id):
    customer = Customer.query.get_or_404(id)
    return render_template('show_customer.html', customer=customer)

## Helpers

@app.context_processor
def template_helpers():

    def static(filename):
        return url_for('static', filename=filename)

    return dict(static=static)
