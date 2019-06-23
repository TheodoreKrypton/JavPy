<template>
  <div>
    <el-tag
      :key="tag"
      v-for="tag in categories"
      closable
      :disable-transitions="false"
      @close="handleClose(tag)"
    >
      {{tag}}
    </el-tag>
    <el-input
      class="input-new-tag"
      v-if="inputVisible"
      v-model="inputValue"
      ref="saveTagInput"
      size="small"
      @keyup.enter.native="handleInputConfirm"
      @blur="handleInputConfirm"
    >
    </el-input>
    <el-popover
      placement="bottom"
      width="400"
    >
      <div v-if="availableCategories != undefined">
        <el-button
          v-for="category in availableCategories"
          :key="category"
          size="mini"
        >{{category}}</el-button>
      </div>

      <el-button
        class="button-new-tag"
        size="small"
        slot="reference"
      >+ New Tag</el-button>
    </el-popover>
    <el-button
      type="primary"
      @click="onSearch"
      style="margin-left: 5px"
    >Search</el-button>
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
export default {
  data() {
    return {
      categories: [],
      inputVisible: false
    };
  },
  computed: {
    availableCategories: {
      get() {
        return [];
      }
    }
  },
  methods: {
    handleClose(tag) {
      this.dynamicTags.splice(this.dynamicTags.indexOf(tag), 1);
    },

    handleInputConfirm() {
      let inputValue = this.inputValue;
      if (inputValue) {
        this.dynamicTags.push(inputValue);
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