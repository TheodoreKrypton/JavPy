<template>
  <div>
    <el-tag
      v-for="category in categories"
      :key="category"
      closable
      :disable-transitions="false"
      @close="handleClose(category)"
    >{{category}}</el-tag>

    <el-input
      class="input-new-tag"
      v-if="inputVisible"
      v-model="inputValue"
      ref="saveTagInput"
      size="small"
      @keyup.enter.native="handleInputConfirm"
      @blur="handleInputConfirm"
    ></el-input>
    <el-popover placement="bottom" width="1300">
      <div v-if="availableCategories != undefined">
        <el-button
          v-for="category in availableCategories"
          :key="category"
          size="mini"
          @click="addTag(category)"
        >{{category}}</el-button>
      </div>

      <el-button class="button-new-tag" size="small" slot="reference" @click="onNewTag">+ New Tag</el-button>
    </el-popover>
    <div></div>
    <el-button type="primary" @click="onSearch" style="margin-left: 5px">Search</el-button>
  </div>
</template>

<style>
.el-tag + .el-tag {
  margin-left: 10px;
}
.button-new-tag {
  margin-left: 10px;
  height: 32px;
  line-height: 30px;
  padding-top: 0;
  padding-bottom: 0;
}
.input-new-tag {
  width: 90px;
  margin-left: 10px;
  vertical-align: bottom;
}
</style>

<script>
import utils from "../utils.js";

export default {
  data() {
    return {
      categories: [],
      inputVisible: false,
      availableCategories: []
    };
  },

  methods: {
    onNewTag() {
      if (this.availableCategories.length === 0) {
        utils.pookie("/get_tags").then(rsp => {
          if (rsp && rsp.status === 200) {
            let set = new Set(rsp.data);
            this.availableCategories = set.toJSON();
          }
        });
      } else {
        return;
      }
    },

    addTag(tag) {
      this.categories.push(tag);
    },

    handleClose(tag) {
      this.categories.splice(this.categories.indexOf(tag), 1);
    },

    handleInputConfirm() {
      let inputValue = this.inputValue;
      if (inputValue) {
        this.categories.push(inputValue);
      }
      this.inputVisible = false;
      this.inputValue = "";
    },

    onSearch() {
      return;
    }
  }
};
</script>