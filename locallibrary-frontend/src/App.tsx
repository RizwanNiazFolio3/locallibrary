import './App.css';
import Navbar from './components/Navbar';
import Authors from "./components/pages/Authors";
import Home from "./components/pages/Home";
import Login from "./components/pages/Login"
import AuthorDetails from './components/pages/AuthorDetails';
import {BrowserRouter as Router, Route, Switch} from 'react-router-dom';
import AuthContextProvider from './contexts/AuthContext';
import AuthorDelete from './components/pages/AuthorDelete';
import AuthorUpdate from './components/pages/AuthorUpdate';
import AuthorCreate from './components/pages/AuthorCreate';

function App() {
  return (
    /**
     * This section of the code uses the react router to allow the user to navigate to different pages
     */
    <Router>
      <div>
        {/**The Authorization context provider is passed to all of the components */}
        <AuthContextProvider>
          {/* The nav bar should be displayed on all the pages */}
          <Navbar/>
          <Switch>
            {/* The relative URL for the home page */}
            <Route exact path = "/">
              <Home />
            </Route>
            {/* Relative URL for the authors list page */}
            <Route exact path = "/authors">
              <Authors />
            </Route>
            {/* URL for the Login Page */}
            <Route path = "/Login">
              <Login />
            </Route>
            {/* URL for a specific authors Details page */}
            <Route exact path = "/authors/:id(\d+)">
              <AuthorDetails />
            </Route>
            {/* URL for the deletion page of a specific author */}
            <Route exact path = "/authors/:id(\d+)/delete">
              <AuthorDelete />
            </Route>
            {/* URL for the update page of a specific author */}
            <Route exact path = "/authors/:id(\d+)/update">
              <AuthorUpdate />
            </Route>
            {/* URL for the author Creation page */}
            <Route exact path = "/authors/create">
              <AuthorCreate />
            </Route>
          </Switch>
        </AuthContextProvider>

      </div>
    </Router>

  );
}

export default App;
