import fitz  # PyMuPDF
from whoosh.fields import Schema, TEXT
from whoosh.index import create_in
from whoosh.writing import AsyncWriter
from whoosh.qparser import QueryParser

# Define the schema
schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True))

# Create an index directory and index object
index_dir = 'indexdir'
ix = create_in(index_dir, schema)

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    pdf_document = fitz.open(pdf_path)
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

def add_document_to_index(pdf_text, title):
    """Add a document to the Whoosh index."""
    writer = AsyncWriter(ix)
    writer.add_document(title=title, content=pdf_text)
    writer.commit()

def search_index(query_string):
    """Search the Whoosh index and return results."""
    results = []
    with ix.searcher() as searcher:
        query_parser = QueryParser("content", ix.schema)
        query = query_parser.parse(query_string)
        search_results = searcher.search(query)
        for hit in search_results:
            results.append(hit['title'])
    return results

def main():
    """Main function to run the search engine."""
    import os

    # Ensure the index directory exists
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)

    # Path to your PDF file
    pdf_path = 'example.pdf'  # Change this to your PDF file path
    title = "Example PDF Title"  # Change this to a meaningful title for your PDF

    # Extract text and index the document
    pdf_text = extract_text_from_pdf(pdf_path)
    add_document_to_index(pdf_text, title)

    while True:
        query_string = input("Enter search term (or 'exit' to quit): ")
        if query_string.lower() == 'exit':
            break
        results = search_index(query_string)
        if results:
            print("Search Results:")
            for result in results:
                print(f"- {result}")
        else:
            print("No results found.")

if __name__ == '__main__':
    main()
