import React, { ReactElement } from 'react'
import AuthorForm, {AuthorDetails} from '../AuthorForm'
import {SubmitHandler} from 'react-hook-form'
import axiosInstance from '../../axios'
import {useHistory} from 'react-router-dom'

interface Props {
    
}
function AuthorCreate(props: Props): ReactElement {
    const history = useHistory()
    const onSubmit: SubmitHandler<AuthorDetails> = data => {
        axiosInstance.post('/catalog/api/authors/',cleanData(data))
        .then(res =>{
            const id = res.data.id
            history.push("/authors/" + id)
        })
    }

    function cleanData(data:AuthorDetails){
        data.first_name = data.first_name===""? null: data.first_name
        data.last_name = data.last_name===""? null: data.last_name
        data.date_of_birth = data.date_of_birth===""? null: data.date_of_birth
        data.date_of_death = data.date_of_death===""? null: data.date_of_death
        return data
    }

    return (
        <div>
            <AuthorForm onSubmit={onSubmit}/>
        </div>
    )
}

export default AuthorCreate
