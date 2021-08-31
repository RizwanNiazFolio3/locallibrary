import logo from './logo.svg';
import './App.css';
import Navbar from './components/Navbar';
import Authors from "./components/pages/Authors";
import Home from "./components/pages/Home";
import Login from "./components/pages/Login"
import {BrowserRouter as Router, Route, Switch} from 'react-router-dom';

function App() {
  return (
    /**
     * This section of the code uses the react router to allow the user to navigate to different pages
     */
    <Router>
      <div>
        {/* The nav bar should be displayed on all the pages */}
        <Navbar/>
        <Switch>
          {/* The relative URL for the home page */}
          <Route exact path = "/">
            <Home />
          </Route>
          {/* Relative URL for the authors list page */}
          <Route path = "/authors">
            <Authors />
          </Route>
          <Route path = "/Login">
            <Login />
          </Route>
        </Switch>
      </div>
    </Router>

  );
}

export default App;
