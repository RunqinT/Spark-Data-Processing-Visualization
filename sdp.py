@app.route("/")
def showChart():
  global words,counts
  counts = []
  words = []
  return render_template('chart.html', counts=counts, words=words) 
