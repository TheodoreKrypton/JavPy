<template>
  <div style="text-align: center;" ref="whole">
    <el-alert
      v-if="videos === ''"
      title="Sorry, cannot find any result."
      type="error"
      description="Please Retry."
      show-icon
    ></el-alert>

    <table
      v-if="videos != undefined && Object.keys(videos).length > 0"
      cellspacing="30"
      style="width: 100%"
    >
      <tr v-for="i in Math.floor(Object.keys(videos).length / item_per_line)" :key="i">
        <td v-for="j in item_per_line" :key="j">
          <showcard style="width:100%;" :video="videos[(i-1)*item_per_line+j-1]"></showcard>
        </td>
      </tr>
      <tr
        v-if="Object.keys(videos).length-Math.floor(Object.keys(videos).length/item_per_line)*item_per_line"
      >
        <td
          v-for="j in Object.keys(videos).length-Math.floor(Object.keys(videos).length/item_per_line)*item_per_line"
          :key="j"
        >
          <showcard
            style="width:100%;"
            :video="videos[Math.floor(Object.keys(videos).length/item_per_line)*item_per_line+(j-1)]"
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
  props: ["videos_prop"],
  data() {
    return {
      page: 0,
      item_per_line: 3,
      av: this.videos_prop
    };
  },
  computed: {
    videos: {
      get() {
        if (!this.av) return this.videos_prop;
        else return this.av;
      },
      set(val) {
        this.av = val;
      }
    }
  },
  methods: {
    getDocumentTop() {
      let scrollTop = 0,
        bodyScrollTop = 0,
        documentScrollTop = 0;

      if (document.body) {
        bodyScrollTop = this.$refs.whole.scrollTop;
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
        windowHeight = this.$refs.whole.clientHeight;
      }

      return windowHeight;
    },

    getScrollHeight() {
      let scrollHeight = 0,
        bodyScrollHeight = 0,
        documentScrollHeight = 0;

      if (document.body) {
        bodyScrollHeight = this.$refs.whole.scrollHeight;
      }

      if (document.documentElement) {
        documentScrollHeight = document.documentElement.scrollHeight;
      }
      scrollHeight =
        bodyScrollHeight - documentScrollHeight > 0
          ? bodyScrollHeight
          : documentScrollHeight;
      return scrollHeight;
    },

    loadMore() {
      Event.$emit("load_more", {
        component: this
      });
    }
  },

  mounted() {
    let self = this;
    window.onscroll = function() {
      if (
        self.getScrollHeight() ==
        self.getWindowHeight() + self.getDocumentTop()
      ) {
        self.loadMore();
      }
    };
  }
};
</script>


<style lang="less" scoped>
td {
  max-width: 25vw;
}
</style>
