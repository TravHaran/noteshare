import styles from './comments.module.css';
import comments from '../../data/comments.json'
import Image from 'next/image'

const Comments = (props) => {

  const {bookName, owner} = props

  const handleSendComment = (e) => {
    e.preventDefault()
    console.log("comment sent!")
  }

  return (
    <div className={styles.container}>
      <div className={styles.commentsContainer}>
        <div className={styles.text}>
        <div className={styles.header} >
          <h1>{bookName}</h1>     
        </div>
        <div className={styles.comments}>
        {comments.comments.map((comment, idx) => {
          return (
            <div className={styles.commentSection} key={idx}>
            <div className={styles.profileAndUsername}>
              <div className={styles.profile}></div>
                <div className={styles.accountName} >
                  {comment.name} {comment.name === owner && <p className={styles.creator}><b>&#8226; Creator</b></p>}     
                </div>   
              </div>
              <div className={styles.comment}  >
                <div className={styles.content} >
                  <p>{comment.content}</p>          
                </div>
                <div className={styles.like}>
                  <p >{comment.likes}</p> 
                </div>
              </div>          
            </div>
          )
      })}
        </div>    
            
        </div>
      </div>
      <div className={styles.submitCommentContainer}>
          <form onSubmit={handleSendComment}>
              <input className={styles.typeComment} placeholder="Share your thoughts on the post :)" />
              <button type="submit" className={styles.submitCommentBtn}>
                <Image src="/static/send_message.svg" alt="send commment" width={20} height={20} />
              </button>    
          </form>
        </div>  
    </div>
    
  )
}

export default Comments