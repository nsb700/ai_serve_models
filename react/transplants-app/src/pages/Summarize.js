import React, { useState } from 'react';
import axios from 'axios'
import { fetchToken } from "./Auth";
import { config } from './Constants';

function Summarize() {
    
    const [text_to_summarize, setTextToSummarize] = useState('');
    const URL = config.url;
    const the_token = fetchToken();
    const [summarized_text, setSummarizedText] = useState(''); 

    const handleSummarize = async (event) => {
        event.preventDefault();
        try {
            let resp = await axios.post(`${URL}/summarize`, {"text": text_to_summarize}, { 
                headers: {
                    Accept: "application/json",
                    Authorization: `Bearer ${the_token}` ,
                },
            });
            setSummarizedText(resp.data.model_output_text)
        } catch (error) {
            alert("Summarization failed"); 
        }
      };

    const handleClearFields = async (event) => {
        event.preventDefault();
        setTextToSummarize('');
        setSummarizedText('');
    };

    return ( 
        <div className='flex flex-center'>
            <br/><br/>
            <form className='card' onSubmit={handleSummarize}>
                <label>Input text to summarize:</label>
                <textarea 
                    class="resizable-textbox"
                    type="text"
                    value={text_to_summarize} 
                    minlength="20"
                    placeholder='Enter your text here'
                    onChange={(e) => setTextToSummarize(e.target.value)} 
                     required
                />
                <br/>
                <button type="submit">Click to Summarize</button>
                <br/>&nbsp;
                <button type="submit" onClick={handleClearFields}>Clear all fields</button>
                <textarea
                    class="resizable-textbox"
                    type="text"
                    value={summarized_text} 
                    placeholder='Summarized output text will appear here'
                />
            </form>   
        </div>            
     );
}

export default Summarize;