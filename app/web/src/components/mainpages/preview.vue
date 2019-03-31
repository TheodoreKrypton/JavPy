<template>
  <div style="text-align: center;" ref="whole">
    <el-alert
      v-if="videos === ''"
      title="Sorry, cannot find any result."
      type="error"
      show-icon
      style="width: 40%; margin-left:auto; margin-right:auto"
    ></el-alert>

    <table v-if="videos != undefined && Object.keys(videos).length > 0" cellspacing="30" style="margin-left: auto; margin-right: auto">
      <tr v-for="i in Math.floor(Object.keys(videos).length / itemPerLine)" :key="i">
        <td v-for="j in itemPerLine" :key="j">
          <showcard style="width:100%;" :video="videos[(i-1)*itemPerLine+j-1]"></showcard>
        </td>
      </tr>
      <tr
        v-if="Object.keys(videos).length-Math.floor(Object.keys(videos).length/itemPerLine)*itemPerLine"
      >
        <td
          v-for="j in Object.keys(videos).length-Math.floor(Object.keys(videos).length/itemPerLine)*itemPerLine"
          :key="j"
        >
          <showcard
            style="width:100%;"
            :video="videos[Math.floor(Object.keys(videos).length/itemPerLine)*itemPerLine+(j-1)]"
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
  props: ["videosProp"],
  data() {
    return {
      page: 0,
      itemPerLine: 3,
      av: this.videosProp
    };
  },
  computed: {
    videos: {
      get() {
        if (!this.av) {
          return this.videosProp;
        } else {
          return this.av;
        }
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
      if (document.compatMode === "CSS1Compat") {
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
    },

    loadMore() {
      Event.$emit("load_more", {
        component: this
      });
    }
  },

  mounted() {
    let self = this;
    this.av = null;
    window.onscroll = function() {
      if (
        self.getScrollHeight() ===
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
