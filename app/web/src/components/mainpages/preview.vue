<template>
  <div style="text-align: center;">
    <el-alert
      v-if="av === ''"
      title="Sorry, cannot find any result."
      type="error"
      description="Please Retry."
      show-icon
    ></el-alert>

    <table v-if="av != undefined && Object.keys(av).length > 0" cellspacing="30">
      <tr v-for="i in Math.floor(Object.keys(av).length / item_per_line)" :key="i">
        <td v-for="j in item_per_line" :key="j">
          <showcard style="width:100%;" :video="av[(i-1)*item_per_line+j-1]"></showcard>
        </td>
      </tr>
      <tr
        v-if="Object.keys(av).length-Math.floor(Object.keys(av).length/item_per_line)*item_per_line"
      >
        <td
          v-for="j in Object.keys(av).length-Math.floor(Object.keys(av).length/item_per_line)*item_per_line"
          :key="j"
        >
          <showcard
            style="width: 100%"
            :video="av[Math.floor(Object.keys(av).length/item_per_line)*item_per_line+(j-1)]"
          ></showcard>
        </td>
      </tr>
    </table>
  </div>
</template>


<script>
import showcard from "./showcard.vue";
import Event from "../../main.js";

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
  props: ["av"],
  methods: {
    getDocumentTop() {
      let scrollTop = 0,
        bodyScrollTop = 0,
        documentScrollTop = 0;

      if (document.body) {
        bodyScrollTop = document.body.scrollTop;
      }

      if (document.documentElement) {
        documentScrollTop = document.documentElement.scrollTop;
      }

      scrollTop =
        bodyScrollTop - documentScrollTop > 0
          ? bodyScrollTop
          : documentScrollTop;
      return scrollTop;
    },
    getWindowHeight() {
      let windowHeight = 0;
      if (document.compatMode == "CSS1Compat") {
        windowHeight = document.documentElement.clientHeight;
      } else {
        windowHeight = document.body.clientHeight;
      }

      return windowHeight;
    },

    getScrollHeight() {
      let scrollHeight = 0,
        bodyScrollHeight = 0,
        documentScrollHeight = 0;

      if (document.body) {
        bodyScrollHeight = document.body.scrollHeight;
      }

      if (document.documentElement) {
        documentScrollHeight = document.documentElement.scrollHeight;
      }
      scrollHeight =
        bodyScrollHeight - documentScrollHeight > 0
          ? bodyScrollHeight
          : documentScrollHeight;
      return scrollHeight;
    }
  },

  mounted() {
    let self = this;
    window.onscroll = function() {
      if (
        self.getScrollHeight() ==
        self.getWindowHeight() + self.getDocumentTop()
      ) {
        Event.$emit("load_more", {
          component: self,
          path: location.pathname
        });
      }
    };
  }
};
</script>


<style lang="less" scoped>
td {
  max-width: 30vw;
}
</style>
