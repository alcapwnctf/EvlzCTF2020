import process from "process";
import axios from "axios";

let API_ROOT = ""

// if (!process.env.NODE_ENV || process.env.NODE_ENV === 'development') {
//     API_ROOT = "http://127.0.0.1:8000/api"
// } else {
API_ROOT = "/api"
// }

const instance = axios.create({
    baseURL: API_ROOT,
    timeout: 5000,
  });

const USER_ENDPOINT = "/user"
const LOGIN_ENDPOINT = "/login"
const PREVIEW_ENDPOINT = "/preview"
const FLAG_ENDPOINT = "/flag"

const getUser = async (userId) => {
    return await instance.get(`${USER_ENDPOINT}/${userId}`, { withCredentials:"true" })
}

const loginUser = async (userCreds) => {
    return await instance.post(LOGIN_ENDPOINT, userCreds, { withCredentials:"true" })
}

const registerUser = async (userData) => {
    return await instance.post(USER_ENDPOINT, userData)
}

const createVaccine = async (userId, vaccine) => {
    const VACCINE_ENDPOINT = "/vaccine"
    return await instance.post(`${USER_ENDPOINT}/${userId}${VACCINE_ENDPOINT}`, vaccine, { withCredentials:"true" })
}

const getPreview = async (url) => {
    return await instance.get(`${PREVIEW_ENDPOINT}?url=${url}`,{ withCredentials:"true" })
}

const getFlag = async () => {
    return await instance.get(`${FLAG_ENDPOINT}`, { withCredentials:"true" })
}

export {
    getUser,
    loginUser,
    registerUser,
    createVaccine,
    getPreview,
    getFlag
}
