import Vue from "vue";
import utils from "./utils.js";

let EventBus = Vue.extend({
  methods: {
    listenToEvents() {
      this.$on("search_magnet_by_code", function (video) {
        this.$router.push({
          path: "/magnet",
          query: {
            code: video.code
          }
        });
      });

      this.$on("search_by_code", function (data) {
        this.$router.push({
          path: "/search/video",
          query: data
        });
      });

      this.$on("search_by_actress", function (data) {
        this.$router.push({
          path: "/search/actress",
          query: data
        });
      });

      this.$on("load_more", async function (from) {
        const path = location.pathname;
        const component = from.component;
        if (path === "/new") {
          await utils.pookie('/new', {
            page: component.page + 1
          }).then(function (response) {
            if (response.status === 200 && response.data) {
              component.$set(component, "videos", component.videos.concat(response.data));
              component.$set(component, "page", component.page + 1);
              // component.av = component.videos.concat(response.data);
              // component.page += 1;
            }
          });
        }
      });
    }
  },

  created() {
    this.listenToEvents();
  }
});

export default EventBus;
