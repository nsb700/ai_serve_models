import './App.css';
import { BrowserRouter, Link, Route, Routes } from 'react-router-dom';
import Home from './pages/Home.js'
import Register from './pages/Register.js'
import Login from './pages/Login.js'
import Summarize from './pages/Summarize.js'
import SignOut from './pages/SignOut.js';
import TransplantDiagRelation from './pages/TransplantDiagRelation.js';
import { RequireToken } from './pages/Auth.js';

function App() {
  return (
    <>
      <BrowserRouter>

      <nav className='flex'>

      <div id="nav-options">
        <span>
          <Link to='/'>Home</Link>
        </span>
        
        <span>
          <Link to='/register'>Register</Link>
        </span>

        <span>
          <Link to='/login'>Login</Link>
        </span>

        <span>
          <Link to='/signout'>Sign out</Link>
        </span>

        <span>
          <Link to='/summarize'>AI (Text Summarization)</Link>
        </span>

        <span>
          <Link to='/transplantdiagrelation'>AI (Transplant Bundle)</Link>
        </span>

      </div>

      </nav>

      <div className='flex header'>
      <div className="application-info">
        <h1>Artificial Intelligence for <br/>Text Summarization and Transplant Bundle</h1>
      </div>

      <div className="ai-pic">
        <img src="https://cdn.pixabay.com/photo/2021/11/04/06/27/artificial-intelligence-6767502_960_720.jpg" alt ="" className="img-responsive img-circle"/>
      </div>
      </div>


      <br></br>
        <Routes>

          <Route 
            path='/' 
            element={<Home/>} 
          />
          
          <Route 
            path='/register' 
            element={<Register/>} 
          />
          
          <Route 
            path='/login' 
            element={<Login/>} 
          />

          <Route 
            path='/signout' 
              element={
                  <SignOut/>
              }
          />

          <Route 
            path='/summarize' 
              element={
                <RequireToken>  
                  <Summarize/>
                </RequireToken>
              }
          />

          <Route 
            path='/transplantdiagrelation' 
              element={
                <RequireToken>  
                  <TransplantDiagRelation/>
                </RequireToken>
              }
          />

          <Route 
            path='*' 
            element={<h1>404 - Page Not Found</h1>} 
            />

        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
