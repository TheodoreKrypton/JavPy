<template>
  <div>
    <el-form
      ref="form"
      :model="form"
      :inline="true"
    >
      <el-form-item>
        <el-input v-model="form.keyword"></el-input>
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
        <el-button
          type="primary"
          @click="onSearch"
        >Search!</el-button>
        <el-button @click="clear">Clear</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>
<script>
import Event from "../../main.js";

export default {
  name: "searchbar",
  data() {
    return {
      form: {
        keyword: "",
        allowManyActresses: false,
        upTo: 0
      }
    };
  },

  methods: {
    onSearch() {
      if (this.form.keyword.includes("-")) {
        Event.$emit("search_by_code", {
          code: this.form.keyword
        });
      } else {
        Event.$emit("search_by_actress", {
          actress: this.form.keyword,
          historyNameRequired: true
        });
      }
    },

    clear() {
      this.form.keyword = "";
    }
  }
};
</script>
<style lang="less" scoped>
</style>
