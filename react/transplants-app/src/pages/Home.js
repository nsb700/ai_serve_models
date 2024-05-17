import React from 'react';

function Home() {
    return ( 
        <div>
            <h4>
                <br/>
                <b>This application lets one play with two AI models:</b>
                <br/>
                <b>(find these options in the menu above)</b>
                <br/>
                <b>1. AI (Text Summarization) :</b> Text summarization using the HuggingFace summarization pipeline.
                <br/>
                <b>2. AI (Transplant Bundle) :</b> Prompting OpenAI for discerning relationships between organ transplants and diagnoses
                <br/><br/>
                *** Log in is required to use AI capabilities ***
            </h4>
        </div>
     );
}

export default Home;