from flask import Flask, render_template, request, json

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/")
def main():
    return render_template('index.html')


@app.route("/decrypt", methods=['POST'])
def decrypt():
    ciphertextInput = request.form['ciphertextInput']
    return json.dumps({'status':'OK', 'ciphertext-input': ciphertextInput})


if __name__ == "__main__":
    app.run()
