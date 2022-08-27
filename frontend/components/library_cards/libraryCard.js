import { useState, useEffect } from "react";

import Image from 'next/image'

import { Document, Page, pdfjs } from "react-pdf";
import workerSrc from "../../pdf-worker";

import styles from './libraryCard.module.css'

import { motion } from "framer-motion";

pdfjs.GlobalWorkerOptions.workerSrc = workerSrc;

const LibraryCard = (props) => { 

  const {filePath="/static/thumbnails/Big_O_Notation.png", title} = props

  return (
    <div className={styles.container}>
        <div className={styles.booksContainer}>
          <h3 className={styles.bookName}>{title}</h3>
                <motion.div initial={{ opacity: 0, scale: 0.5 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.5, delay: 0.5, ease: [0, 0.71, 0.2, 1.01]}} className={styles.pageWrapper}>
                  <img className={styles.bookThumbnail} src={filePath} />                          
                </motion.div>        
        </div>      
    </div>

      
  )
}

export default LibraryCard;