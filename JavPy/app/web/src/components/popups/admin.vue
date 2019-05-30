<template>
  <div style="text-align: center">
    <el-button type="primary" plain @click="authenticationSettings">Authentication</el-button>
  </div>
</template>

<script>
import utils from "../utils.js";

export default {
  name: "admin",
  data() {
    return {};
  },
  methods: {
    async authenticationSettings() {
      let ipBlacklist = [];
      let ipWhitelist = [];
      await utils.pookie("/get_config").then(rsp => {
        if (rsp.status === 200) {
          ipBlacklist = rsp.data["ip-blacklist"];
          ipWhitelist = rsp.data["ip-whitelist"];
        }
      });

      const h = this.$createElement;
      this.$msgbox({
        title: "Authentication Settings",
        message: h("form", null, [
          h("label", null, "New Password: "),
          h(
            "input",
            {
              type: "text",
              style: "width: 100%; clear: both",
              ref: "password"
            },
            ""
          ),
          h("br", null, ""),
          h("label", null, "IP Blacklist: "),
          h(
            "textarea",
            {
              disabled: true,
              style: "overflow-y: auto; width: 100%; clear: both",
              ref: "ipBlacklist"
            },
            "Under Construction"
            // ipBlacklist.join("\n")
          ),
          h("br", null, ""),
          h("label", null, "IP Whitelist: "),
          h(
            "textarea",
            {
              style: "overflow-y: auto; width: 100%; clear: both",
              ref: "ipWhitelist"
            },
            ipWhitelist.join("\n")
          )
        ]),
        showCancelButton: true,
        confirmButtonText: "Confirm",
        cancelButtonText: "Cancel",
        beforeClose: async (action, instance, done) => {
          let self = this;
          if (action === "confirm") {
            instance.confirmButtonLoading = true;
            instance.confirmButtonText = "Updating...";
            await utils.pookie("/update_config", {
              password: self.$refs.password.value,
              ipBlacklist: self.$refs.ipBlacklist.value.split("\n"),
              ipWhitelist: self.$refs.ipWhitelist.value.split("\n")
            });
            instance.confirmButtonLoading = false;
            done();
          } else {
            instance.confirmButtonLoading = false;
            done();
          }
        }
      }).then(action => {
        this.$message({
          type: "info",
          message: "action: " + action
        });
      });
    }
  },
  created() {}
};
</script>

<style lang="less" scoped>
</style>
