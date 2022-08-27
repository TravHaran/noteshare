import Navbar from '../components/navbar/navbar'
import SectionCards from '../components/library_cards/sectionCards/SectionCards'
import TrendingLibraries from '../components/trending_libraries/trending_libraries'
import trending_libraries from '../data/trending_libraries.json'
import libraries from '../data/trending_libraries.json'

import files from '../data/files.json'
import styles from '../styles/explore.module.css'

const Libraries = () => {
  return (
    <div className={styles.container}>

      <Navbar />
     

      <TrendingLibraries libraries={trending_libraries} />

      {
        files.map((library, idx) => [
          <SectionCards key={idx} books={files} library={library.library} banner={libraries[idx].thumbnail}/>          
        ])
      }

    </div>
  )
}

export default Libraries;