from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
import requests
import pandas as pd
import itertools
df=pd.read_csv('indian_food.csv')
app= Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///menu.db'
db=SQLAlchemy(app)
app.app_context().push()

class states(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    state=db.Column(db.String(200),nullable=False)
    recipe=db.Column(db.String(200),nullable=False)
    ingredients=db.Column(db.Text,nullable=False)

    def __repr__(self):
        return '<Item %r>' %self.id

@app.route('/')
def index():
    #for i in range(len(df)):
    #    item=states(state=df.iloc[i][7],recipe=df.iloc[i][0],ingredients=df.iloc[i][1])
    #    db.session.add(item)
    #db.session.commit()
    items=states.query.all()
    state_names=db.session.query(states.state).distinct()
    return render_template('index.html',state_names=state_names)


@app.route('/menu',methods=['POST','GET'])
def menu():
    if request.method=='POST':
        get_state =request.form['states']
        food=db.session.query(states.recipe).filter(states.state == get_state)
        common_food=db.session.query(states.recipe).filter(states.state == '-1')

    return render_template('menu.html',food =food,common_food=common_food)

@app.route('/menu/userprofile',methods=['POST','GET'])
def nutrients():
    if request.method=='POST':
        userfood =request.form.getlist('food')
        ing=[]
        ingre=[]
        nutri=[]
        for u in userfood:
            ing.append(db.session.query(states.ingredients).filter(states.recipe == u))

        for i in ing:
            for j in i:
                ingre.append(j.ingredients)

        for (x,y) in zip(userfood,ingre):
            url='https://api.edamam.com/api/food-database/v2/parser?app_id=4266f351&app_key=79aa66139c2a9634e000f5435120f3e6&ingr='+x
            response = requests.get(url)
            n=response.json()
            if n['hints']==[]:
                url1='https://api.edamam.com/api/food-database/v2/parser?app_id=4266f351&app_key=79aa66139c2a9634e000f5435120f3e6&ingr='+y
                response1=requests.get(url1)
                n=response1.json()
            nutri.append(n['hints'][0]['food']['nutrients'])

        dict={
            'item':userfood,
            'ingredients':ingre,
            'nutrients':nutri
        }
        df=pd.DataFrame(dict)
        n=len(df)

    return render_template('userprofile.html',userfood=userfood,ingre=ingre,nutri=nutri,df=df,n=n)



if __name__ == '__main__':
    app.run(debug=True) 

