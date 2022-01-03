export function handleResponse(response) {
  console.log(response)
    if (response.results) {
      return response.results;
    }
    if (response.data) {
      return response.data;
    }

    // if (response === []) {
    //   return 
    // }
    
    return response;
  }
  
  export function handleError(error) {
    console.log(error)
    if (error.data) {
      return error.data;
    }
    return error;
  }