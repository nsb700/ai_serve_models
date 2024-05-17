import { useLocation,Navigate } from "react-router-dom"

export const setToken = (token)=>{

    localStorage.setItem('thistoken', token)
}

export const fetchToken = (token)=>{

    return localStorage.getItem('thistoken')
}

export function RequireToken({children}){

    let auth = fetchToken()
    let location = useLocation()

    if(!auth){

        return <Navigate to='/' state ={{from : location}}/>;
    }

    return children;
}

export const isLoggedIn = () => {
    if(fetchToken()) {
        return true
    }
    return false
}


export const discardToken = () => {
    if(fetchToken()) {
        localStorage.removeItem("thistoken");
    }
}

