import re, os
import numpy as np
from gensim.models.doc2vec import Doc2Vec
from numpy.linalg import norm

MODEL_PATH = os.path.join(os.path.dirname(__file__),'job_matching', 'models', 'cv_job_maching.model')

def preprocess_text(text):
        text = text.lower()
        text = re.sub('[^a-z]', ' ', text)
        text = re.sub(r'\d+', '', text)
        text = ' '.join(text.split())
        return text

def match_resume_to_jd(resume_text, jd_text):
    model = Doc2Vec.load(MODEL_PATH)
    v1 = model.infer_vector(preprocess_text(resume_text).split())
    v2 = model.infer_vector(preprocess_text(jd_text).split())
    similarity = 100*(np.dot(np.array(v1), np.array(v2))) / (norm(np.array(v1)) * norm(np.array(v2)))
    return round(similarity, 2)
