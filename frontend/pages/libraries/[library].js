import {useState, useEffect, useRef} from 'react';
import Navbar from '../../components/navbar/navbar'
import Image from 'next/image';
import styles from '../../styles/library.module.css'
import LibraryCard from '../../components/library/libraryCard'
import { useRouter } from 'next/router'
import Blur from 'react-blur';
import files from '../../data/files.json'
import banner from '../../data/trending_libraries.json'
import LibraryChat from '../../components/libraryChat/libraryChat';

const Library = ({chats}) => {
    const router = useRouter()

    const [filteredBooks, setFilteredBooks] = useState(files)
    const [books, setBooks] = useState(files)
    const [searchField, setSearchField] = useState('')
    const [showChat, setShowChat] = useState(false)

    const handleShowChat = () => {
        setShowChat(!showChat)
    }

    const handleSearchChange = (event) => {
        setSearchField(event.target.value)
    }
    useEffect(() => {
        setFilteredBooks(books.filter(book =>
        book.title.toLowerCase().includes(searchField.toLowerCase())
    ))
    }, [books, searchField])

    

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
                    
                   {/*<div className={styles.expand}>
                        <Image  src='/static/CommentsIcon.png' onClick={handleShowChat} alt='Library Chat' width={20} height={20} />
                    </div> */}
                   
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
            
            {/*{
                showChat &&
            <div className={styles.chatWrapper}>
                <LibraryChat chats={chats} libraryName={router.query.library} closeChat={setShowChat} />
            </div>                
            } */}


        </div>
            </Blur>
    )
}

export async function getServerSideProps() {
    const url = "http://localhost:3000/api/chats"
    const res = await fetch(url);
    const chats = await res.json();
    console.log(chats)
    return { props: {chats} }
  }

export default Library