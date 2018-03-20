"""Unit tests for the TF-IDF backend in Annif"""

import annif
import annif.backend
import annif.corpus
import os.path


def test_tfidf_load_subjects(tmpdir):
    annif.cxapp.app.config['DATADIR'] = str(tmpdir)
    tfidf_type = annif.backend.get_backend_type("tfidf")
    tfidf = tfidf_type(
        backend_id='tfidf',
        params={'analyzer': 'snowball(finnish)', 'chunksize': 10, 'limit': 10})

    subjdir = os.path.join(
        os.path.dirname(__file__),
        'corpora',
        'archaeology',
        'subjects')
    subjects = annif.corpus.SubjectDirectory(subjdir)
    tfidf.load_subjects(subjects)
    assert len(tfidf._subjects) == 125
    assert len(tfidf._dictionary) > 0
    assert tfidf._tfidf is not None
    assert len(tfidf._index) > 0
    assert tmpdir.join('backends/tfidf/subjects').exists()
    assert tmpdir.join('backends/tfidf/subjects').size() > 0
    assert tmpdir.join('backends/tfidf/dictionary').exists()
    assert tmpdir.join('backends/tfidf/dictionary').size() > 0
    assert tmpdir.join('backends/tfidf/tfidf').exists()
    assert tmpdir.join('backends/tfidf/tfidf').size() > 0
    assert tmpdir.join('backends/tfidf/index').exists()
    assert tmpdir.join('backends/tfidf/index').size() > 0


def test_tfidf_analyze(tmpdir):
    annif.cxapp.app.config['DATADIR'] = str(tmpdir)
    tfidf_type = annif.backend.get_backend_type("tfidf")
    tfidf = tfidf_type(
        backend_id='tfidf',
        params={'analyzer': 'snowball(finnish)', 'chunksize': 1, 'limit': 10})

    subjdir = os.path.join(
        os.path.dirname(__file__),
        'corpora',
        'archaeology',
        'subjects')
    subjects = annif.corpus.SubjectDirectory(subjdir)
    tfidf.load_subjects(subjects)

    results = tfidf.analyze("""Arkeologiaa sanotaan joskus myös
        muinaistutkimukseksi tai muinaistieteeksi. Se on humanistinen tiede
        tai oikeammin joukko tieteitä, jotka tutkivat ihmisen menneisyyttä.
        Tutkimusta tehdään analysoimalla muinaisjäännöksiä eli niitä jälkiä,
        joita ihmisten toiminta on jättänyt maaperään tai vesistöjen
        pohjaan.""")

    assert len(results) == 10
    assert 'http://www.yso.fi/onto/yso/p1265' in [
        result.uri for result in results]
    assert 'arkeologia' in [result.label for result in results]