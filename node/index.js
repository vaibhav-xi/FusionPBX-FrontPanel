/**
 * FreeSWITCH listener app launcher.
 * @file: node/index.js
 */

const EventSocketMonitor = require('./jobs/event-socket-monitor');
const FreeswitchApi = require('../apis/freeswitch');
// Start listening FreeSWITCH events:
EventSocketMonitor.startJob();

const execute = (command) => new Promise((resolve, reject) => {
    connect()
    .then(connection => {
        connection.bgapi(command, response => {
            const responseBody = response.getBody();
            resolve(responseBody);
        });
    })
    .catch(error => {
        reject(error);
    });
});

execute("uuid_getvar");