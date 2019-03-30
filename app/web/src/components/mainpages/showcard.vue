<template>
  <el-card shadow="hover" style="width: 30%;" body-style="padding: 0">
    <div slot="header" class="clearfix">{{video.title}}</div>
    <img :src="video.preview_img_url" class="image" alt="preview" @click="action()">
    <div class="bottom">
      <table style="display: inline; float: left">
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
                <el-button type="danger" plain slot="reference">Expand</el-button>
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
      <table style="display: inline; float: right; vertical-align: bottom; bottom: 0">
        <tr>
          <el-tag size="mini" type="danger">{{video.release_date}}</el-tag>
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
    },
    action() {
      if (this.video.video_url) {
        this.onWatch(this.video.video_url);
      } else {
        this.onSearch({ code: this.video.code });
      }
    }
  }
};
</script>

<style lang="less" scoped>
.bottom {
  bottom: 0;
}

.image {
  width: 100%;
}

.image:hover {
  cursor: pointer;
}

.el-button {
  margin-left: 0;
  padding: 10px;
}

td {
  padding: 0;
}

.el-tag {
  font-size: 14px;
  padding: 10;
}
</style>