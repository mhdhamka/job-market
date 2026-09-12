import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.processing.cleaner import TextCleaner

def test_text_cleaner_html_tags_and_entities():
    # Raw HTML text with tags, encoded entities, and messy whitespaces
    raw_html = """
        <div>
            <h1> Senior Python Developer &amp; Engineer </h1>
            <p>Required: <b>SQL</b>, <i>FastAPI</i> &amp; Docker.</p>
            <p>Salary: RM 6,000 &ndash; RM 10,000</p>
        </div>
    """
    
    cleaned = TextCleaner.clean_text(raw_html)
    
    # Assert HTML tags are removed and entities are decoded correctly
    assert "<div>" not in cleaned
    assert "<h1>" not in cleaned
    assert "<b>" not in cleaned
    assert "&amp;" not in cleaned
    assert "&ndash;" not in cleaned
    
    # Assert text content and spacing are normalized properly
    assert "Senior Python Developer & Engineer" in cleaned
    assert "SQL , FastAPI & Docker." in cleaned
    assert "Salary: RM 6,000 – RM 10,000" in cleaned

def test_text_cleaner_empty_and_invalid_input():
    # Test handling of empty strings or non-string inputs
    assert TextCleaner.clean_text("") == ""
    assert TextCleaner.clean_text(None) == ""
    assert TextCleaner.clean_text(12345) == ""  # type: ignore