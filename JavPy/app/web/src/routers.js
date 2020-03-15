import index from "./components/index.vue";
import searchVideo from "./components/mainpages/searchvideo.vue";
import searchActress from "./components/mainpages/searchactress.vue";
import newlyReleased from "./components/mainpages/newly_released.vue";
import magnet from "./components/mainpages/magnet.vue";
import categories from "./components/mainpages/categories.vue";
import videoplayer from "./components/mainpages/videoplayer.vue"

const routers = [
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
        component: searchVideo
      },
      {
        path: "/search/actress",
        component: searchActress
      },
      {
        path: "/new",
        component: newlyReleased
      },
      {
        path: "/magnet",
        component: magnet
      },
      {
        path: "/categories",
        component: categories
      }
    ]
  },
  {
    path: "/videoplayer",
    component: videoplayer
  }
];

export default routers;
