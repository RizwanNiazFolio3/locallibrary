import React, { 
    ReactElement,
} from 'react'
import {
    useForm,
    SubmitHandler,
} from 'react-hook-form'

export interface AuthorDetails {
    first_name?: string|null,
    last_name?: string|null,
    date_of_birth?: string|null,
    date_of_death?:string|null
}

interface Props extends AuthorDetails{
    onSubmit: SubmitHandler<AuthorDetails> 
}

function AuthorForm(props: Props): ReactElement {
    const {register, handleSubmit} = useForm<Props>({
        defaultValues: {
            first_name:props.first_name,
            last_name:props.last_name,
            date_of_birth:props.date_of_birth,
            date_of_death:props.date_of_death,
        }
    })

    return (
        <>
            <form onSubmit = {handleSubmit(props.onSubmit)}>
                <label>First Name
                    <input
                        {...register('first_name')}
                        type="text"
                        placeholder={"First Name"}
                    />
                </label>
                <br/>
                <label>Last Name
                    <input
                        {...register('last_name')}
                        type="text"
                        placeholder={"Last Name"}
                    />
                </label>
                <br/>
                <label>Date of Birth
                    <input
                        {...register('date_of_birth')}
                        type="text"
                        placeholder={"yyyy-mm-dd"}
                    />
                </label>
                <br/>            
                <label>Date Of Death
                    <input
                        {...register('date_of_death')}
                        type="text"
                        placeholder={"yyyy-mm-dd"}
                    />
                </label>
                <br/>
                <button>Submit</button>

            </form>
        </>
    )
}

export default AuthorForm
