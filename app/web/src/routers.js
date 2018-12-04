import mainpage from "./components/mainpage";
import index from "./components/index";
import search from "./components/mainpages/search";
import newly_released from "./components/mainpages/newly_released"


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
                path: "search",
                component: search
            },
            {
                path: "new",
                component: newly_released
            }
        ]
    }
];

export default routers;
