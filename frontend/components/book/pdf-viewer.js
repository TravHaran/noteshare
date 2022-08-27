import { useState, useEffect } from "react";
import { Document, Page, pdfjs } from "react-pdf";
import workerSrc from "../../pdf-worker";

import Image from 'next/image'

import { Textfit } from 'react-textfit';

import files from '../../data/files.json'

import { motion } from "framer-motion";

import styles from './pdf-viewer.module.css'

pdfjs.GlobalWorkerOptions.workerSrc = workerSrc;

const myFile = files[0]
const pdf = myFile['content']

export default function PDFViewer() {
  
  const [file, setFile] = useState(pdf);
  const [index, setIndex] = useState(0);
  const [numPages, setNumPages] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);
  const [pageHeight, setPageHeight] = useState(0)

  function BookChangeNext() {
    if(index !== files.length - 1) {
    setIndex(index => index + 1)
    const myFile = files[index + 1]
    const pdf = myFile['content']   
    setFile(pdf)
    setPageNumber(1)
    } else {
      return
    } 
}
  function BookChangePrevious() {
    if(index !== 0) {
          setIndex(index => index - 1)
    const myFile = files[index - 1]
    const pdf = myFile['content']   
    setFile(pdf) 
    setPageNumber(1)
    } else {
      return
    }

}
  function debounce(fn, ms) {
    let timer
    return _ => {
      clearTimeout(timer)
      timer = setTimeout(_ => {
        timer = null
        fn.apply(this, arguments)
      }, ms)
    };
  }

  useEffect(()=> {
    const debouncedHandleResize = debounce(function handleResize() {
      const h = window.innerHeight;
      const pageHeightAlg = 0.7 * h;
      setPageHeight(pageHeightAlg)}, 250)

    window.addEventListener('resize', debouncedHandleResize)
    return _ => {
      window.removeEventListener('resize', debouncedHandleResize)
    }
})

  const onFileChange = () => {
    files.map((file) => {
      return files?.files.map((item) => {
        const content = item.content;
        return {
          content
        };
      });
    })
  }

  const nextPageHandler = () => {
    if(pageNumber === numPages) {
        return
    }else {
        setPageNumber(pageNumber + 1)        
    }
  }
  const previousPageHandler = () => {
    if(pageNumber === 1) {
        return
    }else {
        setPageNumber(pageNumber - 1)        
    }
  }

  const handleWindowSizeChange = () => {
    setPageHeight(window.innerWidth);
    
};



  function onDocumentLoadSuccess({ numPages: nextNumPages }) {
      setNumPages(nextNumPages);  
        const debouncedHandleResize = debounce(function handleResize() {
      const h = window.innerHeight;
      const pageHeightAlg = 0.7 * h;
      setPageHeight(pageHeightAlg)}, 250)

    debouncedHandleResize()

  }

  return (
    <div className={styles.container}>
      <div className={styles.col1}>
      <div className={styles.grid}>
        <div className={styles.votingButtons}>
          <div className={styles.Vote}>
            &#8593;        
          </div>
          <div className={styles.Vote}>
            &#8595;        
          </div>
        </div>
        <div>
        <div className={styles.book}>
        <motion.div className={styles.page} initial={{ opacity: 0, scale: 0.5 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{
          duration: 0.8,
          delay: 0.2,
          ease: [0, 0.71, 0.2, 1.01]
        }}>
            <Document file={file} onLoadSuccess={onDocumentLoadSuccess}>
            <motion.div initial={{ opacity: 0, scale: 0.5 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{
          duration: 0.5,
          delay: 0.5,
          ease: [0, 0.71, 0.2, 1.01]
        }}>
              <Page className={styles.bookPage} pageNumber={pageNumber} height={pageHeight} wrap={false}>
              
              </Page> 
              
             </motion.div>  
            </Document>   
                  
        </motion.div>
          <div className={styles.bookDetailsWrapper}>
          <div className={styles.bookDetails}>
            <div className={styles.bookDetailsHeader}>
              <div>
                <h3>Francis B.</h3>
              </div>
              <div className={styles.bookDetailsText}>
                <p>Just made some notes regarding french stuff... enjoy :)</p>
              </div>            
            </div>          
          </div>

          </div>        
      </div> 
      
          <div className={styles.navigation}>
            <button className={styles.Arrow} onClick={previousPageHandler}>&#8592;</button>
            <div className={styles.index}>
              <p>{pageNumber}/{numPages}</p>
            </div>
            <button className={styles.Arrow} onClick={nextPageHandler}>&#8594;</button>        
          </div>  
      </div>


      <div className={styles.navAndComments}>
        <div className={styles.navigateBooks}>
          <button onClick={BookChangePrevious} className={styles.navigateBooksButton} >&#8593;</button>            
          <button className={styles.navigateBooksButton} onClick={BookChangeNext}>	&#8595;</button>
        </div>    
        <div className={styles.commentsIconWrapper}>
          <Image src="/static/CommentsIcon.png" width={25} height={25} alt="Show Comments Icon" />
      </div>      
      </div>      
        </div>
      </div>
    </div>
  );
}
