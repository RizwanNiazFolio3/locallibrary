import React, { 
    ReactElement,
    useEffect,
    useState,
} from 'react';
import {
    useParams,
    useHistory,
} from 'react-router-dom';
import axiosInstance from '../../axios'

interface Props {

}

function AuthorDelete({}: Props): ReactElement {
    let {id}:{id: string} = useParams();
    const history = useHistory()
    const [firstName,setFirstName] = useState<string>("--Loading--")
    const [lastName,setLastName] = useState<string>("--Loading--")

    useEffect(() =>{
        axiosInstance.get('/catalog/api/authors/' + id + "/")
        .then(response => {
            setFirstName(response.data.first_name)
            setLastName(response.data.last_name)
        })
    },[id])

    function handleClick()
    {
        axiosInstance.delete('/catalog/api/authors/' + id + "/")
        .then(
            (response) => {
                history.push('/authors')
            } 
        )
    }

    return (
        <div>
            <h1>DELETE Author {lastName}, {firstName}  ?</h1>
            <button onClick = {handleClick}>Yes, Delete</button>
        </div>
    )
}

export default AuthorDelete
