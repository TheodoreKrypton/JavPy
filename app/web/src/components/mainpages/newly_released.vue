<template>
  <preview :videos_prop="toBePreviewed"></preview>
</template>

<script>
import preview from "./preview";
import axios from "axios";
import Event from "../../main.js";
import config from "../../config.js";

export default {
  name: "newlyReleased",
  components: {
    preview
  },
  data() {
    return {
      toBePreviewed: null
    };
  },

  async created() {
    Event.$emit("begin-loading");
    const rsp = await axios.post(
      `http://${config.address}:${config.port}/new`,
      {
        page: 0
      }
    );
    if (!rsp.data) {
      this.toBePreviewed = "";
    } else {
      this.toBePreviewed = rsp.data;
    }
    Event.$emit("end-loading");
  }
};
</script>

<style lang="less" scoped>
</style>
