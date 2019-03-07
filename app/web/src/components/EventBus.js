import Vue from "vue";

let EventBus = Vue.extend({
  methods: {
    listen_to_events() {
      this.$on("search_magnet_by_code", function(video) {
        this.$router.push({
          path: "/magnet",
          query: {
            code: video.code
          }
        });
      });

      this.$on("search_jav_by_code", function(video) {
        this.$router.push({
          path: "/search",
          query: {
            code: video.code
          }
        });
      });
    }
  },

  created() {
    this.listen_to_events();
  }
});

export default EventBus;
