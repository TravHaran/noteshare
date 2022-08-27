import Navbar from "../../../../components/navbar/navbar";
import styles from "../../../../styles/Home.module.css"

import libraryFiles from '../../../../data/libraryFiles.json'

import files from '../../../../data/files.json'

import dynamic from 'next/dynamic'


import PDFViewer from "../../../../components/book/pdf-viewer"

import {useEffect} from 'react'

import {useRouter} from 'next/router'


export default function Book() {

  const router = useRouter()

  useEffect(() => {
    router.beforePopState(({ as }) => {
        if (as !== router.asPath) {
            router.push("/libraries")
        }
        return true;
    });

    return () => {
        router.beforePopState(() => true);
    };
}, [router]);

  return (
    
    <div className={styles.container}>
      <Navbar />
     
      <div className={styles.content} >
            <PDFViewer bookSet={files} />
      </div>
    </div>
    )
}
