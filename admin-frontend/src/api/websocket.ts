import {io} from "socket.io-client";

const socket = io('/', {
    path: '/backend/ws/socket.io',
    transports: ['polling']
});

socket.on('connect', function (event) {
    console.log('user is connected now');
});

export {socket};