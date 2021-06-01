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
      temp = youtube.main("https://www.youtube.com/watch?v=WPjsDVS_trI", "hi")
      return render_template("ui.html",result = result, temp=temp)


if __name__ == 'main':
   app.run(debug = True)