<template>
  <el-dialog title="Password Required" :visible.sync="visible">
    <el-input v-model="password" placeholder="Enter Password" show-password></el-input>
    <div slot="footer" class="dialog-footer">
      <el-button type="primary" @click="submitPassword">Confirm</el-button>
    </div>
  </el-dialog>
</template>

<script>
import axios from "axios";
import sha256 from "js-sha256";
import config from "../../config.js";

export default {
  name: "login",
  data() {
    return {
      visible: true,
      message: "",
      password: ""
    };
  },
  methods: {
    submitPassword: function() {
      axios
        .post(`http://${config.address}:${config.port}/auth_by_password`, {
          password: sha256.sha256(this.password)
        })
        .then(rsp => {
          if (rsp.data === "auth failed") {
            this.$alert("Authentication Failed", "Please Try Again");
          } else {
            this.$cookies.set("userpass", rsp.data, 0);
            this.visible = false;
          }
        });
    }
  }
};
</script>

<style lang="less" scoped>
</style>
