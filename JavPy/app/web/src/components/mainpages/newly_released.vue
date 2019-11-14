<template>
  <preview :videos="videos"></preview>
</template>

<script>
import preview from "./preview";
import utils from "../utils.js";
import Event from "../../main.js";

export default {
  name: "newlyReleased",
  components: {
    preview
  },
  data() {
    return {
      videos: null
    };
  },

  async created() {
    Event.$emit("begin-loading");
    const rsp = await utils
      .pookie("/new", {
        page: 1
      })
      .finally(() => {
        Event.$emit("end-loading");
      });
    if (!rsp.data) {
      this.videos = "";
    } else {
      this.videos = rsp.data;
    }
  }
};
</script>

<style lang="less" scoped>
</style>
