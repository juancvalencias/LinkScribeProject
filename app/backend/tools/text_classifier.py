import joblib

from transformers import pipeline

from .scrapping_tool import ScrapTool


class TextClassifier:
    def __init__(self, model_path, vectorizer_path, id_to_category) -> None:
        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)
        self.id_to_category = id_to_category

    def predict(self, text) -> str:

        vectorized_text = self.vectorizer.transform([text])
        category_id: int = self.model.predict(vectorized_text)[0]
        return self.id_to_category.get(category_id, "Unknown")
    
    def summarize(self,text)-> str:
                
        pipe = pipeline("summarization", model="facebook/bart-large-cnn")
        summary = pipe(text[:1024], max_length=150, min_length=30, do_sample=False)
        summary = summary[0]['summary_text']
        return summary
