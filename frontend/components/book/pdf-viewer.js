import { useState, useEffect } from "react";
import { Document, Page, pdfjs } from "react-pdf";
import workerSrc from "../../pdf-worker";
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
  const [title, setTitle] = useState("")
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
  const elementPos = bookSet.map(function(book) {return book.id; }).indexOf(id)
  setIndex(elementPos)
  bookSet.map(function(book) {
    if (book.id === id) {
      setFile(book.content)
      setOwner(book.owner)
      setTitle(book.title)
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

    const handleDownVote = () => {
      setDownVote(!downVote)
      setUpVote(false)
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
        const pageHeightAlg = 0.62 * h;
        setPageHeight(pageHeightAlg)}, 250)
      debouncedHandleResize()
    }    

  useEffect(()=> {
    const debouncedHandleResize = debounce(function handleResize() {
      const h = window.innerHeight;
      const pageHeightAlg = 0.62 * h;
      setPageHeight(pageHeightAlg)}, 250)

    window.addEventListener('resize', debouncedHandleResize)
    return _ => {
      window.removeEventListener('resize', debouncedHandleResize)
    }
}, [])

  const searchPage = (event) => {
    const inputVal = document.getElementById("setPageNum").value
    if(event.key === "." || event.key === "-"){
      event.preventDefault();
    }
    else if(event.key === 'Enter') {
      if(parseInt(inputVal) > numPages) {
        console.log("no")
        document.getElementById("setPageNum").value = ""
      }else if(parseInt(inputVal) <= 0) {
        console.log("no")
        document.getElementById("setPageNum").value = ""
      }
      else {
          setPageNumber(parseInt(inputVal))        
      } 
      document.getElementById("setPageNum").value = ""
    }
  }

  function nFormatter(num, digits) {
    const lookup = [
      { value: 1, symbol: "" },
      { value: 1e3, symbol: "k" },
      { value: 1e6, symbol: "M" },
      { value: 1e9, symbol: "G" },
    ];
    const rx = /\.0+$|(\.[0-9]*[1-9])0+$/;
    var item = lookup.slice().reverse().find(function(item) {
      return num >= item.value;
    });
    return item ? (num / item.value).toFixed(1).replace(rx, "$1") + item.symbol : "0";
  }

  return (
    <div className={styles.container}>
      <div className={styles.col1}>
      <div className={styles.grid}>
      <div className={styles.bookSummaryContainer}>
      <h1>Book Summary</h1>
      <p>Nisi Lorem eiusmod non excepteur aliquip ullamco nisi qui Lorem veniam quis. Velit nisi deserunt dolor deserunt adipisicing commodo pariatur aliquip eiusmod ullamco laborum officia consectetur dolor. Magna dolor voluptate est adipisicing duis duis do laborum elit. Adipisicing labore aute do officia. Ipsum aute culpa do excepteur laborum consectetur labore sunt nostrud anim. Occaecat amet ullamco culpa nisi Lorem pariatur in voluptate.Incididunt nostrud esse exercitation qui magna incididunt consectetur tempor id nulla do voluptate. Laborum laborum ut aliqua dolor culpa aute mollit veniam officia veniam reprehenderit nostrud anim consequat. Esse pariatur cillum laborum irure duis dolore sint pariatur sit fugiat. Culpa pariatur tempor excepteur velit magna excepteur. Veniam velit ipsum dolore occaecat elit duis pariatur minim ullamco magna ipsum in. Minim ex aute elit quis ad mollit incididunt reprehenderit. Sunt proident fugiat sunt aute et proident proident nisi in dolor cupidatat.</p>
      </div> 
        <div className={styles.votingButtons}>
          <h3>{nFormatter(upVotes, 2)}</h3>            
          <div className={upVote ? styles.Voted: styles.Vote} onClick={handleUpVote}>
          <Image src="/static/spearUp.svg" width={20} height={20} alt="upVote" />      
          </div>
          <h3>{nFormatter(downVotes, 2)}</h3>             
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
              <p><input className={styles.setPageNum} type="number" min={0}
              id="setPageNum" onKeyDown={searchPage} placeholder={pageNumber}/>/{numPages}</p>
            </div>
            <motion.button whileHover={{ ...scaleUp }} className={styles.Arrow} onClick={nextPageHandler}>&#8594;</motion.button>        
          </div>  
      </div>

      {
        showComments &&
        <div className={styles.commentsWrapper}>
          <Comments bookName={title} owner={owner} />        
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