import styles from './trending_libraries.module.css'
import {useState, useContext} from 'react'
import LibraryCard from './library_cards/LibraryCard'
import CreateLibPopUp from '../CreateLibPopUp/createLib';
import Blur from "react-blur";
import {motion} from 'framer-motion'
import Image from 'next/image'
import Slider from 'react-slick'
import Modal from 'react-modal';
import { NodeNextRequest } from 'next/dist/server/base-http/node';

const TrendingLibraries = (props) => {
    const {libraries=[]} = props
    const [createLib, setCreateLib] = useState(false)
    const [imageIndex, setImageIndex] = useState(0)

    const NextArrow = ({onClick}) => {
        return (
            <div className={styles.arrowNextWrapper} onClick={onClick}>
                <Image className={styles.arrownext} src="/static/arrow_forward.svg" width="50%" height="50%" />
            </div>            
        )

    }
    const PrevArrow = ({onClick}) => {
        return (
            <div className={styles.arrowBackWrapper} onClick={onClick} >
                <Image className={styles.arrowBack} src="/static/arrow_back.svg" width="50%" height="50%" />
            </div>            
        )

    }

    const handleCreateLib = () => {
        setCreateLib(!createLib)
    }

    const scaleUp = {scale: 1.1};
    const scaleDown = {scale: 0.95}
    
 

    const settings = {
        dots: true,
        infinite:true,
        lazyLoad: true,
        speed: 400,
        slidesToShow:3,
        centerMode: true,
        centerPadding: 0,
        nextArrow: <NextArrow />,
        prevArrow: <PrevArrow />,
        initialSlide: 0,
        beforeChange: (current, next) => setImageIndex(next),
        afterChange: current => setImageIndex(current)
    }

    const backgroundImage = libraries[imageIndex].thumbnail

  return (
    <div>
        <div className={styles.background}>                
            <div className={styles.trending}>
                        <h2>Top Libraries</h2>                
            </div>
            <Blur className="blurImage" img={backgroundImage} blurRadius={50} enableStyles shouldResize>       
            
                <div className={styles.container}>


                    <Slider {...settings}>
    
                    {libraries.map((library, idx) => {
                        return (
                        <div className={idx === imageIndex ? 'activeSlide': "slide"} key={idx}>
                        
                            <LibraryCard title={library.library} banner={library.thumbnail} patronCount={library.patrons} />    
                        </div>
                    )})}            
                    </Slider>
                </div>   
                                
            </Blur>  

        </div> 
        <motion.div className={styles.createLibWrapper} onClick={() => setCreateLib(true)} whileHover={{ ...scaleUp }} whileTap={{ ...scaleDown }}>
            
            <h1 className={styles.addLibrary}>
                +
            </h1> 
            <div className={styles.createLibraryWrapper}>
                <h2 className={styles.createLibrary}>Create Library</h2>
            </div>             
        </motion.div>
        
        <Modal 
        isOpen={createLib} 
        ariaHideApp={false}
        closeTimeoutMS={500}
        onRequestClose={() => setCreateLib(false)}
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
        }>
            <CreateLibPopUp closeModal={setCreateLib} />
        </Modal>
                
    </div>



  )
}

export default TrendingLibraries