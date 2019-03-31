<template>
  <div>
    <el-table :data="magnet_res" style="width: 100%;" :row-class-name="tableRowClassName">
      <el-table-column prop="description" label="Total Size" width="180"></el-table-column>
      <el-table-column prop="peers" label="Detected Peers" width="180"></el-table-column>
      <el-table-column prop="magnet" label="Magnet Link"></el-table-column>
    </el-table>
  </div>
</template>

<script>
import axios from "axios";
import Event from "../../main.js";
import config from "../../config.js";

export default {
  name: "magnet",
  data() {
    return {
      magnet_res: []
    };
  },
  methods: {
    tableRowClassName({ row, rowIndex }) {
      if (rowIndex % 4 === 1) {
        return "warning-row";
      } else if (rowIndex % 4 === 3) {
        return "success-row";
      }
      return "";
    },

    async onSearch(data) {
      if (Object.keys(data).length === 0) {
        return;
      }
      Event.$emit("begin-loading");

      let rsp = {};

      await axios
        .post(`http://${config.address}:${config.port}/search_magnet_by_code`, {
          code: data.code
        })
        .then(function(response) {
          rsp = response;
        })
        .catch(function() {
          this.magnet_res = "";
        });

      if (Object.keys(rsp).length === 0) {
        Event.$emit("end-loading");
        return;
      }

      if (rsp.status === 200) {
        if (!rsp.data) {
          this.magnet_res = "";
        } else {
          this.magnet_res = rsp.data;
        }
      } else {
        this.magnet_res = "";
      }
      Event.$emit("end-loading");
    }
  },

  watch: {},

  mounted() {
    this.onSearch(this.$route.query);
  }
};
</script>

<style>
.el-table .warning-row {
  background: oldlace;
}

.el-table .success-row {
  background: #f0f9eb;
}
</style>
