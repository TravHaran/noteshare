import Navbar from "../../../../components/navbar/navbar";
import styles from "../../../../styles/Home.module.css"

import libraryFiles from '../../../../data/libraryFiles.json'

import files from '../../../../data/files.json'

import dynamic from 'next/dynamic'


import PDFViewer from "../../../../components/book/pdf-viewer"

import {useEffect} from 'react'

import {useRouter} from 'next/router'


const Book = (books) => {

  const router = useRouter()

  console.log(books)


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

// export async function getServerSideProps() {
//   const url = "https://noteshare.live/api/books"
//   console.log(url)
//   const res = await fetch(url);
//   const dataExport = await res.json();
//   console.log(dataExport)
//   return { props: {dataExport} }
// }

  var myHeaders = new Headers();
  myHeaders.append("Authorization", process.env.JWT_TOKEN);
  var requestOptions = {
    method: 'GET',
    headers: myHeaders,
    redirect: 'follow'
  };

export async function getServerSideProps() {
    const res = await fetch('https://noteshare.live/api/books/', requestOptions)
     const books = await res.json()
     console.log(books);
  
    return { props: {books} }
}

export default Book;