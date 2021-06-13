import yoogle

from flask import Flask, render_template, request
app = Flask(__name__)

print('Server is up and running!')

@app.route('/',methods = ['POST', 'GET'])
def result():
   if request.method == 'GET':
      return render_template('ui.html')
   if request.method == 'POST':
      result = request.form
      temp={}
      temp = yoogle.main(result['url'], result['word'])
      return render_template("ui.html", temp=temp, url=result['url'], word=result['word'])

if __name__=="__main__":
   app.run(debug = False)