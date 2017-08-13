<template>
    <div id="player"></div>

</template>

<script>
  export default {
    data () {
      return {
        d: this.$route.params.name,
        player: undefined
      }
    },

    created() {
      this.player = jwplayer('player').setup({
        file: 'http://192.168.100.2/stream/' + this.d +'.m3u8',
        volume: 10,
        logo: {
	        hide: true,
	      },
        //      width: 640,
        //      height: 40
      });
    },

    mounted() {

    }
  }
</script>
