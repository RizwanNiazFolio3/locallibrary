import React, { 
    ReactElement,
} from 'react'
import {
    useForm,
    SubmitHandler,
} from 'react-hook-form'
import { AuthorDetails } from '../CustomTypes'

/**
 * Extending the AuthorDetails interface to create the props interface,
 * This is because we need to pass the author details seperately to the OnSubmit function.
 * The OnSubmit function itself is obtained as a prop from either the AuthorCreate or AuthotUpdate pages.
 * This allows the Author Form component to be used by both pages.
 */
interface Props extends AuthorDetails{
    onSubmit: SubmitHandler<AuthorDetails> 
}

function AuthorForm(props: Props): ReactElement {
    //We are using the useForm hook provided by the react-hook-form library
    //We can set the default values of the form by passing the desired values to the hook as shown
    const {register, handleSubmit} = useForm<AuthorDetails>({
        defaultValues: {
            first_name:props.first_name,
            last_name:props.last_name,
            date_of_birth:props.date_of_birth,
            date_of_death:props.date_of_death,
        }
    })

    return (
        <>
            {/* We can pass our custom onSubmit function as an argument to the handleSubmit function provided by react hook forms */}
            <form onSubmit = {handleSubmit(props.onSubmit)}>
                <label>First Name
                    {/* to use reacthook forms, we register the input field of the form as shown below by assigning it a name
                    The name must match the names provided in the DefaultValues defined above. If no DefaultValues are defined, the names
                    can be anything */}
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
