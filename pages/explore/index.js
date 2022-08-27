import {useEffect} from 'react'

import {useRouter} from 'next/router'

export default function PDF() {
  const router = useRouter()

  useEffect(() => {
    router.push('/explore/explore/book/book?title=xHEP') 
  }, [])
}
