import mainpage from "./components/mainpage";
import index from "./components/index";
import search from "./components/mainpages/search";

const routers = [
  {
    path: "/",
    component: index,
    children: [
      {
        path: "/",
        component: search
      }
    ]
  }
];

export default routers;
