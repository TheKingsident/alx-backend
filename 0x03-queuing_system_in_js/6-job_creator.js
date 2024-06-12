import kue from 'kue';

// Create the queue
const queue = kue.createQueue();

// Job data
const jobData = {
  phoneNumber: '1234567890',
  message: 'Hello, this is a notification message',
};

// Create a job in the 'push_notification_code' queue
const job = queue.create('push_notification_code', jobData)
  .save((err) => {
    if (!err) {
      console.log(`Notification job created: ${job.id}`);
    } else {
      console.error(`Failed to create job: ${err.message}`);
    }
  });

// Event listeners for the job
job.on('complete', () => {
  console.log('Notification job completed');
});

job.on('failed', () => {
  console.log('Notification job failed');
});
