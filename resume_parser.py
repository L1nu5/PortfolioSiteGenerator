import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from bs4 import BeautifulSoup
import io
import re


class ResumeParser:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.text = self._extract_text_from_pdf()

    def _extract_text_from_pdf(self):
        text = ""
        try:
            doc = fitz.open(self.pdf_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                pix = page.get_pixmap()
                img_data = pix.tobytes("ppm")
                img = Image.open(io.BytesIO(img_data))
                text += pytesseract.image_to_string(img)
            doc.close()
        except Exception as e:
            print(f"Error processing PDF: {e}")
        return text

    def parse_experience(self):
        # This is a simple example. Regex would be needed for a real resume.
        experience_section = re.search(
            r"Experience(.*?)Education", self.text, re.DOTALL
        )
        if experience_section:
            return experience_section.group(1).strip()
        return "Could not parse experience."

    def parse_education(self):
        education_section = re.search(
            r"Education(.*?)Projects", self.text, re.DOTALL
        )
        if education_section:
            return education_section.group(1).strip()
        return "Could not parse education."

    def parse_projects(self):
        projects_section = re.search(
            r"Projects(.*?)Awards", self.text, re.DOTALL
        )
        if projects_section:
            return projects_section.group(1).strip()
        return "Could not parse projects."

    def parse_awards(self):
        awards_section = re.search(r"Awards(.*)", self.text, re.DOTALL)
        if awards_section:
            return awards_section.group(1).strip()
        return "Could not parse awards."

    def _generate_section_html(self, title, content):
        return f"<h2>{title}</h2><p>{content}</p>"

    def update_html(self, html_path):
        with open(html_path, 'r') as f:
            soup = BeautifulSoup(f, 'html.parser')

        sections = {
            'experience': ('Experience', self.parse_experience()),
            'education': ('Education', self.parse_education()),
            'projects': ('Projects', self.parse_projects()),
            'awards': ('Awards and Achievements', self.parse_awards())
        }

        for section_id, (title, content) in sections.items():
            section_html = self._generate_section_html(title, content)
            soup.find('section', id=section_id).inner_html = section_html

        with open(html_path, 'w') as f:
            f.write(str(soup))
