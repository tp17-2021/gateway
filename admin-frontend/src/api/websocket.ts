import {io} from "socket.io-client";

console.log('ahoj');

const socket = io('/', {
    path: '/../token-manager-api/ws/socket.io',
    transports: ['polling']
});

socket.on('connect', function (event) {
    console.log('user is connected now');
    // socket.emit('client_connect_event', {data: 'User connected'});
});

socket.on('writer_status', function (msg, cb) {
    console.log("--------- writer_status changed", msg, cb);

    if (msg.status == "idle") {
        console.log("+++++++++++++ idle", msg, cb);
        
    } else if (msg.status == "success") {
        console.log("+++++++++++++ success", msg, cb);
    } else {
    }
});

export {socket};
