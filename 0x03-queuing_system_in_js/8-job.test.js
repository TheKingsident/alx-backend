import { expect } from 'chai';
import sinon from 'sinon';
import kue from 'kue';
import createPushNotificationsJobs from './8-job.js';

describe('createPushNotificationsJobs', () => {
  let queue;

  beforeEach(() => {
    queue = kue.createQueue();
    queue.testMode.enter();
  });

  afterEach(() => {
    queue.testMode.clear();
    queue.testMode.exit();
  });

  it('should throw an error if jobs is not an array', () => {
    expect(() => createPushNotificationsJobs(null, queue)).to.throw('Jobs is not an array');
  });

  it('should create jobs with the correct data', () => {
    const jobs = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account',
      },
      {
        phoneNumber: '4153518781',
        message: 'This is the code 4562 to verify your account',
      }
    ];

    createPushNotificationsJobs(jobs, queue);

    expect(queue.testMode.jobs.length).to.equal(2);
    expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
    expect(queue.testMode.jobs[0].data).to.deep.equal(jobs[0]);
    expect(queue.testMode.jobs[1].type).to.equal('push_notification_code_3');
    expect(queue.testMode.jobs[1].data).to.deep.equal(jobs[1]);
  });

  it('should log the correct job creation message', (done) => {
    const jobs = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account',
      },
    ];

    const consoleSpy = sinon.spy(console, 'log');

    createPushNotificationsJobs(jobs, queue);

    queue.testMode.jobs[0].on('enqueue', () => {
      expect(consoleSpy.calledWith(`Notification job created: ${queue.testMode.jobs[0].id}`)).to.be.true;
      consoleSpy.restore();
      done();
    });

    queue.testMode.jobs[0].emit('enqueue');
  });

  it('should log the correct job completion message', (done) => {
    const jobs = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account',
      },
    ];

    const consoleSpy = sinon.spy(console, 'log');

    createPushNotificationsJobs(jobs, queue);

    queue.testMode.jobs[0].on('complete', () => {
      expect(consoleSpy.calledWith(`Notification job ${queue.testMode.jobs[0].id} completed`)).to.be.true;
      consoleSpy.restore();
      done();
    });

    queue.testMode.jobs[0].emit('complete');
  });

  it('should log the correct job failure message', (done) => {
    const jobs = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account',
      },
    ];

    const consoleSpy = sinon.spy(console, 'log');

    createPushNotificationsJobs(jobs, queue);

    queue.testMode.jobs[0].on('failed', (err) => {
      expect(consoleSpy.calledWith(`Notification job ${queue.testMode.jobs[0].id} failed: ${err}`)).to.be.true;
      consoleSpy.restore();
      done();
    });

    queue.testMode.jobs[0].emit('failed', 'Some error');
  });

  it('should log the correct job progress message', (done) => {
    const jobs = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account',
      },
    ];

    const consoleSpy = sinon.spy(console, 'log');

    createPushNotificationsJobs(jobs, queue);

    queue.testMode.jobs[0].on('progress', (progress) => {
      expect(consoleSpy.calledWith(`Notification job ${queue.testMode.jobs[0].id} ${progress}% complete`)).to.be.true;
      consoleSpy.restore();
      done();
    });

    queue.testMode.jobs[0].emit('progress', 50);
  });
});
