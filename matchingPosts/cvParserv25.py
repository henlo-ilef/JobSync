from pyresparser import ResumeParser
import PyPDF2

def extract_text_from_pdf(pdf_file):
    text = ""
    with open(pdf_file, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

def parse_resume_text(text):
    # Use the ResumeParser from pyresparser
    data = ResumeParser(text).get_extracted_data()

    resume_data = {
        "fullName": data.get("name", None),
        "contactInformation": data.get("email", None),
        "skills": data.get("skills", None),
        "objective": data.get("summary", None)
    }

    return resume_data

def main():
    # Replace 'path/to/resume.pdf' with the actual path to your resume PDF file
    resume_pdf = 'D:/HenloIlef/SUMMER 2K23/Internship SFS/matching_project/app/matchingAlgos/cv1.pdf'

    # Extract text from the PDF resume
    resume_text = extract_text_from_pdf(resume_pdf)

    # Parse the text and get the dictionary
    resume_data = parse_resume_text(resume_text)

    # Print the parsed data
    print(resume_data)

if __name__ == "__main__":
    main()
