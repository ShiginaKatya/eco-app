import axios from 'axios'


export const API_URL = 'http://127.0.0.1:8000/api'

const axiosInstance = axios.create({
  baseURL: API_URL,
  // withCredentials: true,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json'
  }
})

axiosInstance.interceptors.request.use((config) => {
  config.headers.Authorization = `Bearer ${window.localStorage.getItem('access_token')}`
  return config
})

axiosInstance.interceptors.response.use(
  (config) => {
    return config
  },
  async (error) => {
    const originalRequest = error.config
    if (error.response.status === 401 && error.config && !error.config._isRetry) {
      originalRequest._isRetry = true
      try {
        const response = await axios.post(`${API_URL}/token/`, false, {
          withCredentials: true
        })
        localStorage.setItem('access_token', response.data.access)
        return axiosInstance.request(originalRequest)
      } catch (e) {
        console.log('ошибка')
      }
    }
    throw error
  }
)

export default axiosInstance