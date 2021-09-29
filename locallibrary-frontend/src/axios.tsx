import axios, {AxiosInstance, AxiosRequestConfig} from 'axios'
import { AuthorDetails } from './CustomTypes'
import { HomeData } from './components/pages/Home'
import { AuthorAttributes } from './CustomTypes'

export class APIClient{

	private static axiosInstance:AxiosInstance
	private static instance:APIClient

	private constructor(options: AxiosRequestConfig){
		APIClient.axiosInstance = axios.create(options)
	}

	public static getInstance(options:AxiosRequestConfig): APIClient{
		if (!APIClient.instance){
			APIClient.instance = new APIClient(options)
		}
		return APIClient.instance
	}

	public GetAuthorDetails(id:string){
		return APIClient.axiosInstance.get("/catalog/api/authors/"+id)
		.then(res=>{

			let author: AuthorDetails = {
				first_name:null,
				last_name:null,
				date_of_death:null,
				date_of_birth:null
			}

			author.date_of_birth = res.data.date_of_birth 
			author.date_of_death = res.data?.date_of_death
			author.first_name = res.data?.first_name
			author.last_name = res.data?.last_name
			return author
		})
	}

	public GetHomePageData(){
		return APIClient.axiosInstance.get("/catalog/api/home")
		.then(res=>{
			let HomePageData:HomeData = res.data
			return HomePageData
		})
	}

	public GetAuthorsList(){
		let authorList:AuthorAttributes[]
		return APIClient.axiosInstance.get("/catalog/api/authors")
		.then(response=>{
			authorList = response.data
			return authorList
		})
	}
}

export const client = APIClient.getInstance({
	/**
	 * This is the axios instance used by the entire frontend app.
	 * When a user logs in, the Authorization details are stored here so that all future requests use them.
	 * Axios interceptors will also be added to help with refreshing the access token and error handling in the future
	 */
	timeout: 5000,
	headers: {
		Authorization: localStorage.getItem('access_token')
			? localStorage.getItem('access_token')
			: null,
		'Content-Type': 'application/json',
		accept: 'application/json',
	},
	// transformResponse: [(response) =>{
	// 	return response.data
	// }]
})


const axiosInstance = axios.create({
	/**
	 * This is the axios instance used by the entire frontend app.
	 * When a user logs in, the Authorization details are stored here so that all future requests use them.
	 * Axios interceptors will also be added to help with refreshing the access token and error handling in the future
	 */
	timeout: 5000,
	headers: {
		Authorization: localStorage.getItem('access_token')
			? localStorage.getItem('access_token')
			: null,
		'Content-Type': 'application/json',
		accept: 'application/json',
	},
});

export default axiosInstance
