function Timer(timerId) {
    this.timerId = timerId;
    this.startTime = null;
    this.intervalId = null;
}

////////////////////// OLD //////////////////////

// Timer.prototype.start = function() {
//     this.startTime = new Date().getTime();

//     this.intervalId = setInterval(() => {
//         const currentTime = new Date().getTime();
//         const elapsedTime = (currentTime - this.startTime) / 1000;

//         // console.log(`Timer ${this.timerId} - Elapsed Time: ${elapsedTime.toFixed(2)} seconds`);
//     }, 1000);
// };

////////////////////// OLD //////////////////////

Timer.prototype.start = function(startTimeInSeconds) {
    // Use the provided start time or default to 0 seconds
    this.startTime = new Date().getTime() - (startTimeInSeconds * 1000);

    this.intervalId = setInterval(() => {
        const currentTime = new Date().getTime();
        const elapsedTime = (currentTime - this.startTime) / 1000;

        // console.log(`Timer ${this.timerId} - Elapsed Time: ${elapsedTime.toFixed(2)} seconds`);
    }, 1000);
};

Timer.prototype.stop = function() {
    clearInterval(this.intervalId);
    console.log(`Timer ${this.timerId} stopped`);
};

Timer.prototype.deleteTimer = function() {
    this.stop();
    console.log(`Timer ${this.timerId} deleted`);
};

// Container to hold timers
const timers = {};

// Function to create a new timer
function createTimer(timerId, startTimeInSeconds) {
    timers[timerId] = new Timer(timerId);
    timers[timerId].start(startTimeInSeconds);
}

// Function to fetch timer status
function fetchTimerStatus(timerId) {
    // console.log("TIMER ID: ", timerId, "TIMERS: ", timers, "TIMER: ", timers[timerId]);
    const timer = timers[timerId];
    if (timer) {
        const currentTime = new Date().getTime();
        const elapsedTime = (currentTime - timer.startTime) / 1000;
        console.log(`Timer ${timerId} - Elapsed Time: ${elapsedTime.toFixed(2)} seconds`);
    } else {
        console.log(`Timer ${timerId} not found`);
    }
}

// Function to delete a timer
function deleteTimer(timerId) {
    const timer = timers[timerId];
    if (timer) {
        timer.deleteTimer();
        delete timers[timerId];
    } else {
        console.log(`Timer ${timerId} not found`);
    }
}

// Example usage:
createTimer(1, 20);
createTimer(2, 0);

// Start the timers
// timers[1].start();
// timers[2].start();

//   // Fetch the status of Timer 1 after 3 seconds
//   setTimeout(() => {
//     fetchTimerStatus(1);
//   }, 3000);

//   // Delete Timer 2 after 5 seconds
//   setTimeout(() => {
//     deleteTimer(2);
//   }, 5000);