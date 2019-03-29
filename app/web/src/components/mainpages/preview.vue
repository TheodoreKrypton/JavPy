<template>
  <div style="text-align: center">
    <el-alert
      v-if="av === ''"
      title="Sorry, cannot find any result."
      type="error"
      description="Please Retry."
      show-icon
    ></el-alert>

    <table v-if="av != undefined && Object.keys(av).length > 0" cellspacing="30">
      <tr v-for="i in parseInt(Object.keys(av).length/item_per_line)" :key="i">
        <td v-for="j in item_per_line" :key="j">
          <showcard style="width:100%;" :video="av[(i-1)*item_per_line+j]"></showcard>
        </td>
      </tr>
      <tr
        v-if="Object.keys(av).length-parseInt(Object.keys(av).length/item_per_line)*item_per_line"
      >
        <td
          v-for="j in Object.keys(av).length-parseInt(Object.keys(av).length/item_per_line)*item_per_line"
          :key="j"
        >
          <showcard
            style="width: 100%"
            :video="av[parseInt(Object.keys(av).length/item_per_line)*item_per_line+(j-1)]"
          ></showcard>
        </td>
      </tr>
    </table>
  </div>
</template>


<script>
import showcard from "./showcard.vue";

export default {
  name: "preview",
  components: {
    showcard
  },
  data() {
    return {
      item_per_line: 3
    };
  },
  props: ["av"]
};
</script>


<style lang="less" scoped>
</style>
