import Navbar from "../components/navbar/navbar";
import styles from "../styles/Home.module.css"

import {useRouter} from 'next/router'
import {useState, useEffect} from 'react'

export default function PDF() {
  const router = useRouter()
  const [calledPush, setCalledPush] = useState(true);

  useEffect(() => {
    if (calledPush) {
          router.push('/explore/explore/book/book?title=xHEP') 
          setCalledPush(false)
    } else {
      return
    }

  }, [])
}
 