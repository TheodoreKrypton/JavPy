import index from "./components/index";
import search from "./components/mainpages/search";
import newlyReleased from "./components/mainpages/newly_released";
import magnet from "./components/mainpages/magnet";

const routers = [
  {
    path: "/",
    component: index,
    children: [
      {
        path: "/",
        component: search
      },
      {
        path: "/search",
        component: search
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
