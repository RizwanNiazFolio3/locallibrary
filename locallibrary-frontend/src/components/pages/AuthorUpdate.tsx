import React, { 
    ReactElement,
    useEffect,
    useState,
} from 'react'
import axiosInstance from '../../axios'
import {
    useParams,
} from 'react-router-dom'
import AuthorForm, {AuthorDetails} from '../AuthorForm';
import {SubmitHandler} from 'react-hook-form'

interface Props {
    
}

function AuthorUpdate(props: Props): ReactElement {
    let {id}:{id: string} = useParams();

    const [firstName,setFirstName] = useState<string>()
    const [lastName,setLastName] = useState<string>()
    const [dateOfBirth,setDateOfBirth] = useState<string>()
    const [dateOfDeath,setDateOfDeath] = useState<string>()
    const [loaded,setLoaded] = useState<boolean>(false)

    const onSubmit: SubmitHandler<AuthorDetails> = data => {
        axiosInstance.put("/catalog/api/authors/"+id+"/", data)
        .then(response =>{
            console.log('This was called')
            console.log(data)
        })
    }

    useEffect(() => {
        axiosInstance.get("/catalog/api/authors/"+id)
        .then(response =>{
            setFirstName(response.data.first_name)
            setLastName(response.data.last_name)
            setDateOfBirth(response.data.date_of_birth)
            setDateOfDeath(response.data.date_of_death)
            setLoaded(true)
        })
    },[id])

    return (
        <div>
            {loaded === true?
            <AuthorForm
                first_name={firstName}
                last_name={lastName}
                date_of_birth={dateOfBirth}
                date_of_death={dateOfDeath}
                onSubmit = {onSubmit}
            />
            :<h1>Loading</h1>}

        </div>
    )
}

export default AuthorUpdate
