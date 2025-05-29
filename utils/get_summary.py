from transformers import pipeline, Pipeline
from typing import Optional

# Global variable to store the model if caching is enabled
_cached_summarizer: Optional[Pipeline] = None

def summarize_article(text: str, max_length: int = 200, min_length: int = 30, use_cache: bool = True) -> Optional[str]:
    """
    Summarizes a given article using the BART summarization model.
    
    Parameters:
        text (str): The input article or text to summarize.
        max_length (int): Maximum length of the summary.
        min_length (int): Minimum length of the summary.
        use_cache (bool): If True, cache the model for reuse.
        
    Returns:
        Optional[str]: The summarized text or error message.
    """
    global _cached_summarizer

    try:
        if not text or len(text.strip()) < min_length:
            return "Error: Input text is too short to summarize."

        if use_cache:
            if _cached_summarizer is None:
                _cached_summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
            summarizer = _cached_summarizer
        else:
            summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

        summary = summarizer(text[:3500], max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']

    except Exception as e:
        # print(summary)
        return f"Error during summarization: {str(e)}"


# Example used cases has been written here.
def main():
    # Example input
    article = """
    Quantum entanglement, in simple terms, means that two or more particles can become linked together in a way that they share the same fate, no matter how far apart they are. If you measure a property of one particle, you instantly know the corresponding property of the other, according to Vajiram & Ravi. It's like they're connected in a mysterious way, even across vast distances. 
    Here's a more detailed explanation:
    Connected Particles:
    Entangled particles are interconnected in a special way, unlike normal particles that act independently. 
    Shared Fate:
    The properties of entangled particles are linked, meaning they behave as one until measured. 
    Instantaneous Influence:
    Measuring a property of one entangled particle instantly reveals the corresponding property of the other, regardless of distance. 
    No Message Passing:
    There's no signal or message traveling between the particles, it's a fundamental connection. 
    Example:
    Imagine two coins that are somehow linked. If one coin lands on heads, you instantly know the other will land on tails, even if they're far apart. 
    Quantum entanglement is a key part of quantum mechanics and has important implications for quantum technologies like quantum computing
    """
    
    print("🔍 Summarizing article...\n")
    summary = summarize_article(article, use_cache=True)
    print("📝 Summary:\n", summary)


# Run this block only if executed directly
if __name__ == "__main__":
    main()

