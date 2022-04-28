import Header from './components/Header.js';
import Main from './components/Main.js';
import Alert from './components/Alert.js';
import {useEffect, useState} from 'react'

function App() {
  const max_pp = 5;
  // const [current_pp, setCurrent_pp] = useState(0);
  var current_pp = 0;
  const [full, setFull] = useState(false);

  const fetch_log = async() => {
    const res = await fetch('http://127.0.0.1:8000/api/report/day/current')
    const data = await res.json()
    return data
  }
  
  function closeModal(){
    current_pp = 0;
    setFull(false);
  }
  
  return (
    <div className="container">
      <Header/>
      <Main fetch_log={fetch_log}/>
      {/* {full ? 
        (<Alert closeModal={closeModal}/>)
      : null} */}
    </div>
  );
}

export default App;


