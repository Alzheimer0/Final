import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from heapq import nlargest

nlp = spacy.load("en_core_web_sm")


def summarize_text(text, num_sentences=3):
    """
    Summarizes the input text by identifying the most relevant sentences.

    Args:
        text (str): The text to be summarized.
        num_sentences (int): The number of sentences to include in the summary.

    Returns:
        str: The summary of the text.
    """
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]

    word_frequency = {}
    for word in doc:
        if not word.is_stop and word.is_alpha:
            key = word.text.lower()
            word_frequency[key] = word_frequency.get(key, 0) + 1

    sentence_scores = {}
    for sentence in sentences:
        for word in sentence.split():
            word_lower = word.lower()
            if word_lower in word_frequency:
                sentence_scores[sentence] = sentence_scores.get(sentence, 0) + word_frequency[word_lower]

    summary_sentences = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    summary = " ".join(summary_sentences)

    return summary


def answer_question(question, text):
    """
    Answers a question by finding the most similar sentence in the text.

    Args:
        question (str): The question to be answered.
        text (str): The text to search for the answer.

    Returns:
        str: The most relevant sentence from the text.
    """
    sentences = text.split(".")
    vectorizer = TfidfVectorizer(stop_words="english")

    vectors = vectorizer.fit_transform(sentences + [question])
    similarity = cosine_similarity(vectors[-1], vectors[:-1])[0]

    best_sentence_index = similarity.argmax()
    return sentences[best_sentence_index].strip()


text = """
In Speed Rush, the latest high-octane racing game, players are immersed
in a world of adrenaline-pumping tracks and custom cars. Experience breathtaking
graphics, realistic physics, and intense rivalries as you climb the leaderboards.
Master the art of drifting, boost management, and strategic shortcuts to outpace
your competition.
With an array of multiplayer modes and seasonal challenges,
Speed Rush keeps the excitement alive. Do you have what it takes to become the
ultimate racing champion?
"""

summary = summarize_text(text)
print("Game Text Summary:")
print(summary)

question = "What is Speed Rush about?"
answer = answer_question(question, text)

print("\nQuestion:", question)
print("Answer:", answer)
