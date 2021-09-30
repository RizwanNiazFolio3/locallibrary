import React, { 
    ReactElement,
    useEffect,
    useState,
} from 'react';
import {
    useParams,
    useHistory,
} from 'react-router-dom';
import {client} from '../../axios'

interface Props {

}

function AuthorDelete(props: Props): ReactElement {
    let {id}:{id: string} = useParams();
    const history = useHistory()
    const [firstName,setFirstName] = useState<string|null|undefined>("--Loading--")
    const [lastName,setLastName] = useState<string|null|undefined>("--Loading--")

    //We will make a get request to obtain the details of the author we are about to delete.
    useEffect(() =>{
        client.GetAuthorDetails(id)
        .then(Author=>{
            setFirstName(Author.first_name)
            setLastName(Author.last_name)
        })
    },[id])

    //Deleting the author and then redirecting to the /authors page upon success
    function handleClick()
    {
        client.DeleteAuthor(id)
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
