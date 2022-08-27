import Navbar from '../components/navbar/navbar'
import styles from '../styles/login.module.css'
import Blur from "react-blur"

const login = () => {
    return (

        <div className={styles.container}>
            <Navbar />
            <div className={styles.loginContainer}>
                <h1 className={styles.header}>Welcome Back!</h1>
                <form className={styles.form}> 
                    <label className={styles.loginLabels}>Email</label>
                    <input type="email" className={styles.email}/>
                    <label className={styles.loginLabels}>Password</label>
                    <input type="text" className={styles.password}/>
                    
                </form>
                <button className={styles.submit}>Login</button>
            </div>
            
        </div>
    )
}

export default login;