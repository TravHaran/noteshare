import {useState} from 'react'
import styles from './login.module.css'

const Login = (props) => {

    const {closeLoginModal, setIsLoggedIn, setUsername} = props

    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')


    const handleSubmitLogin = (event) => {
        event.preventDefault()
        const email = document.getElementById('email').value
        const pass = document.getElementById('password').value
        setUsername(email)
        setEmail(email)
        setPassword(pass)
        setIsLoggedIn(true)
        closeLoginModal(false)
        console.log(email, pass)
    }

  return (
    <div className={styles.loginContainer}>
    <h1 className={styles.loginHeader}>Welcome Back!</h1>
    <form className={styles.loginForm} id="login" onSubmit={handleSubmitLogin}> 
        <label className={styles.loginLabels} >Email</label>
        <input type="email" className={styles.email} id="email" required/>
        <label className={styles.loginLabels} >Password</label>
        <input type="text" className={styles.password} id="password" required/>
        
    </form>
    <button type="submit" form="login" className={styles.loginSubmit}>Login</button>
</div>
  )
}

export default Login