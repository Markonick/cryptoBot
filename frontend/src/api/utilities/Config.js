import React from "react"
import axios from "axios"
import Swal from 'sweetalert2'

let apiClient = {}
  apiClient = axios.create({
    // withCredentials: true,
    baseURL: process.env.REACT_APP_BASE_URL,
    timeout: 1000,
    headers: { Accept: "application/json" }
  })

const generateErrorDetails = (traceId) => {
  let text = `<pre>
    Something went wrong!\n
    trace id: ${traceId}
    <pre>
  `
  return text
}

const custom5xxPopup = (traceId, httpErrorStatus) => {
    Swal.fire({
      background: 'rgb(15,15,15)',
      icon: 'error',
      title: `Oops...${httpErrorStatus}`,
      html: generateErrorDetails(traceId),
      // footer: `<a>trace id: ${traceId}</a>`
    })
}

apiClient.interceptors.response.use(
  response => {
    console.log(response)
    return response
  },
  error => {
    console.log(error)
    // if(error['response'] == undefined) {
    //   console.log('ERROR RESPONSE UNDEFINED')
    //   return []
    // }
    if (error.response.status >= 500 && error.response.status < 600) {
      console.log("ERROR RESPONSE in 500s is: ", error.response.status)
      custom5xxPopup("TraceId", error.response.status)
    } else if (error.response.status === 401) {
      console.log("ERROR RESPONSE is: ", error.response.status)
      custom5xxPopup("TraceId", error.response.status)
    } else {
      console.log("ERROR RESPONSE is: ", error)
      console.log("RETURN EMPTY ARRAY: ")
      custom5xxPopup("TraceId", error)
    }
  })

export default apiClient
