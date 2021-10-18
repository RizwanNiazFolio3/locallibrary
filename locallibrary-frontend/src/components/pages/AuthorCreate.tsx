import React, { ReactElement } from 'react'
import AuthorForm from '../AuthorForm'
import {SubmitHandler} from 'react-hook-form'
import {client} from '../../axios'
import {useHistory} from 'react-router-dom'
import {AuthorDetails} from '../../CustomTypes'

interface Props {
    
}
function AuthorCreate(props: Props): ReactElement {
    const history = useHistory()
    /**
     * We define our onSubmit function and use it to make a post request to the correct API endpoint,
     * @param data AuthorDetails is defined in the AuthorForms component page,
     */
    const onSubmit: SubmitHandler<AuthorDetails> = data => {
        client.PostAuthor(cleanData(data))
        .then(AuthorID => {
            history.push("/authors/" + AuthorID)
        })
    }

    //We must clean our data to ensure empty strings are sent as null values for the POST request to be valid
    function cleanData(data:AuthorDetails){
        data.first_name = data.first_name===""? null: data.first_name
        data.last_name = data.last_name===""? null: data.last_name
        data.date_of_birth = data.date_of_birth===""? null: data.date_of_birth
        data.date_of_death = data.date_of_death===""? null: data.date_of_death
        return data
    }

    return (
        <div>
            {/* We senf the onSubmit function as a prop to the AuthorForm component */}
            <AuthorForm onSubmit={onSubmit}/>
        </div>
    )
}

export default AuthorCreate
