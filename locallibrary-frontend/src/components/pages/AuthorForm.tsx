import React, { ReactElement, } from 'react'
import {
    useParams,
} from 'react-router-dom'

interface Props {
    
}

function AuthorForm({}: Props): ReactElement {
    let {id}:{id: string} = useParams();
    let {method}:{method:string} = useParams();
    return (
        <div>
            <h1>Method : {method} </h1>
        </div>
    )
}

export default AuthorForm
