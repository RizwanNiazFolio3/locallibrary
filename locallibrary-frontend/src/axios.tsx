import axios, {AxiosInstance, AxiosRequestConfig} from 'axios'
import { AuthorDetails } from './CustomTypes'
import { HomeData } from './components/pages/Home'
import { 
	AuthorAttributes,
	UserLoginData,
	Tokens
} from './CustomTypes'
import jwt_decode from 'jwt-decode'
import { DecodedRefreshToken, AuthContext } from './contexts/AuthContext'

export class APIClient{

	private static axiosInstance:AxiosInstance
	private static instance:APIClient

	private constructor(options: AxiosRequestConfig){
		APIClient.axiosInstance = axios.create(options)
	}

	
	public static getInstance(options:AxiosRequestConfig): APIClient{
		if (!APIClient.instance){
			APIClient.instance = new APIClient(options)
			APIClient.instance.getInterceptors()
		}
		return APIClient.instance
	}
	
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
	
	public GetHomePageData():Promise<HomeData>{
		return APIClient.axiosInstance.get("/catalog/api/home")
		.then(res=>{
			let HomePageData:HomeData = res.data
			return HomePageData
		})
	}

	public GetAuthorsList():Promise<AuthorAttributes[]>{
		let authorList:AuthorAttributes[]
		return APIClient.axiosInstance.get("/catalog/api/authors")
		.then(response=>{
			authorList = response.data
			return authorList
		})
	}

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
	
	private SetAuthorizationHeaders(TokenHeader:String|null):void{
		APIClient.axiosInstance.defaults.headers['Authorization'] = TokenHeader
	}
	
	public Logout():Promise<boolean>{
		return APIClient.axiosInstance.post("/catalog/api/logout",{refresh : localStorage.getItem("refresh_token")})
		.then(res=>{
            localStorage.removeItem('access_token')
            localStorage.removeItem('refresh_token')
			APIClient.instance.SetAuthorizationHeaders(null)
			return true
		})
	}
	
	public PostAuthor(AuthorData:AuthorDetails):Promise<Number>{
		return APIClient.axiosInstance.post('/catalog/api/authors/',AuthorData)
        .then(res =>{
			//Redirect to the details page of the currently created author
            const id:Number = res.data.id
            return id
        })
	}
	
	public DeleteAuthor(id:string):Promise<Boolean>{
		return APIClient.axiosInstance.delete('/catalog/api/authors/' + id + "/")
		.then(res=>{
			return true
		})
	}
	
	public PutAuthor(id:string,data:AuthorDetails):Promise<Boolean>{
		return APIClient.axiosInstance.put("/catalog/api/authors/"+id+"/", data)
		.then(res=>{
			return true
		})
	}

	
	private UseRefreshToken(refreshToken:string):Promise<string>{
		return APIClient.axiosInstance.post('/catalog/api/token/refresh/',{refresh : refreshToken})
		.then(response=>{
			const access_token:string = response.data.access
			localStorage.setItem('access_token',access_token)
			APIClient.instance.SetAuthorizationHeaders("Bearer " + access_token)
			return access_token
		})
	}
	private getInterceptors(){
		console.log("Interceptors Set")
		APIClient.axiosInstance.interceptors.response.use(
			(response)=>{
				return response
			},
			(error)=>{
				const originalrequest = error.config
				if(error.response){
					if (error.response.status == 401 && !originalrequest._retry){
						originalrequest._retry = true
						const refreshToken = localStorage.getItem('refresh_token')
						if (refreshToken != null){
							const decoded_token:DecodedRefreshToken = jwt_decode(refreshToken)
							if (decoded_token.exp < Math.ceil(Date.now() / 1000)){
								localStorage.removeItem('refresh_token')
								localStorage.removeItem('access_token')
								window.location.href = '/login'

							}
							console.log(decoded_token)
							return APIClient.instance.UseRefreshToken(refreshToken)
							.then(access_token =>{
								originalrequest.headers['Authorization'] = "Bearer " + access_token
								return APIClient.axiosInstance(originalrequest) 
							})
						}
						window.location.href = '/login'
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
