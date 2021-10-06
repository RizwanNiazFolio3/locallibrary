import axios, {AxiosInstance, AxiosRequestConfig} from 'axios'
import { AuthorDetails } from './CustomTypes'
import { HomeData } from './components/pages/Home'
import { 
	AuthorAttributes,
	UserLoginData,
	Tokens
} from './CustomTypes'
import jwt_decode from 'jwt-decode'
import { DecodedRefreshToken } from './contexts/AuthContext'

export class APIClient{
	/**
	 * This class handles all the calls to the Django Rest Api
	 * The class is a singleton, and uses an Axios Instance as an attribute
	 */

	private static axiosInstance:AxiosInstance
	private static instance:APIClient

	//The constructor creates an axiosInstance
	private constructor(options: AxiosRequestConfig){
		APIClient.axiosInstance = axios.create(options)
	}

	//The getInstance method returns an instance of the class to be used
	public static getInstance(options:AxiosRequestConfig): APIClient{
		if (!APIClient.instance){
			APIClient.instance = new APIClient(options)
			APIClient.instance.getInterceptors()
		}
		return APIClient.instance
	}
	
	//Used to get the detauls of an author
	public GetAuthorDetails(id:string):Promise<AuthorDetails>{
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
	
	//Used to get data needed to fill the home page
	public GetHomePageData():Promise<HomeData>{
		return APIClient.axiosInstance.get("/catalog/api/home")
		.then(res=>{
			let HomePageData:HomeData = res.data
			return HomePageData
		})
	}

	//Used to get a list of all the authors
	public GetAuthorsList():Promise<AuthorAttributes[]>{
		let authorList:AuthorAttributes[]
		return APIClient.axiosInstance.get("/catalog/api/authors")
		.then(response=>{
			authorList = response.data
			return authorList
		})
	}

	//Used to get access and refresh tokens for the login component
	public Login(data:UserLoginData):Promise<Tokens>{
        return APIClient.axiosInstance.post("/catalog/api/token/",data)
        .then((res) =>{
			let tokens:Tokens = {
				access_token:res.data.access,
				refresh_token:res.data.refresh
			}
			localStorage.setItem('access_token',tokens.access_token)
            localStorage.setItem('refresh_token',tokens.refresh_token)
			APIClient.instance.SetAuthorizationHeaders('Bearer '+ tokens.access_token)
			return tokens
        })
	}
	
	//Used to set the authorization headers with the access token for the axios instant
	private SetAuthorizationHeaders(TokenHeader:String|null):void{
		APIClient.axiosInstance.defaults.headers['Authorization'] = TokenHeader
	}
	
	//Used to clear the access and refresh tokens, remove them from the authorization headers and add the refresh token to
	//the blacklist app
	public Logout():Promise<boolean>{
		return APIClient.axiosInstance.post("/catalog/api/logout",{refresh : localStorage.getItem("refresh_token")})
		.then(res=>{
            localStorage.removeItem('access_token')
            localStorage.removeItem('refresh_token')
			APIClient.instance.SetAuthorizationHeaders(null)
			return true
		})
	}
	
	//Used to create a new author from the create author component
	public PostAuthor(AuthorData:AuthorDetails):Promise<Number>{
		return APIClient.axiosInstance.post('/catalog/api/authors/',AuthorData)
        .then(res =>{
			//Redirect to the details page of the currently created author
            const id:Number = res.data.id
            return id
        })
	}
	
	//Used to delete a given author from the delete author page
	public DeleteAuthor(id:string):Promise<Boolean>{
		return APIClient.axiosInstance.delete('/catalog/api/authors/' + id + "/")
		.then(res=>{
			return true
		})
	}
	
	//Used to update a given authors data
	public PutAuthor(id:string,data:AuthorDetails):Promise<Boolean>{
		return APIClient.axiosInstance.put("/catalog/api/authors/"+id+"/", data)
		.then(res=>{
			return true
		})
	}

	//Helper function for the axios interceptors.
	//Used to get a new access token using a refresh token
	private UseRefreshToken(refreshToken:string):Promise<string>{
		return APIClient.axiosInstance.post('/catalog/api/token/refresh/',{refresh : refreshToken})
		.then(response=>{
			const access_token:string = response.data.access
			localStorage.setItem('access_token',access_token)
			APIClient.instance.SetAuthorizationHeaders("Bearer " + access_token)
			return access_token
		})
	}
	//Used to intercept certain responses
	private getInterceptors(){
		APIClient.axiosInstance.interceptors.response.use(
			(response)=>{
				//If the status code for the response is 2XX, do nothing and send the response forward 
				return response
			},
			(error)=>{
				//If the status code is not 2XX
				//Process the request.
				const originalrequest = error.config
				if(error.response){
					if (error.response.status === 401 && !originalrequest._retry){
						//If the status code is 401 and the request has not been retried before, 
						//Check to see if the refresh token is valid
						originalrequest._retry = true
						const refreshToken = localStorage.getItem('refresh_token')
						if (refreshToken != null){
							const decoded_token:DecodedRefreshToken = jwt_decode(refreshToken)
							if (decoded_token.exp < Math.ceil(Date.now() / 1000)){
								//if the refresh token is expired, logout the user and remove the access and refresh tokens,
								//redirect the user to the login page
								localStorage.removeItem('refresh_token')
								localStorage.removeItem('access_token')
								window.location.href = '/login/'
							}
							return APIClient.instance.UseRefreshToken(refreshToken)
							.then(access_token =>{
								//If the refresh token is valid, generate a new access token and retry the original request
								//with the new access token in the authorization header
								originalrequest.headers['Authorization'] = "Bearer " + access_token
								return APIClient.axiosInstance(originalrequest) 
							})
						}
						//If the refresh token is not available, logout the user and redirect them to the login page
						localStorage.removeItem('refresh_token')
						localStorage.removeItem('access_token')
						window.location.href = '/login/'
					}
					return Promise.reject(error)
				}
				return Promise.reject(error)
			}
		)
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
