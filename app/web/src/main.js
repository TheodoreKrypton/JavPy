import Vue from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui'
import locale from 'element-ui/lib/locale/lang/en'
import 'element-ui/lib/theme-chalk/index.css'
import './plugins/element.js'

Vue.config.productionTip = false;
Vue.use(ElementUI, { locale });

new Vue({
    el: '#app',
    render: h => h(App),
}).$mount('#app');
