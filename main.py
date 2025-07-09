from resume_parser import ResumeParser

if __name__ == '__main__':
    parser = ResumeParser('resume.pdf')
    parser.update_html('index.html')
