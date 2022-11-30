/**
 * FreeSWITCH API.
 * @file: node/apis/freeswitch.js
 */

 const ESL = require('modesl');

 const FreeswitchConfig = require('../config/config.js').getConfig('freeswitch');
 
 const Event = {
     Connection: {
         READY: 'esl::ready',
         CLOSED: 'esl::end',
         ERROR: 'error',
     },
     RECEIVED: 'esl::event::*::*',
 };
 const ALL_EVENTS = 'all';
 const DTMF_EVENTS = 'DTMF';
 let connection = null;
 
 const connect = () => new Promise((resolve, reject) => {
     if (connection !== null && connection.connected()) {
         resolve(connection);
     } else {
         // Opening new FreeSWITCH event socket connection...
         connection = new ESL.Connection(FreeswitchConfig.ip, FreeswitchConfig.port, FreeswitchConfig.password);
         connection.on(Event.Connection.ERROR, () => {
             // Error connecting to FreeSWITCH!
             reject('Connection error');
         });
         connection.on(Event.Connection.CLOSED, () => {
             // Connection to FreeSWITCH closed!
             reject('Connection closed');
         });
         connection.on(Event.Connection.READY, () => {
             // Connection to FreeSWITCH established!
             resolve(connection);
         });
     }
 });
 
 exports.ALL_EVENTS = ALL_EVENTS;
 exports.DTMF_EVENTS = DTMF_EVENTS;
 exports.Event = Event;
 exports.connect = connect;