import { useState, useEffect } from "react";
import { Document, Page, pdfjs } from "react-pdf";
import workerSrc from "../../pdf-worker";
import pdfjsWorker from "pdfjs-dist/build/pdf.worker.entry";
import Image from 'next/image'
import Comments from '../comments/comments'
import comments from "../../data/comments.json";


import {useRouter} from 'next/router'
import { motion } from "framer-motion";
// import files from '../../data/files.json'
import styles from './pdf-viewer.module.css'



const PDFViewer = (props) => {
  
  const {bookSet=[], selectedBook=1, dataExport} = props

  const router = useRouter()

  const [file, setFile] = useState('');
  const [index, setIndex] = useState(null);
  const [numPages, setNumPages] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);
  const [pageHeight, setPageHeight] = useState(0);
  const [description, setDescription] = useState('')
  const [owner, setOwner] = useState('')
  const [library, setLibrary] = useState('')
  const [upVotes, setupVotes] = useState(null)
  const [downVotes, setdownVotes] = useState(null)
  const [showComments, setShowComments] = useState(true)
  const [commentCount, setCommentCount] = useState(comments.comments.length)
  const [upVote, setUpVote] = useState(false)
  const [downVote, setDownVote] = useState(false) 

useEffect(() => {
  if (!router.isReady) return;
  pdfjs.GlobalWorkerOptions.workerSrc = `https://unpkg.com/pdfjs-dist@2.12.313/build/pdf.worker.min.js`;
  const id= router.query.title 
  console.log(id) 
  console.log(router.query.title)
  bookSet.map(function(book) {
    if (book.id === id) {
      setFile(book.content)
      setOwner(book.owner)
      setLibrary(book.library)
      setDescription(book.description)
      setupVotes(book.upVotes)
      setdownVotes(book.downVotes)

    }
  })
}, [router.query.title, router.isReady, bookSet, router, upVote, downVote, showComments, index, pageNumber, numPages])
    const scaleUp = {scale: 1.1};
    const scaleDown = {scale: 0.95}

    const handleShowComments = () => {
        setShowComments(!showComments)
      }

      function BookChangeNext() {
        if(index !== bookSet.length - 1) {
        setIndex(index => index + 1)
        const myFile = bookSet[index + 1]
        const pdf = myFile['content'] 
        const myDescription = myFile["description"]
        const bookLibrary = myFile['library']
        const myOwner = myFile["owner"]
        const myUpVotes = myFile["upVotes"]
        const myDownVotes = myFile["downVotes"]
        router.push({
          pathname: router.pathname,
          query: {
            ...router.query,
            title: myFile.id
          }
        })
        setupVotes(myUpVotes)
        setDescription(myDescription)
        setLibrary(bookLibrary)
        setdownVotes(myDownVotes)
        setOwner(myOwner)    
        setFile(pdf)
        setPageNumber(1)
        } else {
          return
        } 
    }
    function BookChangePrevious() {
        if(index !== 0) {
              setIndex(index => index - 1)
        const myFile = bookSet[index - 1]
        const pdf = myFile['content']   
        const myDescription = myFile["description"]
        const bookLibrary = myFile['library']
        const myOwner = myFile["owner"]
        const myUpVotes = myFile["upVotes"]
        const myDownVotes = myFile["downVotes"]
        router.push({
          pathname: router.pathname,
          query: {
            ...router.query,
            title: myFile.id
          }
        })
        setupVotes(myUpVotes)
        setLibrary(bookLibrary)
        setDescription(myDescription)
        setdownVotes(myDownVotes)
        setOwner(myOwner) 
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

    const handleUpVote = () => {
      setUpVote(!upVote)
      setDownVote(false)
    }
    console.log("upVoted", {upVote})

    const handleDownVote = () => {
      setDownVote(!downVote)
      setUpVote(false)
    }
    console.log("downVoted", {downVote})

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
        const pageHeightAlg = 0.62 * h;
        setPageHeight(pageHeightAlg)}, 250)
      debouncedHandleResize()
    }    

//   useEffect(()=> {
  
//     const debouncedHandleResize = debounce(function handleResize() {
//       const h = window.innerHeight;
//       const pageHeightAlg = 0.62 * h;
//       setPageHeight(pageHeightAlg)}, 250)

//     window.addEventListener('resize', debouncedHandleResize)
//     return _ => {
//       window.removeEventListener('resize', debouncedHandleResize)
//     }
// }, [])


  return (
    <div className={styles.container}>
      <div className={styles.col1}>
      <div className={styles.grid}>
        <div className={styles.votingButtons}>
          <h3>{upVotes}</h3>            
          <div className={upVote ? styles.Voted: styles.Vote} onClick={handleUpVote}>
          <Image src="/static/spearUp.svg" width={20} height={20} alt="upVote" />      
          </div>
          <h3>{downVotes}</h3>             
          <div className={downVote ? styles.Voted: styles.Vote} onClick={handleDownVote}>
          <Image src="/static/spearDown.svg" width={20} height={20} alt="downVote" /> 
          </div>
        </div>
        <div>
        <div className={styles.book}>
        <div className={styles.page}>
            <Document file={file} onLoadError={console.log}  onSourceError={console.log} onLoadSuccess={onDocumentLoadSuccess}>
            <div>
              <Page className={styles.bookPage} pageNumber={pageNumber} height={pageHeight} wrap={false} />  
             </div>  
            </Document>   
                  
        </div>
          <div className={styles.bookDetailsWrapper}>
              <div className={styles.bookDetails}>
                <div className={styles.bookDetailsHeader}>
                  <div>
                    <b><h3>{library}</h3> </b>                   
                    <h4>{owner}</h4>
                  </div>
                  <div className={styles.bookDetailsText}>
                    <p>{description}</p>
                  </div>            
                </div>          
              </div>          
          </div>  
              
      </div> 
      
      
          <div className={styles.navigation}>
            <motion.button whileHover={{ ...scaleUp }} className={styles.Arrow} onClick={previousPageHandler}>&#8592;</motion.button>
            <div className={styles.index}>
              <p>{pageNumber}/{numPages}</p>
            </div>
            <motion.button whileHover={{ ...scaleUp }} className={styles.Arrow} onClick={nextPageHandler}>&#8594;</motion.button>        
          </div>  
      </div>

      {
        showComments &&
        <div className={styles.commentsWrapper}>
          <Comments />        
        </div>

      }   
      <div className={styles.navAndComments}>
        <div className={styles.navigateBooks}>
          <motion.button whileHover={{ ...scaleUp }} whileTap={{ ...scaleDown }} onClick={BookChangePrevious} className={styles.navigateBooksButton} >
          <div className={styles.upArrow}>
            <Image src="/static/upArrow.svg" width={50} height={50} alt="upArrow" />
          </div>
          </motion.button>            
          <motion.button whileHover={{ ...scaleUp }} whileTap={{ ...scaleDown }} className={styles.navigateBooksButton} onClick={BookChangeNext}>
          <div className={styles.downArrow}>
            <Image src="/static/downArrow.svg" width={50} height={50} alt="downArrow" />
          </div>
          </motion.button>
        </div>   
         
        <div className={styles.commentsIconWrapper}>
          
          <Image src="/static/CommentsIcon.png" onClick={handleShowComments} width="100%" height="20%"  layout="responsive"  objectFit="contain" alt="Show Comments Icon" />
          <p>{commentCount}</p>
      </div>  
      
      
      </div>            
        </div>

      
      </div>    
  
    </div>
    
  );

}


export default PDFViewer;