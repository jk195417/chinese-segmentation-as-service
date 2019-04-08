from flask import Flask, request, jsonify
from snownlp import SnowNLP
import jieba
import pkuseg

app = Flask(__name__)

@app.route('/')
def root():
    return 'Chinese segmentation as service.'

@app.route('/seg', methods=['POST'])
def seg():
    text = request.json.get('text', False)
    if not text:
        return 'require text'

    global pku_seg
    result = {
        'jieba': ' '.join(jieba.cut(text)),
        'snownlp': ' '.join(SnowNLP(text).words),
        'pkuseg': ' '.join(pku_seg.cut(text))
    }
    return jsonify(result)

if __name__ == '__main__':
    jieba.set_dictionary('dictionaries/big-dict.txt') # https://github.com/fxsjy/jieba/raw/master/extra_dict/dict.txt.big
    jieba.initialize()
    pku_seg = pkuseg.pkuseg()
    app.run('127.0.0.1', 3001)
