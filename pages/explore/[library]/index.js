import Navbar from "../../../components/navbar/navbar";
import styles from "../../../styles/Home.module.css"

import libraryFiles from '../../../data/libraryFiles.json'

import dynamic from 'next/dynamic'

import PDFViewer from "../../../components/book/pdf-viewer"


export default function PDF() {
  return (
    
    <div className={styles.container}>
      <Navbar />
     
      <div className={styles.content} >
            <PDFViewer bookSet={libraryFiles}/>
      </div>
    </div>
    )
}
