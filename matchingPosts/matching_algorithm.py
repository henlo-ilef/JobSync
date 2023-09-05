# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 18:41:57 2023

@author: henloIlef
"""
import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import chardet

# Detect the encoding of the CSV file
def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
    return result['encoding']


# Load the job ads from the CSV file
job_ads = []
encoding = detect_encoding('ads_data_cleaned.csv')
with open('ads_data_cleaned.csv', 'r', encoding=encoding) as file:
    reader = csv.DictReader(file)
    for row in reader:
        job_ads.append(row["Job Description"])  # the job description are in the first column
print(job_ads)

# Load the resume from the CSV file
encoding = detect_encoding('cv_data.csv')
with open('cv_data.csv', 'r', encoding=encoding) as file:
    reader = csv.DictReader(file)
    resume_data = next(reader)  # Assuming there's only one row for the resume
    
# Extract the relevant information from the resume data
resume = resume_data['fullName']
resume += '\n' + resume_data['contactInformation']
resume += '\n' + resume_data['objective']
resume += '\n' + resume_data['profileSummary']
resume += '\n' + resume_data['skills']
resume += '\n' + resume_data['languages']
resume += '\n' + resume_data['experience']
resume += '\n' + resume_data['education']
resume += '\n' + resume_data['certifications']
resume += '\n' + resume_data['projects']
resume += '\n' + resume_data['publications']
resume += '\n' + resume_data['references']

# Prepare the list for storing similarity scores
similarity_scores = []

# Calculate the similarity for each job ad
for job_ad in job_ads:
    # Create a list of resume and current job ad
    text = [resume, job_ad]

    # Perform count vectorization and similarity calculation
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(text)
    similarity_score = cosine_similarity(count_matrix)[0][1]
    similarity_scores.append(similarity_score)

# Print the similarity scores for each job ad
for i, score in enumerate(similarity_scores):
    match_percentage = round(score * 100, 2)
    print("Job Ad {} matches about {}% of the resume.".format(i+1, match_percentage))
