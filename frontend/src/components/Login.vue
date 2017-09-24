<template>
  <div class="container">
    <form class="form-signin">
      <h2 class="form-signin-heading">{{$t("loginp.message")}}</h2>
      <label for="inputEmail" class="sr-only">Username</label>
      <input type="text" id="username" v-model="credentials.username" class="form-control" v-bind:placeholder="$t('loginp.username')" required autofocus>
      <label for="inputPassword" class="sr-only">Password</label>
      <input type="password" v-model="credentials.password"  id="password" class="form-control" v-bind:placeholder="$t('loginp.password')" required>
      <div class="checkbox">
        <label>
          <input type="checkbox" value="remember-me"> {{$t('loginp.remember')}}
        </label>
      </div>
      <button class="btn btn-lg btn-primary btn-block" type="submit"  @click="submit()">{{$t('loginp.button')}}</button>
    </form>
  </div>
</template>

<script>
 import auth from '@/auth'
 export default {
   data() {
     return {
       credentials: {
         username: '',
         password: ''
       },
       error: ''
     }
   },
   methods: {
     submit() {
       var credentials = {
         username: this.credentials.username,
         password: this.credentials.password
       }
       auth.login(this, credentials, 'home')
     }
   }
 }
</script>
