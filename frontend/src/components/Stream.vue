<template>

    <div class="container">
	<h1>{{stream.name}}</h1> <span v-if="stream.live" style="background-color: #d41818" class="badge">{{$t('stream.live')}}</span>

	<div>Jobs list</div>

	<table class="table table-bordered">
	    <thead>
                <tr>
                    <th>{{$t('onestream.inf')}}</th>
                    <th>{{$t('onestream.taskid')}}</th>
		    <th>{{$t('onestream.streamstart')}}</th>
                </tr>
            </thead>
            <tbody>
		<tr v-for="(row, index) in jobs">
		    <td>{{ row.inf }}</td>
		    <td>{{ row.taskid }}</td>
		    <td>{{ row.streamstart }}</td>	
		</tr>
            </tbody>
        </table>
	
	<div>List Files</div>

	<table class="table table-bordered">
	    <thead>
                <tr>
                    <th>{{$t('onestream.filename')}}</th>
                    <th>{{$t('onestream.fileduration')}}</th>
		    <!-- <th>{{$t('onestream.filedownload')}}</th> -->
                </tr>
            </thead>
            <tbody>
		<tr v-for="(row, index) in files">
		    <td>{{ row.filename }}</td>
		    <td>{{ row.duration }}</td>
		    <!-- <td><a @click="downloadFile(row, index)">{{$t('onestream.filedownload')}}</a></td> -->
		    
		</tr>
            </tbody>
        </table>

	
    </div>
    
    
    
</template>

<script>
import {API_URL, SERVER_URL} from '@/shared.js'
import auth from '@/auth'
import bus from '@/eventbus.js'
import moment from 'moment'
import Hls from 'hls.js'


export default {
  data() {
    return {
      channels: [],
      player: null,
      isplaying: localStorage.getItem('isplaying'),
      jobs: [],
      files: [],
      stream: null
    }
  },

  methods: {
    play (stream) {
      let audio = document.getElementById('audio');
      if (audio.paused || stream.name !== this.isplaying) {
	this.player.attachMedia(audio);
	this.player.loadSource(SERVER_URL +stream.name+ '.m3u8');
	bus.$emit('setplaying', stream.name)
	this.toggleplaying(false)

	this.isplaying = stream.name
	localStorage.setItem('isplaying', stream.name)
	let vm = this
	this.player.on(Hls.Events.MANIFEST_PARSED, function() {
	  bus.$emit('splaying', stream.name)
	  vm.toggleplaying(true, stream.name)
 	});
      }
    }

    ,toggleplaying (truth) {
      let audio = document.getElementById('audio')
      let vm = this
      if (truth) {
	audio.play();
      } else {
	audio.pause();
      }
    },

    downloadFile (row, index) {
      
    }
    
  },

  
  created() {
    let vm = this
    let streamid = this.$route.params.id;

    
    if(Hls.isSupported()) {
      this.player = new Hls();
    }
    
    this.$http.get(API_URL + 'api/stream/' + streamid).then(
      response => {
	let data = response.body

	vm.$http.get(
	  SERVER_URL +data.name+ '.m3u8'
	).then(response => {
	  data.live = true
	}, response => {
	  data.live = false
	})

	vm.stream = data
	
	vm.play({name: data.name})
      }
    )

    bus.$on('toggleplaying',(truth) => {
      vm.toggleplaying(truth)
    })

    this.$http.get(API_URL + 'api/cjobs/' + streamid).then(
      response => {
	let data = response.body
	
	vm.jobs = data
	for (let i = 0; i<vm.jobs.length; i++) {
	  for (let j = 0; j<vm.jobs[i].files.length; j++) {
	    vm.jobs[i].files[j].duration = moment.utc(vm.jobs[i].files[j].duration*1000).format('HH:mm:ss');
	    vm.files.push(vm.jobs[i].files[j])
	    
	  }
	}
      }
    )

    
  }
}
  
</script>


<style scoped>
</style>

