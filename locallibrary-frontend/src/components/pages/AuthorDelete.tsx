import React, { 
    ReactElement,
    useState,
    useEffect,
} from 'react';
import {
    useParams
} from 'react-router-dom';
import axiosInstance from '../../axios'

interface Props {
    firstName?: string,
    lastName?: string,
    dateOfBirth?: string,
    dateOfDeath?:string
}

function AuthorDelete({firstName,lastName}: Props): ReactElement {
    let {id}:{id: string} = useParams();
    const [wasDeleted, setWasDeleted] = useState<boolean>(false)

    useEffect(() => {


    })

    function handleClick()
    {
        axiosInstance.delete('/catalog/api/authors/' + id + "/")
        .then(
            (response) => {
                setWasDeleted(true)
            } 
        )
    }
    function SuccessMessage()
    {
        return(
            <p>The Author was successfully deleted</p>
        )
    }
    return (
        <div>
            <h1>DELETE Author with ID = {id} ?</h1>
            <button onClick = {handleClick}>Delete</button>
            {wasDeleted === false? null: SuccessMessage}
        </div>
    )
}

export default AuthorDelete
