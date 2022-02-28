import {io} from "socket.io-client";
import {readable} from "svelte/store";


const socket = io('/', {
    path: '/../token-manager-api/ws/socket.io',
    transports: ['polling']
});

socket.on('connect', function (event) {
    console.log('user is connected now');
    // socket.emit('client_connect_event', {data: 'User connected'});
});

export const writerStatus = readable("error", set => {
    socket.on('writer_status', function (msg, cb) {
        if (msg.status == "idle") {
            set("idle");
        } else if (msg.status == "success") {
            set("success");
            setTimeout(() => {
                set("idle");
            }, 2000);
        } else {
            set("error");
        }
    });
});

export {socket};
