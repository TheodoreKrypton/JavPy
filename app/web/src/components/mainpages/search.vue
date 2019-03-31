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
            v-model="form.allowManyActresses"
            active-color="#13ce66"
            inactive-color="#ff4949"
          ></el-switch>
        </el-form-item>
        <el-form-item>
          <el-input-number
            v-model="form.upTo"
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
    <div v-if="mode.actress && other.history_name && Object.keys(other.history_name).length > 1">
      <el-steps :active="1000" align-center simple>
        <el-step v-for="name in other.history_name" :key="name" :title="name" icon="none" @click.native="onSearch({'actress': name})"></el-step>
      </el-steps>
    </div>
    <preview :videosProp="toBePreviewed"></preview>
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
        allowManyActresses: false,
        upTo: 0
      },
      toBePreviewed: null,
      other: null,
      mode: {
        code: false,
        actress: false
      }
    };
  },
  methods: {
    initPage(){
      this.toBePreviewed = null;
      this.mode.actress = false;
      this.mode.code = false;
    },

    async onSearch(data = null) {
      if (Object.keys(data).length === 0) {
        return;
      }
      this.initPage();

      if (data.actress) {
        this.form.actress = data.actress;
        this.form.code = "";
      }

      if (data.code) {
        this.form.code = data.code;
        this.form.actress = "";
      }

      Event.$emit("begin-loading");
      let rsp = null;
      if (!this.form.code && this.form.actress) {
        await axios
          .post(`http://${config.address}:${config.port}/search_by_actress`, {
            actress: this.form.actress,
            history_name: !this.mode.actress
          })
          .then(function(response) {
            rsp = response;
          })
          .catch(function() {
            this.toBePreviewed = "";
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
            this.toBePreviewed = "";
          });
      } else {
        Event.$emit("end-loading");
        return;
      }
      if (rsp.status === 200) {
        if (!rsp.data) {
          this.toBePreviewed = "";
        } else {
          this.toBePreviewed = rsp.data.videos;
          this.other = rsp.data.other;
          if(this.form.actress){
            this.other.nowViewing = this.form.actress;
            this.mode.actress = true;
          }
        }
      } else {
        this.toBePreviewed = "";
      }
      Event.$emit("end-loading");
    },

    clear() {
      this.form.code = "";
      this.form.actress = "";
    }
  },

  mounted() {
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
.is-wait {
  color: teal;
  border-color: teal;
}

.el-step:hover{
  cursor: pointer;
}

</style>
