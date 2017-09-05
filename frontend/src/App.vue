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
  <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">User actions<span class="caret"></span></a>
  <ul class="dropdown-menu">
    <li class="dropdown-header">Stream</li>
    <li><a @click="opentheModal()" href="#">Add stream</a></li>
    <li><router-link to="streams">Manage streams</router-link></li>
    <li role="separator" class="divider"></li>
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


<div class="customAudioPlayer loading player_0 pitchfork" data-song-index="0">
  <div class="loader"></div><button v-bind:class="playerm.pclass" v-on:click="toggleplaying" class="playerTrigger"><span class="buttonText">play</span></button>
  <div class="metaWrapper"><span class="titleDisplay">{{playerm.title}}</span><span class="artistDisplay"></span></div>
  <div class="timingsWrapper"><span class="songPlayTimer">0:00</span>
    <div class="songProgressSliderWrapper">
      <div class="pseudoProgressBackground"></div>
      <div class="pseudoProgressIndicator"></div>
      <div class="pseudoProgressPlayhead"></div><input type="range" min="0" max="100" class="songProgressSlider"></div><span class="songDuration">-:--</span></div>
  <div class="songVolume"><button class="songMuteButton">Mute</button>
    <div class="songVolumeLabelWrapper"><span class="songVolumeLabel">Volume</span><span class="songVolumeValue">10</span></div>
    <div class="songVolumeSliderWrapper">
      <div class="pseudoVolumeBackground"></div>
      <div class="pseudoVolumeIndicator"></div>
      <div class="pseudoVolumePlayhead"></div><input type="range" min="0" max="1" step="0.1" class="songVolumeSlider"></div>
  </div>
</div>


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
      
      <div class="checkbox">
	<label><input type="checkbox" v-model="job.infinite" >Infinite playback</label>
      </div>
     
      <div class="form-group">
	<label for="dtinput1">Enter date</label>
	<div class='input-group date' id='datetimepicker1'>
	  
          <input v-bind:disabled="job.activate"  id="dtinput1" type='text' class="form-control" />
          <span class="input-group-addon">
            <span class="glyphicon glyphicon-calendar"></span>
          </span>

	</div>
	<input disabled="true" v-model="datefinish" id="dtinput2" type='text' class="form-control" />
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
import Home from '@/components/Home'
import bus from '@/eventbus.js'
import {API_URL} from '@/shared.js'

const STREAM_ADD_URL = API_URL + 'api/stream'
const JOB_ADD_URL = API_URL + 'api/job'


let component =  {
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
	fileduration: 0, // in seconds
	filehash: '',
	infinite: false
      },
      playerm: {
	playing: false,
	pclass: 'songPaused',
	title: 'Not playing'
      },
      inputdatejob: '',
      datefinish: '',
    }
  },

  watch: {
    'datefinish': function (val) {
      if (this.job.infinite) {
	this.datefinish = '∞'
      }
    },
    
    'job.infinite': function (val) {
      if (val) {
	this.datefinish = '∞'
      } else {
	// FIXME: no jquery shit
	let date = $("#datetimepicker1").data("DateTimePicker").date().toDate()
	this.datefinish = new Date(date.getTime() + 1000 * this.job.fileduration)
      }
    }
    
  },
  
  methods: {

    setplaying (stream) {
      this.playerm.title = stream
      this.playerm.pclass = 'songPaused'
    },
    
    toggleplaying (event) {
      this.playerm.playing = !this.playerm.playing
       if (this.playerm.playing) {
	   this.playerm.pclass = 'songPlaying'
       } else {
	 this.playerm.pclass = 'songPaused'
       }
      bus.$emit(
	'toggleplaying', this.playerm.playing
      )
      
    },
    opentheModal() {
      this.$refs.addstream.open()
    },
    opentheJobModal() {
      this.$refs.addJob.open()
    },
    logout() {
      auth.logout()
    },


    startplaying (s) {
      this.playerm.pclass = 'songPlaying'
      this.playerm.title = s
      this.playerm.playing = true
    },
    uploadFile(ev) {
      // console.log('ev')
    },

    submitstream () {
      let data = {
        name: this.stream.name,
        password: this.stream.password,
        stype: this.stream.stype
      }
      let modal = this.$refs.addstream
      this.$http.post(STREAM_ADD_URL, data, {headers: auth.getAuthHeader()})
        .then(response => {
          let data = response.data
          modal.close()
        },response => {

          // error callback
        })
    },

    submitjob () {

      let data = {
	stream: {
	  name: this.job.sname
	},
	filename: this.job.filehash,
	streamstart: $("#datetimepicker1").data("DateTimePicker").date().toDate(),
	streamfinish: new Date(this.datefinish),
	inf: this.job.infinite
      }
      
      let modal = this.$refs.addJob
      this.$http.post(JOB_ADD_URL, data, {headers: auth.getAuthHeader()})
        .then(response => {
	  console.log(data)
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
    bus.$on('splaying', (s) => {
      this.startplaying(s)
    })

  },

  mounted () {
    
    $('#datetimepicker1').datetimepicker({
      minDate:new Date()
    }).on("dp.change", (dt, oldDate) => {
      let date = dt.date.toDate()
      this.datefinish = new Date(date.getTime() + 1000 * this.job.fileduration)
    })
    

    let input = $("#fileinput");
    input.fileinput({
      uploadUrl: API_URL + "api/upload",
      maxFileCount: 1,
      showUpload: false,
      // showRemove: false,
      ajaxSettings: {'headers': {'Authorization': 'Token ' + localStorage.getItem('id_token')}}
    }).on("filebatchselected", function(event, files) {
      // trigger upload method immediately after files are selected
      input.fileinput("upload");
    })

    let vue = this
    $('#fileinput').on('fileuploaded', function(event, data, previewId, index) {
      let form = data.form, files = data.files, extra = data.extra, 
	  response = data.response, reader = data.reader;
      let duration = response.duration
      let filehash = response.hashid
      vue.job.activate = false
      vue.job.fileduration = duration
      vue.job.filehash = filehash
    });
  }
}


export default component

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
