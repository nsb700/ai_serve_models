import axios from "axios";
import { fetchToken } from "./Auth";
import { useState } from "react";
import { config } from './Constants';

function TransplantDiagRelation() {

    const [prompt, setPrompt] = useState('A patient had a {transplant_param} transplant and within 90 days the patient was diagnosed with - {complication_param}. Classify if this diagnosis is related to the transplant. It should be a binary classification with labels as : Related or Unrelated. Along with the classification label, I also want following two details : - Detailed medical explanation for why the diagnosis is classified in that classification. -What is the probability of this diagnosis occurring within 90 days after the transplant. This should only be a percentage value between 0-100%.')
    const [transplant_organ, setTransplantOrgan] = useState('kidney');
    const [diag_description, setDiagDescription] = useState('Other iron deficiency anemias');
    const [response_data, setResponseData] = useState({})
    const URL = config.url;
    const the_token = fetchToken();

    const handleTransplantDiagRelation = async(event) => {
        event.preventDefault();
        try {
            let resp = await axios.post(`${URL}/transplantdiagrelation`, {"prompt_template": prompt, "transplant_organ": transplant_organ, "diagnosis_description": diag_description}, { 
                headers: {
                    Accept: "application/json",
                    Authorization: `Bearer ${the_token}` ,
                },
            });
            setResponseData(resp.data)
        } catch (error) {
            alert("OpenAI call failed"); 
        }
    };

    // const handleClearFields = async (event) => {
    //     event.preventDefault();
    //     setTransplantOrgan('');
    //     setDiagDescription('');
    // };

    return ( 
        <div className='flex flex-center'>
            <br/><br/>
            <form className='card' onSubmit={handleTransplantDiagRelation}>
                <label>Prompt:</label>
                <textarea 
                    class="resizable-textbox"
                    type="text"
                    value={prompt}
                    minlength="100"
                    onChange={(e) => setPrompt(e.target.value)} 
                    required
                />
                <br/>
                <label>Transplant organ:</label>
                <textarea 
                    class="resizable-textbox"
                    type="text"
                    value={transplant_organ} 
                    minlength="3"
                    onChange={(e) => setTransplantOrgan(e.target.value)} 
                     required
                />
                <br/>
                <label>Diagnosis description:</label>
                <textarea 
                    class="resizable-textbox"
                    type="text"
                    value={diag_description} 
                    minlength="5"
                    onChange={(e) => setDiagDescription(e.target.value)} 
                     required
                />
                <br/>
                <button type="submit">Click to send prompt to OpenAI</button>
                <br/>&nbsp;
                {/* <button type="submit" onClick={handleClearFields}>Clear transplant and diag fields</button> */}

                <button>Response from OpenAI</button>
                <div>
                    <table>
                        <thead>
                            <tr>
                                <th>Classification</th>
                                <th>Probability within 90 days</th>
                                <th>Explanation</th>
                                <th>Prompt tokens</th>
                                <th>Completion tokens</th>
                                <th>Total tokens</th>
                            </tr>
                        </thead>
                        <tbody>
                            {
                                <tr>
                                    <td>{response_data.classification}</td>
                                    <td>{response_data.probability_within_90_days}</td>
                                    <td>{response_data.explanation}</td>
                                    <td>{response_data.prompt_tokens}</td>
                                    <td>{response_data.completion_tokens}</td>
                                    <td>{response_data.total_tokens}</td>
                                </tr>
                            }                         
                        </tbody>
                    </table>
                </div>

            </form>   
        </div>            
     );
}

export default TransplantDiagRelation;