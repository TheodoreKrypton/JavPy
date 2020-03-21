import index from "./components/index.vue";
import searchVideo from "./components/mainpages/searchvideo.vue";
import searchActress from "./components/mainpages/searchactress.vue";
import newlyReleased from "./components/mainpages/newly_released.vue";
import magnet from "./components/mainpages/magnet.vue";
import categories from "./components/mainpages/categories.vue";
import videoplayer from "./components/mainpages/videoplayer.vue";
import VueRouter from "vue-router";

const router = new VueRouter({
  mode: "history",
  routes: [
    {
      path: "/",
      component: index,
      children: [
        {
          path: "/",
          redirect: "/search"
        },
        {
          path: "/search",
          redirect: "/search/video"
        },
        {
          path: "/search/video",
          component: searchVideo,
          meta: {
            keepAlive: true
          }
        },
        {
          path: "/search/actress",
          component: searchActress,
          meta: {
            keepAlive: true
          }
        },
        {
          path: "/new",
          component: newlyReleased,
          meta: {
            keepAlive: true
          }
        },
        {
          path: "/magnet",
          component: magnet,
          meta: {
            keepAlive: true
          }
        },
        {
          path: "/categories",
          component: categories,
          meta: {
            keepAlive: true
          }
        }
      ]
    },
    {
      path: "/videoplayer",
      component: videoplayer,
      meta: {
        keepAlive: true
      }
    }
  ]
});

router.beforeEach((to, from, next) => {
  const toDepth = to.path.split('/').length
  const fromDepth = from.path.split('/').length
  if (toDepth < fromDepth) {
    from.meta.keepAlive = false
    to.meta.keepAlive = true
  }
  next()
})

export default router;
