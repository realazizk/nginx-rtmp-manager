<template>
  <div>
    <div class="container">
      <h2>{{$t('stream.list')}}</h2>
      <ul class="list-group">
	<!-- <router-link :to="{name: 'Player', params: {name: channel.name}}" class="list-group-item" v-for="channel in channels" v-bind:href="channel.name"> -->
	<!--      {{channel.name}} <span class="badge">{{channel.stype}}</span> -->
	<!-- </router-link> -->
	<a class="list-group-item" v-for="channel in channels" v-on:click="play(channel)">
         <router-link :to="{name: 'Stream', params: {id: channel.id}}"> <span class="glyphicon glyphicon-link pull-right"></span></router-link> {{channel.name}}  <span class="badge">{{channel.stype}}</span> <span v-if="channel.live" style="background-color: #d41818" class="badge">{{$t('stream.live')}}</span>
	</a>
      </ul>  
    </div>

    
  </div>
</template>

<script>

import bus from '@/eventbus.js'
import {API_URL, SERVER_URL} from '@/shared.js'
import Hls from 'hls.js'


var component = {
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
    this.$http.get(API_URL + 'api/streams').then(
      response => {
        let data = response.body
        this.channels = data

	
	this.channels.forEach(function (item, index, array){
	  if (item.stype === "audio") {
	    item.stype = vm.$t('stream.audio');
	  } else if (item.stype === "video") {
	    item.stype = vm.$t('stream.video');
	  }
	  vm.$http.get(
	    SERVER_URL +item.name+ '.m3u8'
	  ).then(response => {
	    item.live = true
	    vm.$set(array[index], item)
	  }, response => {
	    item.live = false
	    vm.$set(array[index], item)

	  })
	})
      }
    )

    if(Hls.isSupported()) {
      this.player = new Hls();
    }
    
    bus.$on('toggleplaying',(truth) => {
      vm.toggleplaying(truth)
    })


  },

}


export default component
</script>
