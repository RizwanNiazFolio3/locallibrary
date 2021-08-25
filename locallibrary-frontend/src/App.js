import logo from './logo.svg';
import './App.css';
import Navbar from './components/Navbar'
import {BrowserRouter as Router, Route, Switch} from 'react-router-dom';

function App() {
  return (
    <Router>
      <div>
        <Navbar/>
      </div>
    </Router>

  );
}

export default App;
