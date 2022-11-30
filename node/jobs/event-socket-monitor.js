/**
 * FreeSWITCH event socket monitor.
 * @file: node/jobs/event-socket-monitor.js
*/

const FreeswitchApi = require('../apis/freeswitch');
const ChannelObserver = require('../observers/channel-observer');

const startJob = () => {
    FreeswitchApi.connect()
    .then(connection => {
        // Subscribe to all FreeSWITCH events:
        connection.subscribe(FreeswitchApi.ALL_EVENTS);
        connection.on(FreeswitchApi.Event.RECEIVED, event => {
            // A new FreeSWITCH event has been received!
            ChannelObserver.notify(event)
        });
    })
    .catch(error => {
        // An error connecting to FreeSWITCH occurred!
    });
};

exports.startJob = startJob;