from flask import Flask, request, jsonify
from snownlp import SnowNLP
import jieba
import pkuseg

app = Flask(__name__)
# https://github.com/fxsjy/jieba/raw/master/extra_dict/dict.txt.big
jieba.set_dictionary('dictionaries/big-dict.txt')
jieba.initialize()
pku_seg = pkuseg.pkuseg()


@app.route('/')
def root():
    return 'Chinese segmentation as service.'


@app.route('/segmentations', methods=['POST'])
def segmentations():
    text = request.json.get('text', False)
    lib = request.json.get('lib', 'jieba')
    result = {'lib': lib}
    if not text:
        return 'require text'
    if isinstance(text, list):
        result['result'] = []
        for sentence in text:
            result['result'].append(segment(sentence, lib))
    else:
        result['result'] = segment(sentence, lib)
    return jsonify(result)


def segment(sentence, lib):
    if lib == 'jieba':
        return jieba.lcut(sentence)
    elif lib == 'snownlp':
        return SnowNLP(sentence).words
    elif lib == 'pkuseg':
        return pku_seg.cut(sentence)


if __name__ == '__main__':
    app.run('127.0.0.1', 3001)
