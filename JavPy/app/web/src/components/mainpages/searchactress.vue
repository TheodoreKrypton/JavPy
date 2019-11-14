<template>
  <div>
    <searchbar></searchbar>
    <el-row :gutter="20">
      <el-col :span="16">
        <keep-alive>
          <actressprofile :name="actressName" :info="actressInfo"></actressprofile>
        </keep-alive>
      </el-col>
      <el-col :span="8">
        <div v-if="other && other.history_names && Object.keys(other.history_names).length > 1">
          <div>
            <el-steps direction="vertical" :active="1000">
              <el-step
                v-for="name in other.history_names"
                :key="name"
                :title="name"
                @click.native="onSearch({actress: name, fromHistoryName: true})"
              ></el-step>
            </el-steps>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-divider>Movies</el-divider>
    <preview :videos="videos"></preview>
  </div>
</template>
<script>
import searchbar from "./searchbar";
import preview from "./preview";
import Event from "../../main.js";
import utils from "../utils.js";
import actressprofile from "./actressprofile";

export default {
  name: "searchActress",
  components: {
    searchbar,
    preview,
    actressprofile
  },
  data() {
    return {
      actressName: "",
      videos: null,
      other: null,
      actressInfo: null
    };
  },
  methods: {
    async onSearch(data = null) {
      this.actressName = data.actress;

      if (Object.keys(data).length === 0) {
        return;
      }

      Event.$emit("begin-loading");

      if (data.fromHistoryName) {
        await utils
          .pookie("/search_by_actress", {
            actress: data.actress,
            history_name: "false"
          })
          .then(rsp => {
            if (rsp.status === 200 && rsp.data) {
              this.videos = rsp.data.videos;
            } else {
              this.videos = null;
            }
          })
          .finally(() => {
            Event.$emit("end-loading");
          });
      } else {
        await utils
          .pookie("/search_by_actress", {
            actress: data.actress,
            history_name: "true"
          })
          .then(rsp => {
            if (rsp.status === 200 && rsp.data) {
              this.videos = rsp.data.videos;
              this.other = rsp.data.other;
            }
          })
          .finally(() => {
            Event.$emit("end-loading");
          });
        await utils
          .pookie("/actress_info", { actress: data.actress })
          .then(rsp => {
            if (rsp.status === 200) {
              if (rsp.data) {
                this.actressInfo = rsp.data;
                let set = new Set(this.other.history_names);
                for (let i = 0; i < rsp.data.history_names.length; i++) {
                  set.add(rsp.data.history_names[i]);
                }
                this.other.history_names = [...set];
                for (let i = 0; i < this.other.history_names.length; i++) {
                  utils.globalCache.searchActress[
                    this.other.history_names[i]
                  ] = this.other.history_names;
                }
              }
            }
          });
      }
    }
  },
  mounted() {
    this.onSearch(this.$route.query);
  },

  watch: {
    $route(to, from) {
      if (to.path === "/search/actress") {
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
.el-steps:hover {
  cursor: pointer;
}
</style>
