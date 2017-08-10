<template>
  <div>
    <div class="container">
      <h2>List of streams</h2>
      <ul class="list-group">
	<!-- <router-link :to="{name: 'Player', params: {name: channel.name}}" class="list-group-item" v-for="channel in channels" v-bind:href="channel.name"> -->
	<!--      {{channel.name}} <span class="badge">{{channel.stype}}</span> -->
	<!-- </router-link> -->
	<a class="list-group-item" v-for="channel in channels" v-on:click="play(channel)">
          {{channel.name}} <span class="badge">{{channel.stype}}</span>
	</a>
      </ul>  
    </div>

    
  </div>
</template>

<script>

 const API_URL = 'http://localhost:8080/'
import bus from '@/eventbus.js';

var component = {
  data() {
      return {
        channels: [],
        player: null
      }
    },
   methods: {
     play (stream) {
       let audio = document.getElementById('audio');
       this.player.attachMedia(audio);
       this.player.loadSource('http://192.168.100.2/stream/' +stream.name+ '.m3u8');
       this.player.on(Hls.Events.MANIFEST_PARSED, function() {
	 bus.$emit('splaying', stream.name)
       });
     }

     ,toggleplaying (truth) {
       if (truth) {
	 console.log('play')
	 audio.play();
       } else {
	 console.log('play')
	 audio.pause();
       }
     }

   },

   created() {
      this.$http.get(API_URL + 'api/streams').then(
        response => {
          let data = response.body
          this.channels = data
        }
      )

      if(Hls.isSupported()) {
        this.player = new Hls();
      }

     $('.titleDisplay').text('Not playing')

     bus.$on('toggle-playing', (a) => {
       this.toggleplaying(a)
     })
   },

}



export default component
</script>
