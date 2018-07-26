# Copyright 2017 Mario Graff Guerrero

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
TWEETS = os.path.join(os.path.dirname(__file__), 'tweets.json')


def test_corpus():
    from EvoMSA.model import Corpus
    from b4msa.utils import tweet_iterator
    c = Corpus([x['text'] for x in tweet_iterator(TWEETS)])
    a = c['hola hola mundo']
    assert len(a) == 3
    assert a[0] == a[1]


def test_bernulli():
    import numpy as np
    from EvoMSA.model import Corpus, Bernulli
    from b4msa.utils import tweet_iterator
    from sklearn.preprocessing import LabelEncoder
    c = Corpus([x['text'] for x in tweet_iterator(TWEETS)])
    X = c.tonp([c[x['text']] for x in tweet_iterator(TWEETS)])
    y = [x['klass'] for x in tweet_iterator(TWEETS)]
    le = LabelEncoder().fit(y)
    y = le.transform(y)
    b = Bernulli()
    b.fit(X, y)
    pr = b.decision_function(X)
    assert pr.shape[0] == 1000 and pr.shape[1] == 4
    assert np.all((pr <= 1) & (pr >= -1))


def test_multinomial():
    import numpy as np
    from EvoMSA.model import Corpus, Multinomial
    from b4msa.utils import tweet_iterator
    from sklearn.preprocessing import LabelEncoder
    c = Corpus([x['text'] for x in tweet_iterator(TWEETS)])
    X = c.tonp([c[x['text']] for x in tweet_iterator(TWEETS)])
    y = [x['klass'] for x in tweet_iterator(TWEETS)]
    le = LabelEncoder().fit(y)
    y = le.transform(y)
    b = Multinomial()
    b.fit(X, y)
    pr = b.decision_function(X)
    print(pr.shape[0], pr, b.num_terms)
    assert pr.shape[0] == 1000 and pr.shape[1] == 4
    assert np.all((pr <= 1) & (pr >= -1))


def test_EmoSpace():
    from EvoMSA.model import EmoSpace
    from b4msa.utils import tweet_iterator
    X = [x for x in tweet_iterator(TWEETS)]
    emo = EmoSpace()
    Xs = [emo[x] for x in X]
    assert len(Xs) == len(X) and len(Xs[0]) == 64
    assert emo.decision_function(X).shape[1] == 64


def test_EmoSpaceEn():
    from EvoMSA.model import EmoSpaceEn
    cls = EmoSpaceEn()
    assert cls


def test_EmoSpaceAr():
    from EvoMSA.model import EmoSpaceAr
    cls = EmoSpaceAr()
    assert cls


def test_tonp():
    from EvoMSA.model import B4MSATextModel
    from b4msa.utils import tweet_iterator
    c = B4MSATextModel([x for x in tweet_iterator(TWEETS)])
    X = [c[x] for x in tweet_iterator(TWEETS)]
    Xp = c.tonp(X)
    assert Xp.shape[0] == len(X) and Xp.shape[1] == c.num_terms


def test_AffectiveEs():
    from EvoMSA.model import AffectiveEs
    aff = AffectiveEs()
    _ = aff['adoracion XxX fervor vergazo']
    assert len(_) == 3


def test_AffectiveEn():
    from EvoMSA.model import AffectiveEn
    aff = AffectiveEn()
    _ = aff['adorably XxX elation vergazo']
    assert len(_) == 2


def test_AffectiveAr():
    from EvoMSA.model import AffectiveAr
    aff = AffectiveAr()
    _ = aff['adorably XxX elation vergazo']
    assert len(_) == 0


def test_ThumbsUpDownEs():
    from EvoMSA.model import ThumbsUpDownEs
    thumbs = ThumbsUpDownEs()
    _ = thumbs['adoracion XxX fervor vergazo']
    assert _ == (2, 1)


def test_ThumbsUpDownEn():
    from EvoMSA.model import ThumbsUpDownEn
    aff = ThumbsUpDownEn()
    _ = aff['adorably XxX elation vergazo']
    assert (2, 0) == _


def test_ThumbsUpDownAr():
    from EvoMSA.model import ThumbsUpDownAr
    aff = ThumbsUpDownAr()
    _ = aff['adorably XxX elation vergazo']
    assert (0, 0) == _


def test_OutputClassifier():
    import numpy as np
    from EvoMSA.model import Corpus, OutputClassifier
    from b4msa.utils import tweet_iterator
    from sklearn.preprocessing import LabelEncoder
    c = Corpus([x['text'] for x in tweet_iterator(TWEETS)])
    X = c.tonp([c[x['text']] for x in tweet_iterator(TWEETS)])
    y = [x['klass'] for x in tweet_iterator(TWEETS)]
    le = LabelEncoder().fit(y)
    y = le.transform(y)
    b = OutputClassifier(output='xx')
    assert b._output == 'xx'
    b.fit(X, y)
    assert os.path.isfile('xx_train.csv')
    pr = b.decision_function(X)
    assert os.path.isfile('xx_test.csv')
    assert len(open('xx_test.csv').readlines()) == pr.shape[0]
