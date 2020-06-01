import React from 'react';
import logo from './logo.svg';
import './App.css';
import Nav from './Nav';
import Shop from './Shop';
import About from './About';
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';
import ItemDetail from './itemDetail';

function App() {
  return (
    <Router>
    <div className="App">
      <Nav />
      <Switch>
      <Route path='/' exact component={Home} />
      <Route path='/about' component={About}/>
      <Route path='/shop' exact component={Shop} />
      <Route path='/shop/:id' component={ItemDetail}/>
      </Switch>
    </div>
    </Router>
  );
}


const Home = () => {
  return(
    <div>
      <h1>Home page</h1>
    </div>
  )
}



export default App;
