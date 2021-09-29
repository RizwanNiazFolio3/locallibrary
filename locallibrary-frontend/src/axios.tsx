import axios from 'axios'
import jwt_decode from 'jwt-decode'

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

export function GetAuthors(setAuthorList){
	/**
	 * Since we've added "proxy": "http://127.0.0.1:8000/", to packages.json,
	 * We do not need to use the full URL and instead a relative URL can be used to access the endpoint
	 */
		axiosInstance.get("/catalog/api/authors")
		.then(
			(res) => {setAuthorList(res.data)},
			(error) => {console.log("There was an error retrieving author list")}//Place holder. Will be used for error handling
		)
}

export function HomePage(setData){
	/**
	 * Since we've added "proxy": "http://127.0.0.1:8000/", to packages.json,
	 * We do not need to use the full URL and instead a relative URL can be used to access the endpoint
	 */
		axiosInstance.get("/catalog/api/home")
		.then(
			(res) => {setData(res.data)},
			(error) => {console.log("An error occured")}
		) //This should define how the app behaves if the api get request fails
}

export function GetToken(data,history,LoginFunction){
	axiosInstance.post("/catalog/api/token/",data)
	.then((res) =>{
		//Storing the access and refresh tokens.
		localStorage.setItem('access_token',res.data.access)
		localStorage.setItem('refresh_token',res.data.refresh)
		//passing the decoded access token to the AuthContext to get the state variables needed to render for the
		//current user
		const decoded_token = jwt_decode(localStorage.getItem("access_token"))
		LoginFunction(decoded_token)
		axiosInstance.defaults.headers['Authorization'] = "Bearer " + localStorage.getItem('access_token')
		history.push('/')
	})
}

export default axiosInstance