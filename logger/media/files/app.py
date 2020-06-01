from flask import Flask, session, render_template, redirect, url_for, request, flash
import requests
import gunicorn
from werkzeug.exceptions import BadRequest
import json
app = Flask(__name__)
app.secret_key = 'Gooapi'
#for d in pass_times:
 #   print(d['food']['label'])

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        print(request.form)
        search = request.form['search']


    else:
        search = 'chocolate'
    url = "https://edamam-food-and-grocery-database.p.rapidapi.com/parser"

    querystring = {"ingr":search}

    headers = {
        'x-rapidapi-host': "edamam-food-and-grocery-database.p.rapidapi.com",
        'x-rapidapi-key': "1689f7916emsh75e78b03fae9b2ap10fba7jsnc601f750c77b"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    #res = json.loads(response.text)
    res = response.json()['hints']
    pass_times = response.json()['hints']
    
    return render_template('home.html', res=res, search=search)

@app.route('/restaurants',methods=['GET','POST'])
def restaurant():
    location = 'tokyo'
    if request.method == 'POST':
        try:
            if request.form['click'] == 'clicked':
                location = request.form['location']
            else:
                location = 'venice'
        except BadRequest:
            flash("There are some errors being fixed in the meanwhile do not click the orange button")
        
    else:
        location = 'ghana'
    zomato_user_key = 'c0afcdd621a1dbdc89c9ce02bd7a3d17'
    
    geo_url = 'https://developers.zomato.com/api/v2.1/locations?query={}'.format(location)
    headers = {'Accept': 'application/json', 'user-key': zomato_user_key}
    rz = requests.request('GET',geo_url, headers=headers)
    res = rz.json()
    
    #base_url = "https://developers.zomato.com/api/v2.1/"
    base_url = 'https://developers.zomato.com/api/v2.1/locations?query={}'.format(location)
    headers = {'Accept': 'application/json', 'user-key': zomato_user_key}
    rz = requests.request('GET',base_url, headers=headers)
    res = rz.json()

    for i in res['location_suggestions']:
        print(i['title'])
        entity_type = i['entity_type']
        entity_id = i['entity_id']
        print('entity_id:{}  entity_type:{}'.format(entity_id, entity_type))
    
    url_location_det = 'https://developers.zomato.com/api/v2.1/location_details?entity_id={}&entity_type={}'.format(entity_id, entity_type)
    details = requests.request('GET',url_location_det, headers=headers)
    det = details.json()
    
    '''for i in det['top_cuisines']:
        top_cuisines = i
      for i in det['best_rated_restaurant']:
        name = i['restaurant']['name']
        image = i['restaurant']['thumb']
        cuisines = i['restaurant']['']'''
    return render_template('restaurants.html', cuisines=det['top_cuisines'], rest = det['best_rated_restaurant'], count=True)

@app.route('/collections',methods=['GET','POST'])
def collections():
    if request.method == 'POST':
        try:
            if request.form['click'] == 'clicked':
                location = request.form['location']
            else:
                location = 'venice'
        except BadRequest:
            flash("There are some errors being fixed in the meanwhile do not click the orange button")
        
    else:
        location = 'ghana'
    zomato_user_key = 'c0afcdd621a1dbdc89c9ce02bd7a3d17'
    geo_url = 'https://developers.zomato.com/api/v2.1/locations?query={}'.format(location)
    headers = {'Accept': 'application/json', 'user-key': zomato_user_key}
    rz = requests.request('GET',geo_url, headers=headers)
    res = rz.json()
    
    
    #base_url = "https://developers.zomato.com/api/v2.1/"
    base_url = 'https://developers.zomato.com/api/v2.1/locations?query={}'.format(location)
    rz = requests.request('GET',base_url, headers=headers)
    res = rz.json()
    #for i,e in res['location'].items():
     #   print('{} : {}'.format(i,e))
    
    for i in res['location_suggestions']:
        entity_type = i['entity_type']
        entity_id = i['entity_id']
    
    url_location_det = 'https://developers.zomato.com/api/v2.1/location_details?entity_id={}&entity_type={}'.format(entity_id, entity_type)
    details = requests.request('GET',url_location_det, headers=headers)
    det = details.json()
    col = 'https://developers.zomato.com/api/v2.1/collections?city_id={}'.format(entity_id)
    collect = requests.request('GET',col, headers=headers)
    collection = collect.json()
    for i in collection['collections']:
        print(i['collection']['collection_id'])
    
    collection = collection['collections']
    return render_template('collections.html',collection = collection)

@app.route('/test')
def test():
    return render_template('test.html')


if __name__ == '__main__':
    app.run(debug=True)