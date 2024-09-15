from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Página principal que enlaza a mini páginas

@app.route('/project1')
def project1():
    return render_template('project1.html')  # HTML exportado desde un notebook

@app.route('/project2')
def project2():
    return render_template('project2.html')  # Otra mini página

if __name__ == '__main__':
    app.run(debug=True)