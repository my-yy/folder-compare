<template>
  <div class="lazy-audio">
    <el-button v-if="!audioLoaded" @click="loadAudio" icon="el-icon-video-play" size="mini"></el-button>
    <audio v-if="audioLoaded" :src="audioSrc" controls ref="audioPlayer"></audio>
  </div>
</template>

<script>
import web_util from "@/utils/web_util";


export default {
  name: 'Empty',
  components: {},
  props: {
    path: String
  },
  data() {
    return {
      audioLoaded: false,
      audioSrc: ''
    }
  },
  methods: {
    loadAudio() {
      this.audioLoaded = true;
      this.audioSrc = this.get_full_url(this.path);
      this.$nextTick(() => {
        this.playAudio();
      });
    },
    playAudio() {
      const audioPlayer = this.$refs.audioPlayer;
      if (audioPlayer) {
        audioPlayer.play();
      }
    },
    get_full_url(url) {
      return web_util.root_url + "/server" + url
    },
  }
}
</script>
<style scoped>

</style>
