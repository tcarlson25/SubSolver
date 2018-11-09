from flask import Flask, render_template, request, json
from static.utils.solver import NgramSolver, IntersectSolver, FrequencySolver

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/")
def main():
    return render_template('index.html')


@app.route("/decrypt", methods=['POST'])
def decrypt():
    ciphertextInput = request.form['ciphertextInput']
    methodOption = request.form['methodOption']
    solver = None
    if methodOption == "1":
        solver = NgramSolver(ciphertextInput, 1)
        key, plaintext = solver.solve()
        return json.dumps({'key_mapping': key, 'plaintext': plaintext})
    elif methodOption == "2":
        solver = NgramSolver(ciphertextInput, 2)
        key, plaintext = solver.solve()
        return json.dumps({'key_mapping': key, 'plaintext': plaintext})
    elif methodOption == "3":
        solver = NgramSolver(ciphertextInput, 3)
        key, plaintext = solver.solve()
        return json.dumps({'key_mapping': key, 'plaintext': plaintext})
    elif methodOption == "4":
        solver = NgramSolver(ciphertextInput, 4)
        key, plaintext = solver.solve()
        return json.dumps({'key_mapping': key, 'plaintext': plaintext})
    elif methodOption == "5":
        solver = IntersectSolver(ciphertextInput)
        mapping, plaintext = solver.solve()
        return json.dumps({'key_mapping': mapping, 'plaintext': plaintext})
    elif methodOption == "6":
        solver = FrequencySolver(ciphertextInput)
        mapping, plaintext = solver.solve()
        return json.dumps({'key_mapping': mapping, 'plaintext': plaintext})
    else:
        solver = None
        return json.dumps({'status':'Fail'})

if __name__ == "__main__":
    # app.run(host='0.0.0.0')
    app.run()
