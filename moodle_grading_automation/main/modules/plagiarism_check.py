from numpy import vectorize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests

def get_plagiarism_result_data(answers):
    names_of_users = []

    for el in answers:
        names_of_users.append(el['firstname']+" "+el['lastname'])

    

    list_of_dicts = answers
    a_key = 'url'
    urls = [a_dict[a_key] for a_dict in list_of_dicts]
    print(urls)
    
    htmls = []
    for url in urls:
        htmls.append(requests.get(url).text)
    
    sample_contents = htmls
    vectorize = lambda Text: TfidfVectorizer().fit_transform(Text).toarray()
    similarity = lambda doc1, doc2: cosine_similarity([doc1, doc2])

    vectors = vectorize(sample_contents)

    def check_plagiarism():
        results = set()
        s_vectors = list(zip(names_of_users, vectors))
        for sample_a, text_vector_a in s_vectors:
            new_vectors = s_vectors.copy()
            current_index = new_vectors.index((sample_a, text_vector_a))
            del new_vectors[current_index]
            for sample_b, text_vector_b in new_vectors:
                sim_score = similarity(text_vector_a, text_vector_b)[0][1]
                sample_pair = sorted((sample_a, sample_b))
                score = sample_pair[0], sample_pair[1], round(sim_score * 100)
                results.add(score)
        return results
    
    results = check_plagiarism()
    print(results)

    # for data in check_plagiarism():
    #     results.append(data)

    return results