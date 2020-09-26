import React from 'react';
import TopBar from "./Components/TopBar/TopBar.jsx"
import Home from "./views/Home.jsx"
import User from "./views/User.jsx"
import Flag from "./views/Flag.jsx"

import {
    HashRouter as Router,
    Switch,
    Route,
} from "react-router-dom";

const homeContainerStyle = {
  display: "flex",
  flexFlow: "column nowrap",
}

const rootContainerStyle = {
  display: "flex",
  width: "100%",
  flex: "1 100%",
  justifyContent:"center",
}

const centeredContainerStyle = {
  display: "flex",
  width:"80%",
  justifyContent:"center",
  flexFlow:"column nowrap",
  paddingTop:"1rem"
}

function App() {
  return (
    <>
      <Router>
        <main style={rootContainerStyle} className={"bp3-dark"}>
          <section style={centeredContainerStyle}>
            <header> 
              <TopBar />
            </header>
            <section style={homeContainerStyle}>
                <Switch>
                  <Route path="/user/:id">
                    <User />
                  </Route>
                  <Route path="/flag">
                    <Flag />
                  </Route>
                  <Route path="/">
                    <Home />
                  </Route>
                </Switch>
            </section>
          </section>
        </main>
      </Router>
    </>
  );
}

export default App;
