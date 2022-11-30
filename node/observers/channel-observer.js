/**
 * Channel event observer.
 * @file: node/observers/channel-observer.js
 */

 const Event = {
    Channel: {
        CREATE: 'CHANNEL_CREATE',
        HANGUP: 'CHANNEL_HANGUP',
    },
};

const notify = (event) => {
    const eventName = event.getHeader('Event-Name');
    switch (eventName) {
        case Event.Channel.CREATE:
            const uuid = event.getHeader('Unique-ID');
            const answerState = event.getHeader('Answer-State');
            const callDirection = event.getHeader('Call-Direction');
            // ...
            break;
        case Event.Channel.HANGUP:
            const hangupCause = event.getHeader('Hangup-Cause');
            // ...
            break;
        default:
            // A new unhandled event has been received...
            break;
    }
};

exports.notify = notify;