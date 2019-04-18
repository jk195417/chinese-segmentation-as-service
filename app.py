from flask import Flask, request, jsonify
from snownlp import SnowNLP
import jieba
import pkuseg

app = Flask(__name__)


@app.route('/')
def root():
    return 'Chinese segmentation as service.'


@app.route('/segmentations', methods=['POST'])
def segmentations():
    text = request.json.get('text', False)
    if not text:
        return 'require text'
    global pku_seg
    if isinstance(text, list):
        result = {
            'jieba': [],
            'snownlp': [],
            'pkuseg': []
        }
        for sentence in text:
            result['jieba'].append(jieba.lcut(sentence))
            result['snownlp'].append(SnowNLP(sentence).words)
            result['pkuseg'].append(pku_seg.cut(sentence))
    else:
        result = {
            'jieba': jieba.lcut(text),
            'snownlp': SnowNLP(text).words,
            'pkuseg': pku_seg.cut(text)
        }
    return jsonify(result)


if __name__ == '__main__':
    # https://github.com/fxsjy/jieba/raw/master/extra_dict/dict.txt.big
    jieba.set_dictionary('dictionaries/big-dict.txt')
    jieba.initialize()
    pku_seg = pkuseg.pkuseg()
    app.run('127.0.0.1', 3001)
