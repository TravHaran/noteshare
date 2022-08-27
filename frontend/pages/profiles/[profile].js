import {useState, useEffect} from 'react'

import Navbar from "../../components/navbar/navbar"

import Image from 'next/image'

import styles from '../../styles/profile.module.css'

import files from '../../data/files.json'

import LibraryCard from '../../components/library/libraryCard'


const profile = () => {
  const [IslikedBooks, setIsLikedBooks] = useState(false)
  const [filteredLikedBooks, setFilteredLikedBooks] = useState([])
  const [likedBooks, setLikedBooks] = useState(files)
  const [searchField, setSearchField] = useState('')

  useEffect(() => {
    const getUserData = () => {

    }
  }, [])

  const handleSearchChange = (event) => {
    setSearchField(event.target.value)
    
}

  useEffect(() => {
    setFilteredLikedBooks(likedBooks.filter(book =>
    book.title.toLowerCase().includes(searchField.toLowerCase())
))
}, [searchField])

  return (
    <div className={styles.container}>
        <Navbar />
        <div className={styles.textContainer}>
          
          <div className={styles.logoAndText}>
            <div className={styles.text}>
              <div className={styles.iconAndHeader}>
                  <Image src="/static/Profile.svg" className={styles.profileIcon} width={100} height={100} />
                  <h1>Francis B.</h1>  
              </div>

              <div className={styles.Followers}>            
                <div className={styles.follow}>
                  <h3>2.7K</h3>
                  <h3>12</h3> 
                  <p>Followers</p>
                  <p>Following </p>         
                </div>
              </div>
            </div>
          </div>

        </div>
        <div className={styles.likedBooksContainer}>
          <h1>My Liked Books</h1>
          <input onChange={handleSearchChange} type="text" className={styles.searchBooks} placeholder="Search for books"/>

          <div className={styles.likedBooks}>
          {
            filteredLikedBooks.map((book, idx) => {
              return (
              <div className={styles.bookContainer} key={idx}>
                <LibraryCard  filePath={book.thumbnail} title={book.title} upVotes={book.upVotes} downVotes={book.downVotes} />
              </div>
              )
              
            })
          } 
          </div>

          
        </div>
    </div>
  )
}

export default profile