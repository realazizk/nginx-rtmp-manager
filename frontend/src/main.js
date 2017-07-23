// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import VueResource from 'vue-resource'
import auth from './auth'
import $ from 'jquery'
import 'bootstrap'

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
