import React, { 
    ReactElement,
} from 'react';
import {
    useParams
} from 'react-router-dom';

interface Props {
    
}

function AuthorDelete({}: Props): ReactElement {
    let {id}:{id: string} = useParams();
    return (
        <div>
            <h1>DELETE Author with ID = {id} ?</h1>
        </div>
    )
}

export default AuthorDelete
