import {io} from "socket.io-client";
import {readable, writable} from "svelte/store";


const socket = io('/', {
    path: '/../token-manager-api/ws/socket.io',
    transports: ['polling']
});


// writerStatus enum type
export enum WriterStatus {
    IDLE = 'idle',
    ERROR = 'error',
    SUCCESS = 'success',
    OFF = 'off',
}

export const writerStatus = writable(WriterStatus.OFF);
socket.on('writer_status', function (msg, cb) {
    console.log('writer_status', msg);
    if (msg.status !== WriterStatus.ERROR) {
        writerStatus.set(msg.status);
    } else {
        writerStatus.set(WriterStatus.ERROR);
    }
});

socket.on('connect', function (event) {
    console.log('user is connected now');
    socket.emit('join', {data: 'User connected'});
});


export {socket};
