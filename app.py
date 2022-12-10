import requests
from flask import Flask, request

import os
import platform
import sys
import psutil


app = Flask(__name__)

def controller_poke(headers):
    
    _url = 'http://127.0.0.1:9002/api/v1/auth'
    _headers = {'uuid': headers['uuid']}
    _token = request.cookies.get('jwt')
    # request
    _reponse = requests.get(url = _url, headers=_headers, cookies={'jwt': _token})

    # transform to json
    _reponse = _reponse.json()

    #if (not authenticated) refuse access
    if not _reponse['authenticated']:
        return _reponse

    try:
        # get the api endpoint (pokeapi) from headers
        endpoint_poke_api = headers['endpoint_poke_api']
        # get the ability name from headers we are looking for
        head_ability_name = headers['ability_name']
        # get the number of ability we are looking for
        ability_range = int(headers['ability_range'])
        # request
        response = requests.get(endpoint_poke_api)
        # transform to json
        response = response.json()

        print(response)
        # get the ability from response in index ability_range
        abilities = response['abilities'][ability_range]
        # "skill" obtained from headers and we are looking for
        ability_name = abilities['ability']['name']
        # print in console abilities, ability name and range
        print(abilities, ability_name, ability_range)

    # in case of error
    except Exception as e:
        return  {'error': e.args[0]},400
    else:
        if head_ability_name in ability_name:
            return {f'head_ability_name: {head_ability_name} ': True},200
        
        return {f'head_ability_name: {head_ability_name} ': False},200
    return {'controller_poke':True}

# first endpoint: poke
@app.route('/api/v1/poke')
def poke():
    response = controller_poke(request.headers)
    return response



# second endpoint: status
@app.route('/api/v1/status')
def memory():
    ram = psutil.virtual_memory().total   # total physical memory in Bytes
    response = {'memory': f' {ram} ram', 'system':platform.system() + '-' + sys.platform}
    return response

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=9000, debug=True)


