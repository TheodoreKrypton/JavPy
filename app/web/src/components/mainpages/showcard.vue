<template>
  <el-card shadow="hover" style="width: 30%;" body-style="padding: 0">
    <img :src="video.preview_img_url" class="image" alt="preview">
    <div class="bottom">
      <table>
        <tr>
          <td v-if="video.actress">
            <div v-if="video.actress.indexOf(',') != -1">
              <el-popover placement="bottom-start" trigger="hover">
                <el-button
                  v-for="one_actress in video.actress.split(', ')"
                  :key="one_actress"
                  type="primary"
                  plain
                  @click="onSearch({actress: one_actress})"
                  style="display: block"
                >{{one_actress}}</el-button>
                <el-button type="primary" plain slot="reference">Many Actresses</el-button>
              </el-popover>
            </div>
            <el-button
              v-else
              type="primary"
              plain
              style="float: left;"
              @click="onSearch({actress: video.actress})"
            >{{video.actress}}</el-button>
          </td>
          <td v-if="video.video_url">
            <el-popover placement="bottom-end" trigger="hover">
              <el-button type="primary" plain @click="onWatch(video.video_url)">Watch</el-button>
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

.el-button {
  margin-left: 0;
}
</style>