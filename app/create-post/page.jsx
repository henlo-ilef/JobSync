"use client";
import { useState } from 'react';
import {useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';

import Form from '@components/Form';
import PostCard from '@components/PostCard';

const CreatePost = () => {
  const router = useRouter();
  const { data: session } = useSession();
  const [submitting, setSubmitting] = useState(false);
  const [ post, setPost ] = useState({
    summary: '',
    tag: '',
  });
  const createPost = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try{
      const response = await fetch('/api/post/new',{ 
        method: 'POST',
        body: JSON.stringify({
          summary: post.summary,
          userId: session?.user.id,
          tag: post.tag
        })
      })
      if (response.ok){
        const responseData = await response.json(); // Parse the JSON response
      console.log(responseData.similarity_results); // Access similarity_results from the parsed response data
      alert(JSON.stringify(responseData.similarity_results, null, 2));
  
      router.push('/');
      }
    } catch (error){
      console.log(error);
    }
    finally{
      setSubmitting(false)
    }
  }
  return (
    <div>
      <Form
      type="Create"
      post={post}
      setPost={setPost}
      submitting={submitting}
      handleSubmit={createPost}
    ></Form>
    </div>
  )
}

export default CreatePost;
