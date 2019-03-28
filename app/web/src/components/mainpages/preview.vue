<template>
  <div style="text-align: center">
    <el-alert
      v-if="av === ''"
      title="Sorry, cannot find any result."
      type="error"
      description="Please Retry."
      show-icon
    ></el-alert>

    <!-- <el-row> -->
    <!-- <el-col :span="6" v-for="(video, i) in av" :key="i" :offset="1"
    style="margin: 0; margin-bottom: 40px;">-->
    <showcard
      :video="video"
      v-for="(video, i) in av"
      :key="i"
      style="margin: 10px; margin-bottom: 40px; max-width: 300px; float: left"
    ></showcard>
    <!-- </el-col> -->
    <!-- </el-row> -->
  </div>
</template>


<script>
import showcard from "./showcard.vue";

export default {
  name: "preview",
  components: {
    showcard
  },
  props: ["av"]
};
</script>


<style lang="less" scoped>
</style>
