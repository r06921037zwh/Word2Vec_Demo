from flask import Flask, request, render_template
from gensim.models import word2vec
import os

app = Flask(__name__)
print("Loading Model ... ")
model = word2vec.Word2Vec.load(os.path.join('model', 'news_and_sg2.model'))

@app.route('/')
def index():
    keyword = request.args.get('keyword')
    result = ''
    if keyword != None:
        result = model.wv.most_similar(positive=[str(keyword)])
        result = [list(it) for it in result]
    else:
        return render_template('show.html', response=result)
    if result == '':
        result = str(keyword) + " NOT IN VOCABULARY"
    return render_template('show.html', response=result)

@app.route('/Comp')
def comp():
    keyword1 = request.args.get('keyword1')
    keyword2 = request.args.get('keyword2')
    result = ''
    ans1 = ''
    ans2 = ''
    if keyword1 == None and keyword2 == None:
        pass
    else:
        ans1 = model.wv.most_similar(positive=[str(keyword1)])[0]
        ans2 = model.wv.most_similar(positive=[str(keyword2)])[0]
        result = model.wv.similarity(str(keyword1), str(keyword2))
    return render_template('comp.html', response=result,
                            keyword1=keyword1, keyword2=keyword2,
                            ans1=ans1, ans2=ans2)
if __name__ == '__main__':
    app.run(debug=True)
