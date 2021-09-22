import axios from 'axios'

const axiosInstance = axios.create({
	/**
	 * This is the axios instance used by the entire frontend app.
	 * When a user logs in, the Authorization details are stored here so that all future requests use them.
	 * Axios interceptors will also be added to help with refreshing the access token and error handling in the future
	 */
	timeout: 5000,
	headers: {
		Authorization: localStorage.getItem('access_token'),
		'Content-Type': 'application/json',
		accept: 'application/json',
	}, 
});

export function Axioslogout(history,LogoutFunction){
	//The logout api endpoint takes the current refresh token and adds it to the blacklist
	axiosInstance.post("/catalog/api/logout",{refresh : localStorage.getItem("refresh_token")})
	.then((res) =>{
		//Access and refresh tokens removed from localStorage
		localStorage.removeItem('access_token')
		localStorage.removeItem('refresh_token')
		//The state variables in the context provider are set to default
		LogoutFunction()
		//The authorization in the headers is set to null for all future requests
		axiosInstance.defaults.headers['Authorization'] = null
		history.push('/')
	})
}

export function GetAuthorDetails(
	id,
	setFirstName,
	setLastName,
	setDateOfBirth,
	setDateOfDeath){
	axiosInstance.get("/catalog/api/authors/"+id)
	.then(response =>{
		setFirstName(response.data.first_name)
		setLastName(response.data.last_name)
		setDateOfBirth(response.data.date_of_birth)
		setDateOfDeath(response.data.date_of_death)
	})
}

export default axiosInstance