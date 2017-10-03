<template>
<div id="app">
    <nav class="navbar navbar-inverse" id="nav">
    <div class="container-fluid">
        <div class="navbar-header">
        <a class="navbar-brand" href="#">{{$t("name")}}</a>
        </div>
        <ul class="nav navbar-nav">
        <router-link active-class="active" tag="li" to="home"><router-link to="home">{{$t("home")}}</router-link></router-link>

        <router-link active-class="active"  tag="li" to="contact"> <router-link to="contact">{{$t("contact")}}</router-link> </router-link>     </li>

	<li class="dropdown" v-if="user.authenticated">
	    <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">{{$t('menu.actions')}}<span class="caret"></span></a>
	    <ul class="dropdown-menu">
		<li class="dropdown-header">{{$t('menu.stream')}}</li>
		<li><a @click="opentheModal()" href="#">{{$t('menu.addstream')}}</a></li>
		<li><router-link to="streams">{{$t('menu.managestreams')}}</router-link></li>
		<li role="separator" class="divider"></li>
		<li class="dropdown-header">{{$t('menu.jobs')}}</li>
		<li><router-link to="jobs">{{$t('menu.managejobs')}}</router-link></li>
		<li><a @click="opentheJobModal()" href="#">{{$t('menu.addjob')}}</a></li>
		</ul>

		
		
	</li>

	<li class="dropdown">
	    <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">{{$t('lang.l')}}<span class="caret"></span></a>
	    
	    <ul class="dropdown-menu">  
		<li v-for="lang in $t('lang.ls')">
		    <a @click="changeLang(lang['code'])"  href="#">{{lang['name']}}</a>
		    </li>
	    </ul>
	</li>

	</ul>

	<template v-if="locale == 'ar'">
	    <ul class="nav navbar-nav navbar-left">
		<template v-if="!user.authenticated">
		    <router-link active-class="active" tag="li" to="login">
			<router-link to="login">
			    <span class="glyphicon glyphicon-log-in"></span> {{$t("login")}}
			    </router-link>
		    </router-link>
      </template>
		<template v-else>
		  <li>
		    <router-link to="login" v-on:click.native="logout()">
		      <span class="glyphicon glyphicon-log-in"></span> {{$t('bar.logout')}}
		    </router-link>
		  </li>
		</template>
	    </ul>
	</template>
	<template v-else>
	  <ul class="nav navbar-nav navbar-right">
	    <template v-if="!user.authenticated">
	      <router-link active-class="active" tag="li" to="login">
		<router-link to="login">
		  <span class="glyphicon glyphicon-log-in"></span> {{$t("login")}}
		</router-link>
	      </router-link>
	    </template>
	    <template v-else>
	      <li>
		<router-link to="login" v-on:click.native="logout()">
		  <span class="glyphicon glyphicon-log-in"></span> {{$t('bar.logout')}}
		</router-link>
	      </li>
	    </template>
	  </ul>
	</template>


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
    {{$t('addstreammodal.title')}}
  </div>
  <div slot="body">
    <form action="">
      <label for="name">{{$t('addstreammodal.url')}}</label>
      <div class="input-group">
        <span class="input-group-addon" id="basic-addon3">http://{{hostname}}</span>
        <input type="text"   v-model="stream.name" class="form-control" id="name" aria-describedby="basic-addon3">
      </div>

      <label for="password">{{$t('addstreammodal.password')}}</label>
      <input type="password"  v-model="stream.password" class="form-control" id="password">

      <label for="sel1">{{$t('addstreammodal.stype')}}</label>
      <select v-model="stream.stype"  class="form-control" id="stype">
        <option selected>video</option>
        <option>audio</option>
      </select>

      <button type="submit" class="btn btn-default "  @click="submitstream()">{{$t('addstreammodal.submit')}}</button>

    </form>
  </div>

</bootstrap-modal>

<bootstrap-modal ref="addJob" :needHeader="true" :needFooter="false" size="large">
  <div slot="title">
    {{$t('addjobmodal.title')}}
  </div>
  <div slot="body">
    <form action="">
      <input id="fileinput" type="file" class="file" v-on:change="uploadFile">
      
      <div class="checkbox">
	<label><input type="checkbox" v-model="job.infinite" >{{$t('addjobmodal.inf')}}</label>
      </div>

      <div class="checkbox">
	<label><input type="checkbox" v-model="job.shuffle" >{{$t('addjobmodal.shuffle')}}</label>
      </div>

      

      <div class="form-group">

	<div class="checkbox">
	  <label><input type="checkbox" v-model="job.playnow" >{{$t('addjobmodal.playnow')}}</label>
	</div>

	<label for="dtinput1">{{$t('addjobmodal.enterdate')}}</label>
	<div class='input-group date' id='datetimepicker1'>
	  
          <input v-bind:disabled="job.activate || job.playnow"  id="dtinput1" type='text' class="form-control" />
          <span class="input-group-addon">
            <span class="glyphicon glyphicon-calendar"></span>
          </span>

	</div>
	<input disabled="true" v-model="datefinish" id="dtinput2" type='text' class="form-control" />
      </div>
      <label for="selst">{{$t('addjobmodal.channel')}}</label>
      <select v-model="job.sname" v-bind:disabled="job.activate"  class="form-control" id="selst">
        <option v-for="stream in job.streams">
          {{stream.name}}
        </option>
      </select>

      <button type="submit" class="btn btn-default " v-bind:disabled="job.activate" @click="submitjob()">{{$t('addjobmodal.submit')}}</button>

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
import moment from 'moment'


