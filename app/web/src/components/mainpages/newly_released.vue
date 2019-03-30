<template>
  <preview :videos_prop="to_be_previewed"></preview>
</template>

<script>
import preview from "./preview";
import axios from "axios";
import Event from "../../main.js";
import config from "../../config.js";

export default {
  name: "newly_released",
  components: {
    preview
  },
  data() {
    return {
      to_be_previewed: null
    };
  },

  created: async function() {
    Event.$emit("begin-loading");
    console.log(`http://${config.address}:${config.port}/new`);
    const rsp = await axios.post(`http://${config.address}:${config.port}/new`, {
      page: 0
    });
    if (!rsp.data) {
      this.to_be_previewed = "";
    } else {
      this.to_be_previewed = rsp.data;
    }
    Event.$emit("end-loading");
  }
};
</script>

<style lang="less" scoped>
</style>
