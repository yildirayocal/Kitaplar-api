from flask import Flask, request
from flask_restful import Api, Resource
import pandas as pd

app = Flask(__name__)
api = Api(app)

class Books(Resource):
    def get(self):
        data = pd.read_csv('kitap.csv')

        result = data[['KITAP', 'YAYIN EVI', 'SAYFA', 'BASIM YILI', 'YAZAR']].to_dict('records')
        return {'data' : result}, 200

    def post(self):
        kitap = request.args['KITAP']
        yayin_evi  = request.args['YAYIN EVI']
        sayfa = request.args['SAYFA']
        basim_yili = request.args['BASIM YILI']
        yazar = request.args['YAZAR']

        req_data = pd.DataFrame({
            'KITAP': [kitap],
            'YAYIN EVI': [yayin_evi],
            'SAYFA': [sayfa],
            'BASIM YILI': [basim_yili],
            'YAZAR': [yazar]
        })

        data = pd.read_csv('kitap.csv')
        data = data.append(req_data, ignore_index=True)
        data.to_csv('kitap.csv', index=False)

        return {'message' : 'Record successfully added.'}, 200

class BookName(Resource):
    def get(self, name):
        data = pd.read_csv('kitap.csv')
        data = data.to_dict('records')

        for entry in data:
            if entry['KITAP'] == name:
                return {'data' : entry}, 200

        return {'message' : f"No entry found with this book name: {name}."}, 404

class BookCities(Resource):
    def get(self):
        data = pd.read_csv('kitap.csv', usecols=['YAYIN EVI'])
        data = data.to_dict('records')
        return {'data' : data}, 200

api.add_resource(Books, '/books')
api.add_resource(BookCities, '/bookcities')
api.add_resource(BookName, '/books/<string:name>')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6767)
