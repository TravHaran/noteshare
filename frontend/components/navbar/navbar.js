import styles from './navbar.module.css';
import Image from 'next/image'
import Login from './login/login'
import SignUp from './signUp/signUp'
import Link from 'next/link'
import {useRouter} from 'next/router';
import {useState} from 'react'
import Modal from 'react-modal';

const Navbar = () => {
    const router = useRouter()
    const [profileClicked, setProfileClicked] = useState(false)
    const [isLoggedIn, setIsLoggedIn] = useState(false)
    const [loginModal, setLoginModal] = useState(false)
    const [registerModal, setRegisterModal] = useState(false)
    const [username, setUsername] = useState('Test User')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    // const [samePass, setSamePass] = useState(false)

    const handleProfileClick = () => {
        setProfileClicked(!profileClicked)
    }

    const handleLoginClick = () => {
        setLoginModal(true) 
        setProfileClicked(false)
    }

    const handleRegisterClick = () => {
        setRegisterModal(true) 
        setProfileClicked(false)
    }

    const handleSubmitLogin = (event) => {
        event.preventDefault()
        const email = document.getElementById('email').value
        const pass = document.getElementById('password').value
        setUsername(email)
        setEmail(email)
        setPassword(pass)
        setIsLoggedIn(true)
        setLoginModal(false)
        console.log(email, pass)
    }
    const handleSubmitSignUp = (event) => {
        event.preventDefault()
        const username = document.getElementById('username').value
        const email = document.getElementById('email').value
        const pass = document.getElementById('password').value
        setUsername(username)
        setEmail(email)
        setPassword(pass)
        setRegisterModal(false)
        setIsLoggedIn(true)
        console.log(email, pass, username)
    }

    const validatePassword = () => {
        const pass = document.getElementById('password')
        const confirmPass = document.getElementById('confirmPassword')
            if(pass.value != confirmPass.value) {
              confirmPass.setCustomValidity("Passwords Don't Match");
            } else {
              confirmPass.setCustomValidity('');
            }
          }

  return (
    <div>
        <div className={styles.container}>
            <div className={styles.navContainer}>
                <Image className={styles.profileIcon} onClick={() => {router.push("/")}} src="/static/Logo Orange.svg" alt="NoteShare Logo" width="100%" height="100%"  layout="responsive"  objectFit="contain" />    
                    <input className={styles.search} placeholder="Search for Libraries and Books" />
                <Image className={styles.profileIcon} onClick={handleProfileClick} alt="Logo Icon" src="/static/profile.svg" width="100%" height="100%"  layout="responsive"  objectFit="contain" />
                
            </div>
            
        </div>
        {
            profileClicked && 
            <div className={styles.profileDropDown}>
            {
                isLoggedIn &&
                <div>
                    <Link href={`/profiles/${username}`}>
                        <p className={styles.dropDownText}>{username}</p>
                    </Link>
                    <p className={styles.dropDownText}>Sign Out</p>
                </div>
            }
            {
                isLoggedIn === false &&
                <div>
                    <div onClick={handleLoginClick}><p className={styles.dropDownText}>Login</p></div>
                    <div onClick={handleRegisterClick}><p className={styles.dropDownText}>Register</p></div>                    
                </div>

            }
            

            
        </div>
        }
        <Modal isOpen={loginModal} 
        closeTimeoutMS={500}
        ariaHideApp={false}
        onRequestClose={() => setLoginModal(false)}
                style={
            {
                overlay: {
                    color: '#fff',
                    background: 'rgba( 0, 0, 0, 0.5 )',
                    backdropFilter: 'blur(15px)',
                    zIndex: '900'
                },
                content: {
                    width: '90%',
                    justifyContent: 'center',
                    margin: 'auto',
                    height: "90vh",
                    overflowX: "hidden",
                    color: '#fff',
                    background: 'rgba( 0, 0, 0, 0.45 )',
                    border: 0,
                    borderRadius: '2vw',
                    zIndex: '900'
                    
                }
            }
        }>
            <Login closeLoginModal={setLoginModal} setIsLoggedIn={setIsLoggedIn} setUsername={setUsername}/>
        </Modal>

        <Modal isOpen={registerModal} 
        closeTimeoutMS={500}
        ariaHideApp={false}
        onRequestClose={() => setRegisterModal(false)}                
        style={
            {
                overlay: {
                    color: '#fff',
                    background: 'rgba( 0, 0, 0, 0.5 )',
                    backdropFilter: 'blur(15px)',
                    zIndex: '900'
                },
                content: {
                    width: '90%',
                    justifyContent: 'center',
                    margin: 'auto',
                    height: "90vh",
                    overflowX: "hidden",
                    color: '#fff',
                    background: 'rgba( 0, 0, 0, 0.45 )',
                    border: 0,
                    borderRadius: '2vw',
                    zIndex: '900'
                    
                }
            }
        }>
            <SignUp closeRegisterModal={setRegisterModal} setIsLoggedIn={setIsLoggedIn} setUsername={setUsername} />
        </Modal>
        
        <div className={styles.categoriesWrapper}>
            <div className={styles.navCategories}>
                <div>
                    <h2 className={styles.category} style={router.route === '/explore' ? {fontWeight:600}: {fontWeight:200}}>
                        <Link href={"/explore"} >
                            Explore
                        </Link>
                    </h2>
                </div>
                    <hr className={styles.hr} />
                <div>
                    <h2 className={styles.category} style={router.route === '/libraries' ? {fontWeight:600}: {fontWeight:200}}>
                        <Link href={"/libraries"} >
                            Libraries  
                        </Link>  
                    </h2>  
                </div>           
            </div>
        </div>
    </div>

  )
}

export default Navbar