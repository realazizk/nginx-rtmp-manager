<template>
  <h1>{{$route.params.id}}</h1>
</template>

<script>
import {API_URL, SERVER_URL} from '@/shared.js'
import auth from '@/auth'
import bus from '@/eventbus.js'


export default {
  data() {
    return {
      channels: [],
      player: null,
      isplaying: localStorage.getItem('isplaying')
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
	vm.play({name: data.name})
      }
    )

    bus.$on('toggleplaying',(truth) => {
      vm.toggleplaying(truth)
    })

    
  }
}
  
</script>


<style scoped>
</style>

