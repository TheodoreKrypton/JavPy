<template>
  <div id="container">
    <video
      ref="video"
      class="video-js vjs-default-skin"
      controls
      autoplay="muted"
      preload="metadata"
      id="video"
    ></video>
  </div>
</template>

<script>
import videojs from "video.js";

export default {
  name: "videoplayer",
  data() {
    return {
      player: null
    };
  },
  methods: {
    play() {
      if (this.$route.query.video_url) {
        const options = {
          autoplay: true,
          controls: true,
          sources: [
            {
              src: decodeURIComponent(this.$route.query.video_url)
            }
          ],
          techOrder: ["hlsjs", "html5", "flash"]
        };
        this.player = videojs(this.$refs.video, options);
      }
    }
  },
  mounted() {
    this.play();
  },
  watch: {
    $route(to) {
      if (to.path == "/videoplayer") {
        this.play();
      }
    }
  },
  beforeDestroy() {
    if (this.player) {
      this.player.dispose();
    }
  }
};
</script>
<style scoped>
.vjs-default-skin {
  position: fixed;
  right: 0;
  bottom: 0;
  min-width: 100%;
  min-height: 100%;
  width: auto;
  height: auto;
}
</style>