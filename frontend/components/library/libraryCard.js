import styles from './libraryCard.module.css'
import Image from 'next/image'
import {motion} from 'framer-motion'
import Router, { useRouter } from 'next/router'
import Link from 'next/link'

const LibraryCard = (props) => {

    const router = useRouter()

    const {filePath="/static/thumbnails/Big_O_Notation.png", library='explore', id=0, title, downVotes=0, upVotes=0} = props

    function nFormatter(num, digits) {
        const lookup = [
          { value: 1, symbol: "" },
          { value: 1e3, symbol: "k" },
          { value: 1e6, symbol: "M" },
          { value: 1e9, symbol: "G" },
        ];
        const rx = /\.0+$|(\.[0-9]*[1-9])0+$/;
        var item = lookup.slice().reverse().find(function(item) {
          return num >= item.value;
        });
        return item ? (num / item.value).toFixed(1).replace(rx, "$1") + item.symbol : "0";
      }

    const scaleUp = {scale: 1.01};
    const scaleDown = {scale: 1}


  return (
    <div className={styles.container}>
        <Link href={`/explore/${library}/book/book?title=${id}`}>
                <motion.div  className={styles.booksContainer} whileHover={{ ...scaleUp }} whileTap={{ ...scaleDown }}>
            <h3 className={styles.bookName}>{title}</h3>
            <div className={styles.pageWrapper}>
                <img className={styles.bookThumbnail} src={filePath} />                      
            </div>    
            <div className={styles.detailsWrapper}>
                <div className={styles.Vote}>
                    <div className={styles.Vote2}>
                        <Image src="/static/spearUp.svg" width={40} height={40} alt="upVote" /> 
                        <h3 className={styles.detailNums}>{nFormatter(upVotes, 2)}</h3>      
                    </div>      
                    
                    <div className={styles.Vote1}>
                        <Image src="/static/spearDown.svg" width={40} height={40} alt="downVote" /> 
                        <h3 className={styles.detailNums}>{nFormatter(downVotes, 2)}</h3> 
                    </div>         
                    </div>
                </div>      
            </motion.div>    
        </Link>
    
    </div>

  )
}

export default LibraryCard