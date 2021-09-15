import React, { ReactElement } from 'react'
import AuthorForm, {AuthorDetails} from '../AuthorForm'
import {SubmitHandler} from 'react-hook-form'
import axiosInstance from '../../axios'

interface Props {
    
}
function AuthorCreate(props: Props): ReactElement {
    const onSubmit: SubmitHandler<AuthorDetails> = data => {
        axiosInstance.post('/catalog/api/authors/',data)
        .then(res =>{
            console.log('Author Created')
        })
    }

    return (
        <div>
            <AuthorForm onSubmit={onSubmit}/>
        </div>
    )
}

export default AuthorCreate
