from sklearn.metrics import precision_score, recall_score, f1_score, average_precision_score

relevant_documents = [1, 2, 3, 4, 5]
retrieved_documents = [1, 2, 3, 6, 7]

precision = len(set(relevant_documents).intersection(retrieved_documents)) / len(retrieved_documents)
recall = len(set(relevant_documents).intersection(retrieved_documents)) / len(relevant_documents)
f_measure = (
    2 * (precision * recall) / (precision + recall)
    if precision + recall > 0 else 0
)

print("Manual Calculation:")
print("Precision:", precision)
print("Recall:", recall)
print("F-measure:", f_measure)

y_true = [1 if doc in relevant_documents else 0 for doc in retrieved_documents]
y_pred = [1 if doc in retrieved_documents else 0 for doc in relevant_documents]

sklearn_precision = precision_score(y_true, y_pred)
sklearn_recall = recall_score(y_true, y_pred)
sklearn_f1 = f1_score(y_true, y_pred)

print("\nEvaluation Toolkit (sklearn):")
print("Precision (sklearn):", sklearn_precision)
print("Recall (sklearn):", sklearn_recall)
print("F1 Score (sklearn):", sklearn_f1)

y_scores = [1 if doc in relevant_documents else 0 for doc in retrieved_documents]
avg_precision = average_precision_score(y_true, y_scores)

print("Average Precision:", avg_precision)
