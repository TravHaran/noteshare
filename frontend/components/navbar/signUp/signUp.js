import {useState} from 'react'

const SignUp = (props) => {

    const {closeRegisterModal, setIsLoggedIn, setUsername} = props

    const handleSubmitSignUp = (event) => {
        event.preventDefault()
        const username = document.getElementById('username').value
        const email = document.getElementById('email').value
        const pass = document.getElementById('password').value
        setUsername(username)
        setEmail(email)
        setPassword(pass)
        closeRegisterModal(false)
        setIsLoggedIn(true)
        console.log(email, pass, username)
    }

  return (
    <div className={styles.signUpContainer}>
    <h1 className={styles.header}>Join The Community</h1>
    <form className={styles.signUpForm} onSubmit={handleSubmitSignUp} id="signUpForm">
        <label className={styles.signUpLabels}>Username</label>
        <input className={styles.SignUpUsername} id="username" required/>
        <label className={styles.signUpLabels}>Email</label>
        <input className={styles.SignUpEmail} type="email" id="email" required/>
        <label className={styles.signUpLabels}>Password</label>
        <input className={styles.SignUpPassword} type="password" onChange={validatePassword} id="password" required/>
        <label className={styles.signUpLabels}>Confirm Password</label>
        <input className={styles.SignUpConfirm} type="password" onChange={validatePassword} id="confirmPassword" required/>
    </form>
        <button type="submit" form="signUpForm" className={styles.SignUpSubmit}>Sign Up</button>
</div>
  )
}

export default SignUp