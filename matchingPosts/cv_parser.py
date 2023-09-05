import requests
import base64
import pandas as pd
# Read the PDF file from your local machine
file_path = "D:/HenloIlef/SUMMER 2K23/Internship SFS/matching_project/cv1.pdf"
with open(file_path, "rb") as file:
    pdf_data = file.read()
from pyresparser import ResumeParser

# Encode the PDF data to base64
base64_data = base64.b64encode(pdf_data).decode("utf-8")

# Prepare the payload with the base64-encoded PDF data
data = ResumeParser('D:/HenloIlef/SUMMER 2K23/Internship SFS/matching_project/cv1.pdf').get_extracted_data()

url = "https://ai-resume-parser-extractor.p.rapidapi.com/pdf-base64"

payload = { "base64": base64_data }
headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "9cab40c7ffmsh3d92a274c2eae02p1c49d5jsn82a3b9890136",
	"X-RapidAPI-Host": "ai-resume-parser-extractor.p.rapidapi.com"
}

response = requests.post(url, json=payload, headers=headers)
data = response.json()
print(data)
# Extract the specific keys and their values
keys_to_extract = ['fullName', 'contactInformation', 'objective', 'profileSummary', 'skills', 'languages', 'experience', 'education', 'certifications', 'projects', 'publications', 'references']
extracted_data = {}

for key in keys_to_extract:
    if key in data['data']['content']:
        extracted_data[key] = [data['data']['content'][key]]
print(extracted_data)
# Create a DataFrame from the extracted data
cvdf = pd.DataFrame(extracted_data)
cvdf.to_csv('cv_data.csv', index=False)
#cvdf.to_csv('cv_data2.csv', index=False)