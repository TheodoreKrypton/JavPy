import Vue from "vue";
import App from "./App.vue";
import ElementUI from "element-ui";
import locale from "element-ui/lib/locale/lang/en";
import "element-ui/lib/theme-chalk/index.css";
import "./plugins/element.js";
import VueRouter from "vue-router";
import routers from "./routers.js";

Vue.config.productionTip = false;
Vue.use(ElementUI, { locale });
Vue.use(VueRouter);

const router = new VueRouter({
  mode: "history",
  routes: routers
});

new Vue({
  el: "#app",
  router,
  render: h => h(App)
}).$mount("#app");
