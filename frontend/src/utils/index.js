import axios from 'axios'

export const backend = axios.create({
  baseURL: process.env.VUE_APP_BACKEND_URL,
  timeout: 5000
})