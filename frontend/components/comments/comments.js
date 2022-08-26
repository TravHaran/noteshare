import styles from './comments.module.css';
import comments from '../../data/comments.json'

const Comments = () => {
  return (
    <div className={styles.commentsContainer}>
      <div className={styles.text}>
      <div className={styles.header} >
        <h1>Comments</h1>     
      </div>
      <div className={styles.comments}>
      {comments.comments.map((comment, idx) => {
        return (
          <div className={styles.commentSection} key={comment}>
            <div className={styles.profile}></div>
            <div className={styles.accountName}>{comment.name}</div>
            <div className={styles.comment} >
              <div className={styles.content}>
                <p key={idx}>{comment.content}</p>          
              </div>
              <div className={styles.like}>
                <p key={comment.id}>{comment.likes}</p> 
              </div>
            </div>          
          </div>
        )
    })}
      </div>
 
      </div>
    </div>
  )
}

export default Comments