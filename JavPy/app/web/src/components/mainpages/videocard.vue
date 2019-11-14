<template>
  <el-card shadow="none" style="width: 30%;" body-style="padding: 0">
    <div
      style="background-color: #e9eef3; color: teal; padding-bottom: 10px; font-size: 20px;"
    >{{video.title}}</div>
    <el-image :src="video.preview_img_url" class="image" alt="preview" @click="action()" lazy></el-image>

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
                  size="mini"
                  @click="onSearch({actress: one_actress.trim()})"
                  style="display: block; padding: 5px"
                >{{one_actress}}</el-button>
                <el-button type="danger" plain slot="reference">Expand</el-button>
              </el-popover>
            </div>
            <el-button
              v-else
              type="primary"
              plain
              style="float: left;"
              @click="onSearch({actress: video.actress.trim()})"
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
      <table style="display: inline; float: right;">
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
  name: "videocard",
  props: ["video"],

  methods: {
    onWatch(url) {
      window.open(url);
    },
    onSearch(video) {
      if (video.actress) {
        Event.$emit("search_by_actress", {
          actress: video.actress
        });
      } else if (video.code) {
        Event.$emit("search_by_code", {
          code: video.code
        });
      }
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
.el-card:hover {
  box-shadow: 0 1px 6px 0 rgba(32, 33, 36, 20);
}

.bottom {
  background-color: #e9eef3;
  height: 40px;
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