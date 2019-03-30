<template>
  <div>
    <div>
      <el-form ref="form" :model="form" :inline="true">
        <el-form-item>
          <el-input v-model="form.code" placeholder="Jav Code"></el-input>
        </el-form-item>
        <el-form-item>
          <el-input v-model="form.actress" placeholder="Actress"></el-input>
        </el-form-item>
        <el-form-item>
          <el-switch
            v-model="form.allow_many_actresses"
            active-color="#13ce66"
            inactive-color="#ff4949"
          ></el-switch>
        </el-form-item>
        <el-form-item>
          <el-input-number
            v-model="form.up_to"
            controls-position="right"
            :min="1"
            label="Count"
            size="mini"
            style="width: 80px"
          ></el-input-number>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="onSearch">Search!</el-button>
          <el-button @click="clear">Clear</el-button>
        </el-form-item>
      </el-form>
    </div>
    <preview :videos_prop="to_be_previewed"></preview>
  </div>
</template>

<script>
import axios from "axios";
import preview from "./preview";
import Event from "../../main.js";
import config from "../../config.js";

export default {
  name: "search",
  components: {
    preview
  },
  data() {
    return {
      form: {
        code: "",
        actress: "",
        allow_many_actresses: false,
        up_to: 0
      },
      to_be_previewed: null,
      isPreviewLoading: false
    };
  },
  methods: {
    async onSearch(data = null) {
      if (Object.keys(data).length === 0) {
        return;
      }
      this.to_be_previewed = null;
      if (data.actress) {
        this.form.actress = data.actress;
      }

      if (data.code) {
        this.form.code = data.code;
      }

      Event.$emit("begin-loading");
      let rsp = null;
      if (!this.form.code && this.form.actress) {
        await axios
          .post(`http://${config.address}:${config.port}/search_by_actress`, {
            actress: this.form.actress
          })
          .then(function(response) {
            rsp = response;
          })
          .catch(function() {
            this.to_be_previewed = "";
          });
      } else if (!this.form.actress && this.form.code) {
        await axios
          .post(`http://${config.address}:${config.port}/search_by_code`, {
            code: this.form.code
          })
          .then(function(response) {
            rsp = response;
          })
          .catch(function() {
            this.to_be_previewed = "";
          });
      } else {
        Event.$emit("end-loading");
        this.clear();
        return;
      }
      if (rsp.status === 200) {
        if (!rsp.data) {
          this.to_be_previewed = "";
        } else {
          this.to_be_previewed = rsp.data;
        }
      } else {
        this.to_be_previewed = "";
      }
      Event.$emit("end-loading");
      this.clear();
    },

    clear() {
      this.form.code = "";
      this.form.actress = "";
    }
  },

  mounted: function() {
    this.onSearch(this.$route.query);
  },

  watch: {
    $route(to, from) {
      this.onSearch(this.$route.query);
    }
  }
};
</script>

<style lang="less" scoped>
</style>
