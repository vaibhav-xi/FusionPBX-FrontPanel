/**
 * FreeSWITCH Config.
 * @file: node/config/config.js
 */

 const configParams = {
    freeswitch: {
        ip: '167.99.241.212',
        port: 5080,
        password: '@0249Vaibhav',
    },
};

const getConfig = module => (configParams[module] !== undefined) ? configParams[module] : {};

exports.getConfig = getConfig;