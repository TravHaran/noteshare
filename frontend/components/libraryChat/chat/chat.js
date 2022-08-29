import styles from './chat.module.css'

const Chat = (props) => {
    const {name, content} = props
  return (
    <div className={styles.chatContainer}>
        <p className={styles.profileAndName}>
            <span className={styles.profile}>
            </span >
            <b className={styles.username}>{name}</b>
        </p> 
        <p>{content}</p>
    </div>
  )
}

export default Chat