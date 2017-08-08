<template>
  <div id="app">
    <nav class="navbar navbar-inverse" id="nav">
      <div class="container-fluid">
        <div class="navbar-header">
          <a class="navbar-brand" href="#">Stream manager</a>
        </div>
        <ul class="nav navbar-nav">
          <router-link active-class="active" tag="li" to="home"><router-link to="home">Home</router-link></router-link>

          <router-link active-class="active"  tag="li" to="contact"> <router-link to="contact">Contact</router-link> </router-link>     </li>

<li class="dropdown" v-if="user.authenticated">
  <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Admin actions<span class="caret"></span></a>
  <ul class="dropdown-menu">
    <li class="dropdown-header">Stream</li>
    <li><a @click="opentheModal()" href="#">Add stream</a></li>
    <li><a href="#">Delete stream</a></li>
    <li role="separator" class="divider"></li>
    <li class="dropdown-header">Users</li>
    <li><a href="#">Add admin</a></li>
    <li><a href="#">Delete admin</a></li>

    <li class="dropdown-header">Jobs</li>
    <li><router-link to="jobs">Manage jobs</router-link></li>
    <li><a @click="opentheJobModal()" href="#">Add a job</a></li>
  </ul>
</li>

</ul>



<ul class="nav navbar-nav navbar-right">
  <template v-if="!user.authenticated">
    <router-link active-class="active" tag="li" to="login">
      <router-link to="login">
        <span class="glyphicon glyphicon-log-in"></span> Login
      </router-link>
    </router-link>
  </template>
  <template v-else>
    <li>
      <router-link to="login" v-on:click.native="logout()">
        <span class="glyphicon glyphicon-log-in"></span> Logout
      </router-link>
    </li>
  </template>
</ul>
</div>
</nav>




<router-view></router-view>

<bootstrap-modal ref="addstream" :needHeader="true" :needFooter="false" size="large">
  <div slot="title">
    Add stream
  </div>
  <div slot="body">
    <form action="">
      <label for="name">The stream url</label>
      <div class="input-group">
        <span class="input-group-addon" id="basic-addon3">http://{{hostname}}</span>
        <input type="text"   v-model="stream.name" class="form-control" id="name" aria-describedby="basic-addon3">
      </div>

      <label for="password">Password</label>
      <input type="password"  v-model="stream.password" class="form-control" id="password">

      <label for="sel1">Select stream type:</label>
      <select v-model="stream.stype"  class="form-control" id="stype">
        <option selected>video</option>
        <option>audio</option>
      </select>

      <button type="submit" class="btn btn-default "  @click="submitstream()">Submit</button>

    </form>
  </div>

</bootstrap-modal>

<bootstrap-modal ref="addJob" :needHeader="true" :needFooter="false" size="large">
  <div slot="title">
    Add a job
  </div>
  <div slot="body">
    <form action="">
      <label for="fileinput">The file (can convert video to audio only)</label>
      <input id="fileinput" type="file" class="file" v-on:change="uploadFile">
      
      <div class="form-group">
	<label for="dtinput1">Enter date</label>
	<div class='input-group date' id='datetimepicker1'>
	  
          <input v-bind:disabled="job.activate" id="dtinput1" type='text' class="form-control" />
          <span class="input-group-addon">
            <span class="glyphicon glyphicon-calendar"></span>
          </span>

	  <input style='margin-left: 10px' disabled="true" id="dtinput2" type='text' class="form-control" />

	</div>
      </div>
      <label for="selst">Select the channel to stream to</label>
      <select v-model="job.sname" v-bind:disabled="job.activate"  class="form-control" id="selst">
        <option v-for="stream in job.streams">
          {{stream.name}}
        </option>
      </select>

      <button type="submit" class="btn btn-default " v-bind:disabled="job.activate" @click="submitjob()">Submit</button>

    </form>
  </div>

</bootstrap-modal>



</div>
</template>

<script>
import auth from '@/auth'
const API_URL = 'http://localhost:8080/'
const STREAM_ADD_URL = API_URL + 'api/stream'


export default {
  name: 'app',
  data() {
    return {
      user: auth.user,
      stream: {
        name: '',
        password: '',
        stype: '',
      },
      job: {
        streams: [],
        sname: '',
	activate: true,
	fileduration: 0 // in seconds
      },

    }
  },
  methods: {
    opentheModal() {
      this.$refs.addstream.open()
    },
    opentheJobModal() {
      this.$refs.addJob.open()
    },
    logout() {
      auth.logout()
    },

    submitjob() {

    },

    uploadFile(ev) {
      console.log('ev')
    },

    submitstream () {
      var data = {
        name: this.stream.name,
        password: this.stream.password,
        stype: this.stream.stype
      }
      var modal = this.$refs.addstream
      this.$http.post(STREAM_ADD_URL, data, {headers: auth.getAuthHeader()})
        .then(response => {
          let data = response.data
          modal.close()
        },response => {

          // error callback
        })
    }

  },
  computed: {
    hostname () {
      return location.hostname + ':1935/stream/';
    }

  },

  created() {
    this.$http.get(API_URL + 'api/streams').then(
      response => {
        let data = response.body
        this.job.streams = data
      }
    )

  },
  mounted () {
    $(function () {
      $('#datetimepicker1').datetimepicker({
	minDate:new Date()
      });
    });

    var input = $("#fileinput");
    input.fileinput({
      uploadUrl: "http://localhost:8080/api/upload",
      maxFileCount: 1,
      showUpload: false,
      showRemove: false,
      ajaxSettings: {'headers': {'Authorization': 'Token ' + localStorage.getItem('id_token')}}
    }).on("filebatchselected", function(event, files) {
      // trigger upload method immediately after files are selected
      input.fileinput("upload");
    })

    var vue = this
    $('#fileinput').on('fileuploaded', function(event, data, previewId, index) {
      var form = data.form, files = data.files, extra = data.extra, 
	  response = data.response, reader = data.reader;
      let duration = response.duration
      console.log(date)
      console.log(vue.job)
      vue.job.activate = false
      vue.job.fileduration = duration
    });
  }
}
</script>

<style>
#app {
      font-family: 'Avenir', Helvetica, Arial, sans-serif;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      text-align: center;
      color: #2c3e50;
      margin: 0;
  }

#nav {
    border-radius: 0;
}
</style>
