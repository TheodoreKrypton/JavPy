import index from "./components/index";
import searchvideo from "./components/mainpages/searchvideo";
import searchactress from "./components/mainpages/searchactress";
import newlyReleased from "./components/mainpages/newly_released";
import magnet from "./components/mainpages/magnet";

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
        component: searchvideo
      },
      {
        path: "/search/actress",
        component: searchactress
      },
      {
        path: "/new",
        component: newlyReleased
      },
      {
        path: "/magnet",
        component: magnet
      }
    ]
  }
];

export default routers;
