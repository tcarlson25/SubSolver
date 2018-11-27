from flask import Flask, render_template, request, json
from static.utils.solver import NgramSolver, IntersectSolver, FrequencySolver, ManualSolver

app = Flask(__name__)
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# app.config['TEMPLATES_AUTO_RELOAD'] = True
# app.config['SECRET_KEY'] = 'secret_key'

monogramSolver = NgramSolver(1)
bigramSolver = NgramSolver(2)
trigramSolver = NgramSolver(3)
quadgramSolver = NgramSolver(4)
intersectSolver = IntersectSolver()
frequencySolver = FrequencySolver()
manualSolver = ManualSolver()


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/decrypt", methods=['POST'])
def decrypt():
    ciphertextInput = request.form['ciphertextInput']
    methodOption = request.form['methodOption']
    keyInput = request.form['keyInput']
    solver = None
    if methodOption == "1":
        key, plaintext = monogramSolver.solve(ciphertextInput)
        return json.dumps({'key_mapping': key, 'plaintext': plaintext})
    elif methodOption == "2":
        key, plaintext = bigramSolver.solve(ciphertextInput)
        return json.dumps({'key_mapping': key, 'plaintext': plaintext})
    elif methodOption == "3":
        key, plaintext = trigramSolver.solve(ciphertextInput)
        return json.dumps({'key_mapping': key, 'plaintext': plaintext})
    elif methodOption == "4":
        key, plaintext = quadgramSolver.solve(ciphertextInput)
        return json.dumps({'key_mapping': key, 'plaintext': plaintext})
    elif methodOption == "5":
        mapping, plaintext,divData = intersectSolver.solve(ciphertextInput)
        return json.dumps({'key_mapping': mapping, 'plaintext': plaintext, 'tableData' : divData})
    elif methodOption == "6":
        key, plaintext, divData = frequencySolver.solve(ciphertextInput)
        return json.dumps({'key_mapping': key, 'plaintext': plaintext, 'barData': divData})
    elif methodOption == "7":
        plaintext = manualSolver.decrypt(keyInput, ciphertextInput)
        return json.dumps({'plaintext': plaintext})
    elif methodOption == "8":
        ciphertext = manualSolver.encrypt(keyInput, ciphertextInput)
        return json.dumps({'ciphertext': ciphertext})
    else:
        return json.dumps({'status':'Fail'})

if __name__ == "__main__":
    app.run(host='0.0.0.0')
    # app.run(debug=True);
