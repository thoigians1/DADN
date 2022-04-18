import Header from './components/Header.js';
import Main from './components/Main.js';
import Alert from './components/Alert.js';
import {useEffect, useState} from 'react'

function App() {
  const max_pp = 5;
  // const [current_pp, setCurrent_pp] = useState(0);
  var current_pp = 0;
  const [full, setFull] = useState(false);

  useEffect(() => {
    setInterval(() => {
      if (current_pp >= max_pp){
        current_pp -= 1
        setFull(true);
      }
      else{
        current_pp += 1
        setFull(false);
      }
    }, 1000)
  }, []);

  function closeModal(){
    current_pp = 0;
    setFull(false);
  }
  
  return (
    <div className="container">
      <Header/>
      <Main/>
      {/* {full ? 
        (<Alert closeModal={closeModal}/>)
      : null} */}
    </div>
  );
}

export default App;


