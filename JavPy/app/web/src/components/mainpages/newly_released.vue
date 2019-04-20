<template>
  <preview :videosProp="toBePreviewed"></preview>
</template>

<script>
import preview from "./preview";
import pookie from "../utils.js";
import Event from "../../main.js";

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
    const rsp = await pookie("/new", {
      page: 1
    }).finally(() => {
      Event.$emit("end-loading");
    });
    if (!rsp.data) {
      this.toBePreviewed = "";
    } else {
      this.toBePreviewed = rsp.data;
    }
  }
};
</script>

<style lang="less" scoped>
</style>
