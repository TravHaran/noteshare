import {useState, useEffect} from 'react';
import Navbar from '../../components/navbar/navbar'
import Image from 'next/image';
import styles from '../../styles/library.module.css'
import LibraryCard from '../../components/library/libraryCard'
import Router, { useRouter } from 'next/router'
import Link from 'next/link';
import Blur from 'react-blur';
import files from '../../data/files.json'
import banner from '../../data/trending_libraries.json'

const Library = () => {
    const router = useRouter()

    const [filteredBooks, setFilteredBooks] = useState(files)
    const [books, setBooks] = useState(files)
    const [searchField, setSearchField] = useState('')
    const handleSearchChange = (event) => {
        setSearchField(event.target.value)
        
    }
    useEffect(() => {
        setFilteredBooks(books.filter(book =>
        book.title.toLowerCase().includes(searchField.toLowerCase())
    ))
    }, [searchField])

    

    const libraryStyle = {
        background:`url('${banner[7].thumbnail}')`,
        width: '100vw',
        backgroundPosition: 'center',
        MozBackgroundSize: "cover",
        backgroundSize: "cover",
        backgroundRepeat: "no-repeat",
    }

    

    return (
    <Blur img={banner[6].thumbnail}  blurRadius={50} shouldResize enableStyles style={{overflow: 'hidden'}}>        
        <div>
            <Navbar /> 

            <div className={styles.container}>
                <div className={styles.titleText}>
                                   
                   <div className={styles.description}>
                        <h1>Welcome to {router.query.library}</h1> 
                        
                   </div>
                                 
                   <p className={styles.libraryDescription}>Eiusmod elit quis dolore ea voluptate incididunt sint Lorem nostrud id cupidatat commodo elit. Amet aliqua ea esse magna ad quis qui veniam duis laboris eu consectetur nulla ea. Qui id et sint anim sit qui non officia ad qui magna. Adipisicing anim Lorem occaecat eiusmod. Occaecat laborum officia consectetur sunt culpa quis quis.

                    Occaecat fugiat quis ipsum officia amet est sit non aliqua ad. Consectetur eiusmod nisi pariatur et dolore dolore occaecat culpa fugiat sunt nostrud minim. Nostrud enim excepteur quis nostrud non eiusmod minim. Aliqua ex non voluptate adipisicing incididunt laborum cupidatat cupidatat amet minim reprehenderit.
                    </p>
                    <input onChange={handleSearchChange} type="text" className={styles.searchBooks} placeholder="Search for books"/>
                    
                   <div className={styles.expand}>
                    <Image  src='/static/downArrow.svg' width={50} height={50} />
                   </div>
                   
                </div>
                
                <div className={styles.bookContainer}>
                    {
                        filteredBooks.map((book, idx) => {
                            return (
                                    <LibraryCard id={book.id} key={idx} filePath={book.thumbnail} library={book.actualLibrary} title={book.title} downVotes={book.downVotes} upVotes={book.upVotes}/>
                                
                            )
                        })
                    }                
                </div>
            </div>            
           

        </div>
            </Blur>
    )
}

export default Library