import express from 'express';
import kue from 'kue';
import { promisify } from 'util';
import redis from 'redis';

// Create a Redis client
const client = redis.createClient();
const reserveSeatAsync = promisify(client.set).bind(client);
const getCurrentAvailableSeatsAsync = promisify(client.get).bind(client);

// Set the initial number of available seats
reserveSeatAsync('available_seats', 50);

// Initialize reservation status
let reservationEnabled = true;

// Create a Kue queue
const queue = kue.createQueue();

// Create express server
const app = express();
const PORT = 1245;

// Route to get the number of available seats
app.get('/available_seats', async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeatsAsync('available_seats');
  res.json({ numberOfAvailableSeats });
});

// Route to reserve a seat
app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  }

  const job = queue.create('reserve_seat').save((err) => {
    if (err) {
      return res.json({ status: 'Reservation failed' });
    }
    res.json({ status: 'Reservation in process' });
  });

  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (err) => {
    console.log(`Seat reservation job ${job.id} failed: ${err.message}`)
  });
});

// Route to process the reservation queue
app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  const numberOfAvailableSeats = await getCurrentAvailableSeatsAsync('available_seats');
  if (numberOfAvailableSeats <= 0) {
    reservationEnabled = false;
    return;
  }

  await reserveSeatAsync('available_seats', numberOfAvailableSeats - 1);
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
