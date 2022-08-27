import Navbar from '../components/navbar/navbar'
import styles from './../styles/signup.module.css'

const signUp = () => {
    return (
        <div>
            <Navbar />
            <h1 className={styles.header}>Sign Up</h1>
            <form>
                <label>Username</label>
                <input className={styles.username}/>
                <label>Email</label>
                <input className={styles.email}/>
                <label>Password</label>
                <input className={styles.password}/>
                <label>Confrim Password</label>
                <input className={styles.confirm}/>
            </form>
        </div>
    )
}

export default signUp;