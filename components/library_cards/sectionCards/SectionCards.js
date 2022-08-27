import LibraryCard from '../libraryCard'
import {useState} from 'react'
import Link from 'next/link'
import styles from './SectionCards.module.css'
import Modal from 'react-modal'
import {motion} from 'framer-motion'

const SectionCards = (props) => {

    const {books, library, banner} = props;

    const [createBookPopUp, setCreateBookPopUp] = useState(false)

    const libraryStyle = {
        background:`url('${banner}')`,
        width: '100vw',
        backgroundPosition: 'center',
        MozBackgroundSize: "cover",
        backgroundSize: "cover",
        backgroundRepeat: "no-repeat",
    }

    const scaleUp = {scale: 1.1};
    const scaleDown = {scale: 0.95}

    const createBookModal = (e) => {
        e.preventDefault()
        setCreateBookPopUp(true)
    }

    const handleSubmitBook = () => {
        console.log("submited")
    }

    return (
        <div>  
            <Link href={`/libraries/${library}`} >
                <h2 className={styles.libraryName} style={{cursor: 'pointer'}}>{library}</h2>    
            </Link>                     
                  
            <div className={styles.container}  style={libraryStyle}>
                <div >
                    <motion.button onClick={createBookModal} className={styles.add} whileHover={{ ...scaleUp }} whileTap={{ ...scaleDown }}>+</motion.button>                    
                </div>
                <Modal isOpen={createBookPopUp} 
                        closeTimeoutMS={500}
                        onRequestClose={() => setCreateBookPopUp(false)}
                        ariaHideApp={false}
                        style={
                            {
                                overlay: {
                                    color: '#fff',
                                    background: 'rgba( 0, 0, 0, 0.5 )',
                                    backdropFilter: 'blur(15px)',
                                    zIndex: '900'
                                },
                                content: {
                                    width: '90%',
                                    justifyContent: 'center',
                                    margin: 'auto',
                                    height: "90vh",
                                    overflowX: "hidden",
                                    color: '#fff',
                                    background: 'rgba( 0, 0, 0, 0.45 )',
                                    border: 0,
                                    borderRadius: '2vw',
                                    zIndex: '900'
                                    
                                }
                            }
                        }    
                >
                    <form className={styles.formContainer} onSubmit={handleSubmitBook}>
                        <h1>Create a Book</h1>
                        <label>Title</label>
                        <input className={styles.input} placeholder="Type Here" />
                        <label>Description</label>
                        <input className={styles.input} placeholder="Type Here" />
                        <input className={styles.input} type="file" multiple />
                        <motion.button type="submit" className={styles.submitButton}>Create Book</motion.button>
                    </form>
                </Modal>

                <div className={styles.cardsWrapper}>
                    
                    {
                        books.map((book, idx) => {
                            return (
                                <Link href={`/explore/${book.actualLibrary}/book/book?title=${book.id}`} key={idx}>
                                    <motion.div className={styles.cardWrapper} initial={{ opacity: 0, scale: 0.5 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.5, delay: 0.5, ease: [0, 0.71, 0.2, 1.01]}}>
                                            <LibraryCard id={idx} filePath={book.thumbnail} title={book.title} /> 
                                                            
                                    </motion.div>
                                </Link>   
                            )
                        })
                    }
                </div>
            </div>
            
        </div>

    )
}

export default SectionCards;