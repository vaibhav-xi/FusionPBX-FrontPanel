
/**
 * Get FreeSWITCH channel variable use case.
 * @file: node/use-cases/get-channel-variable.js
 */

 const FreeswitchApi = require('../apis/freeswitch');

 const execute = (uuid, variable) => new Promise((resolve, reject) => {
     FreeswitchApi.execute(`uuid_getvar ${uuid} ${variable}`)
     .then(value => {
         resolve(value);
         console.log(value);
     })
     .catch(error => {
         reject(error);
     });
 });

 const test = () => new Promise((resolve, reject) => {
    FreeswitchApi.execute(`uuid_getvar`)
    .then(value => {
        resolve(value);
        console.log(value);
    })
    .catch(error => {
        reject(error);
    });
});

 test();
 
 exports.execute = execute;