import HomeImage from '../assets/HomeImage.jpg';

function Home() {
    return (
        <div>
            <h1>Supermercados El Edificio</h1>
            <p>¡Los mejores productos a los mejores precios!</p>
            <img src={HomeImage} alt="Logo" />
        </div>
    )
}

export default Home