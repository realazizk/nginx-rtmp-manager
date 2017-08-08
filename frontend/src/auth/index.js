///
// Audio Stream Manager
// Copyright Mohamed Aziz knani <medazizknani@gmai.com> 2017/
///


import router from '@/router'

const API_URL = 'http://localhost:8080/'
const LOGIN_URL = API_URL + 'api/login'
const SIGNUP_URL = API_URL + 'users/'

export default {

  user: {
    authenticated: false
  },

  login(context, creds, redirect) {
    context.$http.post(LOGIN_URL, creds)
      .then(response => {
        // success callback
        let data = response.body;
        localStorage.setItem('id_token', data.id_token)

        this.user.authenticated = true

        if(redirect) {
          router.go(redirect)
        }
      }, response => {
        // error callback
      })
  },

  signup(context, creds, redirect) {
    context.$http.post(SIGNUP_URL, creds, (data) => {
      localStorage.setItem('id_token', data.id_token)

      this.user.authenticated = true

      if(redirect) {
        router.go(redirect)
      }

    }).error((err) => {
      context.error = err
    })
  },

  logout() {
    localStorage.removeItem('id_token')
    this.user.authenticated = false
  },

  checkAuth() {
    var jwt = localStorage.getItem('id_token')
    if(jwt) {
      this.user.authenticated = true
    }
    else {
      this.user.authenticated = false
    }
  },


  getAuthHeader() {
    return {
      'Authorization': 'Token ' + localStorage.getItem('id_token')
    }
  }
}
