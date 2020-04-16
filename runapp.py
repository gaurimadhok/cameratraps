import argparse
import sys
import bottle
import csv
import json

#--------some stuff needed to get AJAX to work with bottle?--------#
def enable_cors():
    '''
    From https://gist.github.com/richard-flosi/3789163
    This globally enables Cross-Origin Resource Sharing (CORS) headers for every response from this server.
    '''
    bottle.response.headers['Access-Control-Allow-Origin'] = '*'
    bottle.response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    bottle.response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run a web user interface for labeling camera trap images for classification.')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Web server host to bind to.')## default='localhost', help='Web server host to bind to.')
    parser.add_argument('--port', type=int, default=8081, help='Web server port port to listen on.')
    args = parser.parse_args(sys.argv[1:])


    # -------------------------------------------------------------------------------- #
    # CREATE AND SET UP A BOTTLE APPLICATION FOR THE WEB UI
    # -------------------------------------------------------------------------------- #
    
    webapp = bottle.Bottle()
    webapp.add_hook("after_request", enable_cors)
    webapp_server_kwargs = {
        "server": "tornado",
        "host": args.host,
        "port": args.port
    }

    @webapp.route('/')
    def index():
        return bottle.static_file("index.html", root='static/html')

    ## dynamic routes
    @webapp.route('/getCSV', method='POST')
    def getCSV():
        data = bottle.request.json
        with open('location_data_lat_long.csv') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            count = 0
            data['locations'] = []
            for row in readCSV:
                data['locations'].append([row[0], row[1], row[2]]) 
                print(row[0], row[1], row[2])
        bottle.response.content_type = 'application/json'
        bottle.response.status = 200
        return data

    webapp.run(**webapp_server_kwargs)