import Navbar from "../components/navbar/navbar";
import Image from 'next/image'
import styles from "../styles/Home.module.css"

import {useState} from 'react'

import PDFViewer from "../components/book/pdf-viewer";

import Comments from '../components/comments/comments'

export default function PDF() {
  const [showComments, setShowComments] = useState(false)

  const handleShowComments = () => {
    setShowComments(!showComments)
  }

  return (
    <div className={styles.container}>
      <Navbar />
     
      <div className={styles.content} >
            <PDFViewer />
                      
            {showComments && 
              <Comments />               
            }       
      </div>

    </div>
    )
}
