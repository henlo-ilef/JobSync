import { connectToDB } from '@utils/database';
import Post from '@models/post';

import job_ads from '../../../../data/ads_data_cleaned.json';


// Vectorization function
function CountVectorizer(text) {
  const words = text.split(' ');
  const vector = {};
  for (const word of words) {
    if (vector[word]) {
      vector[word]++;
    } else {
      vector[word] = 1;
    }
  }
  return vector;
}

function cosineSimilarity(vec1, vec2) {
    let dotProduct = 0;
    let magnitude1 = 0;
    let magnitude2 = 0;
  
    for (const word in vec1) {
      if (vec2[word]) {
        dotProduct += vec1[word] * vec2[word];
      }
      magnitude1 += vec1[word] ** 2;
    }
  
    for (const word in vec2) {
      magnitude2 += vec2[word] ** 2;
    }
  
    if (magnitude1 === 0 || magnitude2 === 0) {
      return 0; // Avoid division by zero
    }
  
    const similarity = dotProduct / (Math.sqrt(magnitude1) * Math.sqrt(magnitude2));
    return similarity;
}
  

export const POST = async (req) => {
  const { userId, summary, tag } = await req.json();

  try {
    await connectToDB();
    const newPost = new Post({
      creator: userId,
      summary,
      tag,
    });
    await newPost.save();

    // Prepare the list for storing similarity scores
    const similarity_scores = [];

    // Calculate the similarity for each job ad
    for (const job_ad of job_ads) {
      const text = [summary, job_ad["Job Description"]]; // Using the input summary and job description from JSON
      const vec1 = CountVectorizer(text[0]);
      const vec2 = CountVectorizer(text[1]);
      const similarity_score = cosineSimilarity(vec1, vec2);
      similarity_scores.push(similarity_score);
    }

    // Sort similarity_scores in descending order and get the indices of the top 10 scores
    const top_10_indices = similarity_scores
      .map((score, index) => ({ score, index }))
      .sort((a, b) => b.score - a.score)
      .slice(0, 10)
      .map(entry => entry.index);

      // Prepare the response data
        const similarity_results = top_10_indices.map(i => ({
            jobInfo: `${job_ads[i]["Job Title"]} at ${job_ads[i]["Company Name"]}`,
            matchPercentage: (similarity_scores[i] * 100).toFixed(2),
        }));

    return new Response(
      JSON.stringify({ newPost, similarity_results }),
      { status: 201 }
    );
  } catch (error) {
    console.error(error);
    return new Response('Failed to create a new post', { status: 500 });
  }
};
