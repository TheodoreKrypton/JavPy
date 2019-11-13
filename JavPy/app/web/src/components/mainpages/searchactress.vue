<template>
  <div>
    <searchbar></searchbar>
    <el-row :gutter="20">
      <el-col :span="16">
        <actressprofile v-if="actressInfo" :name="actressName" :info="actressInfo"></actressprofile>
      </el-col>
      <el-col :span="8">
        <div v-if="other && other.history_name && Object.keys(other.history_name).length > 1">
          <div>
            <el-steps direction="vertical" :active="1000">
              <el-step
                v-for="name in other.history_name"
                :key="name"
                :title="name"
                @click.native="onSearch({actress: name, historyNameRequired: 'false'})"
              ></el-step>
            </el-steps>
          </div>
          <!-- <el-steps :active="1000" align-center simple>
        <el-step
          v-for="name in other.history_name"
          :key="name"
          :title="name"
          icon="none"
          @click.native="onSearch({actress: name, historyNameRequired: 'false'})"
        ></el-step>
          </el-steps>-->
        </div>
      </el-col>
    </el-row>

    <el-divider>Movies</el-divider>
    <preview :videosProp="toBePreviewed"></preview>
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
      toBePreviewed: null,
      other: null,
      actressInfo: null
    };
  },
  methods: {
    initPage() {
      this.toBePreviewed = null;
    },

    async onSearch(data = null) {
      this.initPage();
      this.actressName = data.actress;

      if (Object.keys(data).length === 0) {
        return;
      }

      Event.$emit("begin-loading");
      await utils
        .pookie("/search_by_actress", {
          actress: data.actress,
          history_name: data.historyNameRequired
        })
        .then(rsp => {
          if (rsp.status === 200) {
            if (!rsp.data) {
              this.toBePreviewed = "";
            } else {
              this.toBePreviewed = rsp.data.videos;
              if (data.historyNameRequired === "true") {
                this.other = rsp.data.other;
              }
            }
          } else {
            this.toBePreviewed = "";
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
            }
          }
        });
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
