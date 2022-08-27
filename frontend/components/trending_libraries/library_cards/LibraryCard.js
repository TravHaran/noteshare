import styles from './LibraryCard.module.css'
import Image from 'next/image'
import {motion} from 'framer-motion'
import Link from 'next/link'

const LibraryCard = (props) => {

    const {title="", banner="static/library_banners/space_banner 1.png", patronCount="40K", visibility} = props

    const libraryStyle = {
        background:` no-repeat center url('${banner}')`,
    }

    const scaleUp = {scale: 1.09};

  return (
    <motion.div className={styles.container} initial={{ opacity: 0, scale: 0.5 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.3, delay: 0.2, ease: [0, 0.71, 0.2, 1.01]}}>
      <Link href={`/libraries/${title}`}>
        <motion.div className={styles.cardContainer} whileHover={{ ...scaleUp }} style={libraryStyle}>
          <Image src={banner} layout="fill" />
          <div className={styles.detailsContainer}>
            <h3>{title}</h3>
            <div className={styles.extraDetails}>
              <img className={styles.patronCountIcon} src="/static/patrons.png"   />
              <h4>{patronCount}</h4>    
            </div>  
          </div>
        </motion.div>
      </Link>
    </motion.div>
  )
}

export default LibraryCard