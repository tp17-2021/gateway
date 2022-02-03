// svelte-router documentation https://github.com/jorgegorka/svelte-router
import Home from "./pages/Home.svelte";
import NotFound404 from "./pages/404.svelte";
import Pin from "./pages/Pin.svelte";
import LoggedInHome from "./pages/LoggedInHome.svelte";
import VTStatuses from "./pages/VTStatuses.svelte";
import NFCTags from "./pages/NFCTags.svelte";
import VotingHome from "./pages/VotingHome.svelte";

const routes = [
    {name: '/', component: Home,},
    {
        name: 'gateway',
        nestedRoutes: [
            {name: 'pin', component: Pin},
            {name: 'auth/home', component: LoggedInHome},
            {name: 'auth/statuses', component: VTStatuses},
            {name: 'auth/nfc', component: NFCTags},
            {name: 'auth/voting', component: VotingHome},
        ],
    },
    // custom 404 route
    {
        name: '404',
        path: '404',
        component: NotFound404
    }
]


export {routes}