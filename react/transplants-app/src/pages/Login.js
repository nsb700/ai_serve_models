import React, { useState } from 'react';
import axios from 'axios'
import { setToken, isLoggedIn } from "./Auth";
import { useNavigate } from 'react-router-dom';


function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    axios.defaults.baseURL = 'http://localhost:8000';
    const navigate = useNavigate();
    const is_logged_in = isLoggedIn()

    const handleLogin = async (event) => {
        event.preventDefault();
        try {
            const form_data = new FormData()
            form_data.append("username", email)
            form_data.append("password", password)
            await axios
                    .post('/token', 
                    form_data
                ).then(function (response) {
                    if (response.data.access_token) {
                        setToken(response.data.access_token);
                        navigate("/summarize");
                      }
                })
                .catch(function (error) {
                    console.log(error, "error");
                });
            alert('Login successful');
            setEmail('');
            setPassword('');
        } catch (error) {
            alert('Login failed'); 
            setEmail('');
            setPassword('');
        }
      };

    return ( 
        <div className='flex flex-center'>
            <br/><br/>

            {is_logged_in ? (
                <h2>You are logged in and may now use the AI capabilities.</h2>
            ): (
                <div>
                    <form className='card' onSubmit={handleLogin}>
                        <label>Email:</label>
                        <input 
                            type="email"
                            value={email} 
                            placeholder='youremail@domain'
                            onChange={(e) => setEmail(e.target.value)} 
                            required
                        />
                        <br/>
                        <label>Password:</label>
                        <input 
                            type="password" 
                            value={password} 
                            onChange={(e) => setPassword(e.target.value)} 
                            required
                        />
                        <br/>
                        <button type="submit">Login</button>
                    </form>                       
                </div>               
            )
            } 
        </div>        
     );
}

export default Login;