<template>
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

        <audio id="audio"></audio>
    </div>
</template>

<script>

 const API_URL = 'http://localhost:8080/'

 export default {
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
       this.player.loadSource('http://192.168.100.3/stream/' +stream.name+ '.m3u8');
       this.player.on(Hls.Events.MANIFEST_PARSED, function() {
         audio.play();
       });
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
    }
  }
</script>
