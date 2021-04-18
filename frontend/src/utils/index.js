import axios from 'axios'

export const backend = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 30000
})