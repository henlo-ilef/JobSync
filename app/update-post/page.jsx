"use client";
import { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';

import Form from '@components/Form';

const EditPost = () => {
  const router = useRouter();
  const [submitting, setSubmitting] = useState
  (false);
  const searchParam = useSearchParams();
  const postId = searchParam.get('id');


  const [ post, setPost ] = useState({
    summary: '',
    tag: '',
  });

  useEffect(() => {
    const getPostDetails = async () => {
      const response = await fetch(`/api/post/${postId}`);  
      const data = await response.json();
      setPost({
        summary : data.summary,
        tag: data.tag
      });
    }
    if (postId) getPostDetails();
  }, [postId])
  

  const updatePost = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    if(!postId) alert("Post ID not found");

    try{
      const response = await fetch(`/api/post/${postId}`,{ 
        method: 'PATCH',
        body: JSON.stringify({
          summary: post.summary,
          tag: post.tag
        })
      })
      if (response.ok){
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
    <Form
      type="Edit"
      post={post}
      setPost={setPost}
      submitting={submitting}
      handleSubmit={updatePost}
    >
      
    </Form>
  )
}

export default EditPost