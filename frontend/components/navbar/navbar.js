import styles from './navbar.module.css';
import Image from 'next/image'
import Link from 'next/link'

import { Textfit } from 'react-textfit';

const Navbar = () => {
  return (
    <div>
        <div className={styles.container}>
            <div className={styles.wrapper}>
                <a className={styles.LogoLink} >
                    <Image src="/static/Logo Orange.svg" alt="NoteShare Logo" width={70} height={70} />
                </a>
            </div>
            <nav className={styles.navContainer}>
                <div className={styles.searchWrapper} >
                    <input className={styles.search} placeholder="Search for Libraries and Books" />
                </div>
                <div className={styles.navItems}>
                    <div className={styles.notificatioLogo}>

                    </div>
                    <div className={styles.profileIcon} >
                        <Image alt="Logo Icon" src="/static/profile.svg" width={50} height={50} />
                    </div>
                </div>
            </nav>
        </div>
        <div className={styles.categoriesWrapper}>
            <div className={styles.navCategories}>
            <div>
                <h2 className={styles.category}>
                    <Link href={"/"}>
                        Explore                    
                    </Link>
                </h2>
            </div>
                <hr className={styles.hr} />
            <div className={styles.cetegory}>
                <h2 className={styles.category}>
                    <Link href={"/explore"}>
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