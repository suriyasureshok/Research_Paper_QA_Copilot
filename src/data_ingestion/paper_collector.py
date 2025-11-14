import urllib.request as libreq
import feedparser
import requests
import fitz

class ArxivPaperCollection:
    def __init__(self, query, max_results=5):
        self.query = query
        self.max_results = max_results
        self.base_url = 'http://export.arxiv.org/api/query?'
        
    def fetch_papers(self):
        """
        Fetch papers from arXiv based on the query.
        Args:
            query (str): The search query.
            max_results (int): Maximum number of results to fetch.
        Returns:
            list: A list of dictionaries containing paper metadata and full text.
        """
        search_url = f"{self.base_url}search_query=all:{self.query}&start=0&max_results={self.max_results}"
        with libreq.urlopen(search_url) as url:
            response = url.read()
        
        feed = feedparser.parse(response)
        papers = []
        
        for entry in feed.entries:
            pdf_link = next((link.href for link in entry.links if 'pdf' in link.href), None)
            full_text = ""
            if pdf_link:
                try:
                    pdf_response = requests.get(pdf_link)
                    pdf_response.raise_for_status()
                    pdf_document = fitz.open(stream=pdf_response.content, filetype="pdf")
                    full_text = ""
                    for page in pdf_document:
                        page_text = page.get_text()
                        full_text += page_text
                    pdf_document.close()
                    # Successfully extracted text
                except Exception as e:
                    print(f"Error extracting text from {pdf_link}: {e}")
                    full_text = ""
            
            paper = {
                'id': entry.id,
                'title': entry.title,
                'authors': [author.name for author in entry.authors],
                'full_text': full_text,
                'published': entry.published,
                'link': entry.link,
                'pdf_link': pdf_link
            }
            papers.append(paper)
        
        return papers