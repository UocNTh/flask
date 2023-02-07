
from math import gcd
from flask import Flask , request , jsonify , make_response

app = Flask(__name__)



@app.route('/ucln', methods = ['POST']) 
def UCLN(): 
    data = request.get_json() 
    s1 = data['a'] 
    s2 = data['b']
    try : 
        s1 = int(s1) 
        s2 = int(s2) 
    except: 
        return jsonify({'error': 'ValueError'}), 400

    ucln = gcd(s1,s2)

    return jsonify({'a': s1, 'b' : s2 , 'ucln': ucln} )



@app.route('/bcnn', methods = ['POST']) 
def BCNN(): 
    data = request.get_json() 
    s1 = data['a'] 
    s2 = data['b']
    try : 
        s1 = int(s1) 
        s2 = int(s2) 
    except: 
        return jsonify({'error': 'ValueError'}), 400

    ucln = gcd(s1,s2) 
    bcnn = int(s1*s2/ucln) 

    return jsonify({'a': s1, 'b' : s2 , 'bcnn': bcnn} )
        

@app.errorhandler(404)
def handle_404_error(_error): 
    return make_response(jsonify({'error': 'Not Found'}), 404)


@app.errorhandler(400)
def handle_400_error(_error): 
    return make_response(jsonify({'error': 'Bad Request'}), 400)

@app.errorhandler(405)
def handle_405_error(_error): 
    return make_response(jsonify({'error': 'Method Not Allowed'}), 405)

if __name__ == "__main__": 
    app.run(debug=True)