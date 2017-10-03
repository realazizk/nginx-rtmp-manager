

let a = process.env.NODE_ENV;

if (a === 'development') {
  var API_URL = "http://localhost:8090/"
  var SERVER_URL = "http://localhost/stream/"
} else {
  var API_URL = "http://45.77.99.83:5000/"
  var SERVER_URL = "http://45.77.99.83/stream/"
}


export {
  API_URL,
  SERVER_URL
}
