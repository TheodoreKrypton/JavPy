<template>
  <el-card shadow="hover" style="width: 30%;" body-style="padding: 0">
    <img :src="video.preview_img_url" class="image" alt="preview">
    <div class="bottom">
      <table>
        <tr>
          <td v-if="video.actress">
            <el-button
              type="primary"
              plain
              style="float: left;"
              @click="onSearch({actress: video.actress})"
            >{{video.actress}}</el-button>
          </td>
          <td v-if="video.video_url">
            <el-popover placement="bottom-end" trigger="hover">
              <el-button type="primary" plain @click="onWatch(url)">Watch</el-button>
              <el-button type="primary" plain @click="onMagnet({code: video.code})">Magnet</el-button>
              <el-button type="primary" plain slot="reference">{{video.code}}</el-button>
            </el-popover>
          </td>
          <td v-else>
            <el-button
              type="primary"
              plain
              style="float: right;"
              @click="onSearch({code: video.code})"
            >{{video.code}}</el-button>
          </td>
        </tr>
      </table>
    </div>
  </el-card>
</template>

<script>
import Event from "../../main.js";

export default {
  name: "showcard",
  props: ["video"],
  methods: {
    onWatch(url) {
      window.open(url);
    },
    onSearch(video) {
      Event.$emit("search_jav", video);
    },
    onMagnet(video) {
      Event.$emit("search_magnet_by_code", video);
    }
  }
};
</script>

<style lang="less" scoped>
.image {
  width: 100%;
}
</style>