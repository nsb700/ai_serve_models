import React, { useState } from 'react';
import axios from 'axios'
import { isLoggedIn } from './Auth';
import { config } from './Constants';

function Register() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const URL = config.url;
    const is_logged_in = isLoggedIn()
    
    const handleRegister = async (event) => {
        event.preventDefault();
        try {
            await axios.post(`${URL}/register`, {"email": email, "password": password});
            alert('Registration successful');
            setEmail('');
            setPassword('');
        } catch (error) {
            alert('Registration failed'); 
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
                <form className='card' onSubmit={handleRegister}>
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
                    <button type="submit">Register</button>
                </form>             
            )
            } 
        </div>
     );
}

export default Register;