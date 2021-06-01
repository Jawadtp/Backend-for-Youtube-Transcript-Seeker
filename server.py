import youtube
from flask import Flask, render_template, request
app = Flask(__name__)

print('Server is up and running!')

@app.route('/')
def student():
   return render_template('ui.html')


@app.route('/',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      print(result['url'])
      print(result['word'])
      temp = youtube.main(result['url'], result['word'])
      return render_template("ui.html", temp=temp)


if __name__ == 'main':
   app.run(debug = True)