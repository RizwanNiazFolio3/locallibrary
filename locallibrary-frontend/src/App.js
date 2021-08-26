import logo from './logo.svg';
import './App.css';
import Navbar from './components/Navbar';
import Authors from "./components/pages/Authors";
import Home from "./components/pages/Home";
import {BrowserRouter as Router, Route, Switch} from 'react-router-dom';

function App() {
  return (
    <Router>
      <div>
        <Navbar/>
        <Switch>
          <Route exact path = "/">
            <Home />
          </Route>
          <Route path = "/authors">
            <Authors />
          </Route>
        </Switch>
      </div>
    </Router>

  );
}

export default App;
