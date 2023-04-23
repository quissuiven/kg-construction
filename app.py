from flask import Flask, Response, request, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from QueryConversion_v2 import *

app = Flask(__name__)
 
class BasicForm(FlaskForm):
    text_input = StringField("Input your query:",validators=[DataRequired()],render_kw={'style': 'width: 60ch'})
    submit = SubmitField("Submit")

@app.route("/",methods=['GET','POST'])           
def signup():
    form = BasicForm(meta={'csrf': False})
    return render_template("signup.html",form = form)

@app.route("/success",methods=['GET','POST'])           
def success():
    form = BasicForm(meta={'csrf': False})
    if request.method=="POST":
        text_input = form.text_input.data
        model  = QueryConversionModel()
        query = model.get_cypherquery(text_input) 
        return render_template("knowledge_graph.html", query=query)

if __name__ == '__main__':
    app.run()