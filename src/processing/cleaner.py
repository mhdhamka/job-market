import re
import html

class TextCleaner:
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Cleans raw scraped text by decoding HTML entities, removing HTML tags, 
        and normalizing whitespace.
        """
        if not text or not isinstance(text, str):
            return ""
        
        # Decode HTML entities (e.g., &amp; -> &, &nbsp; -> space)
        text = html.unescape(text)
        
        # Remove HTML tags
        tag_pattern = re.compile('<.*?>')
        text = tag_pattern.sub(' ', text)
        
        # Normalize whitespace (collapse multiple spaces, tabs, and newlines into a single space)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

if __name__ == "__main__":
    # Quick test
    sample_raw = "<div>  Software Engineer &amp; Developer needed!  <br> Experience with Python. </div>"
    print("Before:", sample_raw)
    print("After: ", TextCleaner.clean_text(sample_raw))