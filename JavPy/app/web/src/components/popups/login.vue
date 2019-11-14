<template>
  <el-dialog title="Password Required" :visible.sync="visible">
    <el-input v-model="password" placeholder="Enter Password" show-password></el-input>
    <div>Just click "Confirm" if you didn't set a password.</div>
    <div slot="footer" class="dialog-footer">
      <el-button type="primary" @click="submitPassword">Confirm</el-button>
    </div>
  </el-dialog>
</template>

<script>
import axios from "axios";
import utils from "../utils.js";
import sha256 from "js-sha256";
import config from "../../config.js";

export default {
  name: "login",
  data() {
    return {
      visible: false,
      message: "",
      password: ""
    };
  },
  methods: {
    submitPassword() {
      axios
        .post(`http://${config.address}:${config.port}/auth_by_password`, {
          password: sha256.sha256(this.password)
        })
        .then(rsp => {
          if (rsp.data === "auth failed") {
            this.$alert("Authentication Failed", "Please Try Again");
          } else {
            utils.setUserpass(rsp.data);
            this.visible = false;
            location.reload();
          }
        });
    },

    isLoggedIn() {
      if (!utils.getUserpass()) {
        this.visible = true;
      }
    }
  },
  created() {
    setInterval(this.isLoggedIn, 1000);
  }
};
</script>

<style lang="less" scoped>
</style>
