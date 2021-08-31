import axios from 'axios'

const axiosInstance = axios.create({
	baseURL: '',
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