from flask import Flask, request, after_this_request
from flask_api import status
import datetime
import jwt  #pip install pyjwt

app = Flask(__name__)

#define the route
@app.route('/api/v1/login')
def login():
    # build the token
    payload = {
        #id is a data from headers
        'id': request.headers['uuid'] ,
        #time expiring 10 minutes
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10),
        #time begins
        'iat': datetime.datetime.utcnow(),
    }
    # secret string secreto, this link generate a secret string:
    # https://www.lastpass.com/es/features/password-generator
    token = jwt.encode(payload, 'ADDcUvgQ4t6f#7F%cGvQ08pg7FcHVW&$ti6!', algorithm='HS256').decode('utf-8')
    
    # set the jwt as a session cookie
    @after_this_request
    def add_cookie(response):
        response.set_cookie('jwt', token)
        return response
    # return the token in a json
    response = {'jwt':token}
    return response

# another route, to decode the token and validate the authorization
@app.route('/api/v1/auth')
def auth():
    try:
        # get the token set in the cookie
        token = request.cookies.get('jwt')
        # using the same secret string
        payload = jwt.decode(token, 'ADDcUvgQ4t6f#7F%cGvQ08pg7FcHVW&$ti6!', algorithm='HS256')

        # compare id from token and uuid
        if payload['id'] != request.headers['uuid']:
            # if not equal then refuse the access and return unauthorized
            return {'authenticated': False}, status.HTTP_401_UNAUTHORIZED

    # if time expired then too refuse the access and return unauthorized
    except jwt.ExpiredSignatureError:
        return {'authenticated': False}, status.HTTP_401_UNAUTHORIZED
    # if id and time expired is ok, authorize the access
    return {'authenticated': True}, status.HTTP_200_OK

# host is localhost and port 9002 
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=9002, debug=True)