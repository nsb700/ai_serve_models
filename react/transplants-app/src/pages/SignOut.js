import { discardToken, fetchToken, isLoggedIn } from "./Auth";

function SignOut() {
    const is_logged_in = isLoggedIn()

    const handleSignOut = async (event) => {
        event.preventDefault();
        try {
            discardToken()
            console.log(fetchToken())
            alert('Sign out successful');
        } catch (error) {
            alert('Sign out failed'); 
        }
      };

    return ( 
        <>
            {is_logged_in ? (
                <form className='card' onSubmit={handleSignOut}>
                    <button type="submit">*** Are you sure about signing out ? ***</button>
                </form>     
                ): (
                <h2>You are already logged out.</h2>          
            )
            } 
        </>
     );
}

export default SignOut;