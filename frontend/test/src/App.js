import logo from './logo.svg';
import './App.css';

function App() {
  const fetch_log = async() => {
    const res = await fetch('http://127.0.0.1:8000/api/room/log')
    const data = await res.json()
    console.log(data)
    return data
  }
  return (
    <div className="App">
      <button className='btn' onClick={() => fetch_log()}> click </button>
    </div>
  );
}

export default App;
