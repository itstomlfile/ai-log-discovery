import gensim

def load_model(model_filename):
    """
    Load a pretrained Word2Vec model from a file.
    """
    return gensim.models.Word2Vec.load(model_filename)
