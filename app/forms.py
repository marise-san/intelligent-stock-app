from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, DateField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from app.models.product import CategoryEnum

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class RegistrationForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    password2 = PasswordField(
        'Repita a Senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')

class AddProductForm(FlaskForm):
    barcode = StringField('Código de Barras', validators=[DataRequired()])
    name = StringField('Nome do Produto', validators=[DataRequired()])
    description = StringField('Descrição')
    category = SelectField('Categoria', choices=[(category.name, category.value) for category in CategoryEnum], validators=[DataRequired()])
    supplier = StringField('Fornecedor')
    cost_price = FloatField('Preço de Custo', validators=[DataRequired()])
    sale_price = FloatField('Preço de Venda', validators=[DataRequired()])
    unit_of_measure = StringField('Unidade de Medida', validators=[DataRequired()])
    minimum_stock = IntegerField('Quantidade Mínima em Estoque', validators=[DataRequired()])
    expiration_date = DateField('Data de Validade', format='%Y-%m-%d')
    quantity = IntegerField('Quantidade', validators=[DataRequired()])
    submit = SubmitField('Cadastrar')

class EditStockForm(FlaskForm):
    quantity = IntegerField('Nova Quantidade', validators=[DataRequired()])
    submit = SubmitField('Atualizar Estoque')

class EditProductForm(FlaskForm):
    name = StringField('Nome do Produto', validators=[DataRequired()])
    description = StringField('Descrição')
    category = SelectField('Categoria', choices=[(category.name, category.value) for category in CategoryEnum], validators=[DataRequired()])
    supplier = StringField('Fornecedor')
    cost_price = FloatField('Preço de Custo', validators=[DataRequired()])
    sale_price = FloatField('Preço de Venda', validators=[DataRequired()])
    minimum_stock = IntegerField('Quantidade Mínima em Estoque', validators=[DataRequired()])
    expiration_date = DateField('Data de Validade', format='%Y-%m-%d')
    submit = SubmitField('Salvar Alterações')
