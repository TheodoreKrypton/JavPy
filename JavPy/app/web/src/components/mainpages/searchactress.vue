<template>
  <div>
    <searchbar></searchbar>
    <div v-if="other && other.history_name && Object.keys(other.history_name).length > 1">
      <el-steps :active="1000" align-center simple>
        <el-step
          v-for="name in other.history_name"
          :key="name"
          :title="name"
          icon="none"
          @click.native="onSearch({actress: name, historyNameRequired: 'false'})"
        ></el-step>
      </el-steps>
    </div>
    <preview :videosProp="toBePreviewed"></preview>
  </div>
</template>
<script>
import searchbar from "./searchbar";
import preview from "./preview";
import Event from "../../main.js";
import utils from "../utils.js";

export default {
  name: "searchActress",
  components: {
    searchbar,
    preview
  },
  data() {
    return {
      toBePreviewed: null,
      other: null
    };
  },
  methods: {
    initPage() {
      this.toBePreviewed = null;
    },

    async onSearch(data = null) {
      this.initPage();

      if (Object.keys(data).length === 0) {
        return;
      }

      Event.$emit("begin-loading");
      let rsp = await utils
        .pookie("/search_by_actress", {
          actress: data.actress,
          history_name: data.historyNameRequired
        })
        .finally(() => {
          Event.$emit("end-loading");
        });
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
