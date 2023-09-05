import React from 'react'
import Feed from '@components/Feed';
const Home = () => {
  return (
    <section className="w-full flex-center flex-col">
        <h1 className="head_text text-center">
            Calculate & Share
            <br className="max-md:hidden" />
            <span className="orange_gradient text-center">Resume Scores</span>
        </h1>
        <p className="desc text-center">
            JobSync is an open 
            source score calculating tool for
            modern world to calculate resume summary scores based on their similarity to job offers on Glassdoor and share their resume summaries with other candidates and recruiters.
        </p>
        <Feed />
    </section>
  )
}

export default Home