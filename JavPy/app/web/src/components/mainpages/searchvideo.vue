<template>
  <div>
    <searchbar></searchbar>
    <preview :videos="videos"></preview>
  </div>
</template>

<script>
import preview from "./preview";
import searchbar from "./searchbar";
import Event from "../../main.js";
import utils from "../utils.js";

export default {
  name: "searchVideo",
  components: {
    searchbar,
    preview
  },
  data() {
    return {
      videos: null,
      other: null
    };
  },
  methods: {
    async onSearch(data) {
      if (Object.keys(data).length === 0) {
        return;
      }

      Event.$emit("begin-loading");
      let rsp = await utils
        .pookie("/search_by_code", {
          code: data.code
        })
        .finally(() => {
          Event.$emit("end-loading");
        });
      if (rsp.status === 200) {
        if (!rsp.data) {
          this.videos = "";
        } else {
          this.videos = rsp.data.videos;
          this.other = rsp.data.other;
        }
      } else {
        this.videos = "";
      }
    }
  },

  mounted() {
    this.onSearch(this.$route.query);
  },

  watch: {
    $route(to, from) {
      if (to.path == "/search/video") {
        this.onSearch(this.$route.query);
      }
    }
  }
};
</script>

<style lang="less" scoped>
.is-wait {
  color: teal;
  border-color: teal;
}
</style>
