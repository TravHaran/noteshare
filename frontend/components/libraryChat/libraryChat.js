import styles from './libraryChat.module.css'
import Image from 'next/image'
import Chat from './chat/chat'

const LibraryChat = (props) => {

    const {libraryName="Theoretical Physics", closeChat, chats} = props
    console.log(chats)

  return (
    <div className={styles.libraryChatContainer}>
    <div>
        <h2 className={styles.close} onClick={() => closeChat(false)}>X</h2>    
    </div>
        <h1 className={styles.libraryName}>{libraryName}</h1>     
        <div className={styles.chatsContainer}>

        {chats.map(function (item, idx) {
            return (
            <Chat key={idx} name={item.name} content={item.content} />
            )
        })}
        </div>
    <div className={styles.sendMessageContainer}>
        <input className={styles.typingContainer} placeholder="please be kind in the chat :)" />
        <Image src="/static/send_message.svg" alt="send message" width={20} height={10}/>            
    </div>        

    </div>
  )
}

export async function getServerSideProps() {
    const url = "http://localhost:3000/api/chats"
    const res = await fetch(url);
    const chats = await res.json();
    console.log(chats)
    return { 
        props: {chats},
        unstable_revalidate: 1,
     }
  }

export default LibraryChat

