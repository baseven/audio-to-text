import numpy as np


# use cosine similarity to determine who similar two vectors are
def cosine_dist(vector1, vector2):
    dot = np.dot(vector1, vector2)
    norm_vec1 = np.linalg.norm(vector1)
    norm_vec2 = np.linalg.norm(vector2)
    cosine_similarity = dot / (norm_vec1 * norm_vec2)
    return cosine_similarity


def set_speaker(item, input_cv_dict):
    most_similar_person = None
    most_similar_score = 0
    # print(f"!!!Item {item}")
    input_vec = item['spk']
    # return immediately if input vector was empty (too short text snippet for identification)
    if len(input_vec) == 0:
        return "Unknown"

    # compare all combination and save  the closest one to return below
    for person in input_cv_dict:
        # print(f"!!! input_vec\n"
        #       f" {input_vec}")
        # print(f"!!!input_cv_dict[person]\n"
        #       f" {input_cv_dict[person]}")

        smlr = cosine_dist(input_vec, input_cv_dict[person])
        if smlr > most_similar_score:
            most_similar_score = smlr
            most_similar_person = person

    item['spk'] = most_similar_person if most_similar_score > 0.5 else "Unkown"
    return item
