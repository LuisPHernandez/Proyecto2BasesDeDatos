import HomeImage from '../../assets/HomeImage.jpg';
import styles from "./Home.module.css";

function Home() {
    return (
        <div>
            <h1>Supermercados El Edificio</h1>
            <p className={styles.p}>¡Los mejores productos a los mejores precios!</p>
            <img src={HomeImage} alt="Logo" />
        </div>
    )
}

export default Home