const STREAM_ADD_URL = API_URL + 'api/stream'
const JOB_ADD_URL = API_URL + 'api/job'


let component =  {
  name: 'app',

  ////
  // Data
  ////

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
	files: [],
	infinite: false,
	filesduration: 0,
	shuffle: false,
	playnow: false
      },
      playerm: {
	playing: false,
	pclass: 'songPaused',
	title: 'Not playing'
      },
      inputdatejob: '',
      datefinish: '',
      locale: this.$i18n.locale
    }
  },

  ////
  // End data
  ////


  ////
  // Watchers
  ////
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
	this.datefinish = new Date(date.getTime() + 1000 * this.job.filesduration)
      }
    },

    'job.filesduration': function (val) {
      var l = $("#datetimepicker1").data("DateTimePicker").date()
      if (l !== null) {
	let date = l.toDate()
	this.datefinish = new Date(date.getTime() + 1000 * val) }
    },

    'job.playnow': function (val) {
      if (val) {
	let nw = new Date()
	this.datefinish = new Date(nw.getTime() + 1000 * this.job.filesduration)
      }
    }

    
  },

  ////
  // End watchers
  ////

  
  ////
  // Methods
  ////
  methods: {

    getUTCDate() {
      return moment($('#datetimepicker1').data("DateTimePicker").date()).utc().format('YYYY-MM-DDTHH:mm:ssZZ')
    },
    
    changeLang(locale) {
      if (['en', 'ar'].includes(locale)) {
	this.$i18n.locale = locale
	localStorage.setItem('lang', locale)
	setTimeout(function(){
	  window.location.reload();
	},100); 
      }
      
    },
    
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

      function shuffle(a) {
	// Fisher–Yates shuffle algorithm
	for (let i = a.length; i; i--) {
          let j = Math.floor(Math.random() * i);
          [a[i - 1], a[j]] = [a[j], a[i - 1]];
	}
      }

      if (this.job.shuffle) {
	shuffle(this.job.files)
      }

      
      let data = {
	stream: {
	  name: this.job.sname
	},
	files: this.job.files,
	streamstart: this.job.playnow ? moment().utc().format('YYYY-MM-DDTHH:mm:ssZZ') : this.getUTCDate(),
	streamfinish: moment(this.datefinish).utc().format('YYYY-MM-DDTHH:mm:ssZZ'),
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
  ////
  // End methods
  ////

  ////
  // Computed data
  ////
  computed: {
    hostname () {
      return location.hostname + ':1935/stream/';
    }

  },
  ////
  // End Computed data
  ////
  

  ////
  // Created hook
  ////
  created() {

    let locale = localStorage.getItem('lang')
    if (locale) {
      // Vue.$i18n.locale is reactive so I can do this
      if (locale && ['en', 'ar'].includes(locale))
	this.$i18n.locale = locale	
    }
    
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
  ////
  // End Created hook
  ////

  
  ////
  // Mounted hook
  ////
  mounted () {
    $('#datetimepicker1').datetimepicker({
      minDate:new Date()
    }).on("dp.change", (dt, oldDate) => {
      let date = dt.date.toDate()
      this.datefinish = new Date(date.getTime() + 1000 * this.job.filesduration)
    })
    console.log(this.$i18n.locale)
    if (this.$i18n.locale === 'ar') {
      require('bootstrap-rtl/dist/css/bootstrap-rtl.css')
    }
    let input = $("#fileinput");
    
    input.fileinput({
      uploadUrl: API_URL + "api/upload",
      multiple: true,
      showUpload: false,
      showRemove: false,
      ajaxSettings: {'headers': {'Authorization': 'Token ' + localStorage.getItem('id_token')}}
    })


    input.on("filebatchselected", function(event, files) {
      // trigger upload method immediately after files are selected
      input.fileinput("upload")
    })


    let vue = this

    // fast hack because bootstrap fileinput events doesn't fireup
    $(document).on('click', '.kv-file-remove', function () {
      let index = $(".kv-file-remove").index(this) / 2
      vue.job.filesduration -= vue.job.files[index].fileduration
      vue.job.files.splice(index, 1)
    })

    
    $('#fileinput').on('fileuploaded', function(event, data, previewId, index) {
      let form = data.form, files = data.files, extra = data.extra, 
	  response = data.response, reader = data.reader;
      var duration = response.duration
      var filehash = response.hashid
      vue.job.activate = false
      let f = {
	fileduration: duration,
	filehash: filehash
      }
      vue.job.filesduration += duration
      vue.job.files.push(f)
    });
  }
  ////
  // End Mounted hook
  ////
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
