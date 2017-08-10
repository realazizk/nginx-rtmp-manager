///
// Audio Stream Manager
// Copyright Mohamed Aziz knani <medazizknani@gmai.com> 2017
///

import Vue from 'vue'
import App from './App'
import router from './router'
import VueResource from 'vue-resource'
import auth from './auth'
import $ from 'jquery'
import 'bootstrap'
import 'bootstrap-fileinput'
import dateTimePicker from 'eonasdan-bootstrap-datetimepicker'
import 'eonasdan-bootstrap-datetimepicker/build/css/bootstrap-datetimepicker.css'
import './assets/player.css'


let bs_modal = require('vue2-bootstrap-modal')

Vue.use(VueResource)
Vue.component('bootstrap-modal', bs_modal)

// checks auth in start of the application
auth.checkAuth()

Vue.config.productionTip = false

new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: {
    App
  }
})
