# vote-app-django

# Introduction

This is a Django Rest Framework voting app.
Users can create plans, register, vote on a plan, and view the results.

## Project Structure

The project is organized into three directories:

- **core:** Core files like `settings.py`.
- **plan:** views, models, and other components related to plans.
- **user:** views, models, and other components related to users.

## Execution

To serve the app, build the `docker-compose.yaml` file by running:

```bash
docker compose build
docker compose up -d
```

I've chosen not to include .env in the .gitignore file for easier Docker Compose builds.

To receive test results for the app's main APIs, run:

```bash
python manage.py test
```

## Code Description

Given the potential impact of processing millions of requests on performance, I opted to implement the CQRS pattern. While I considered storing the average and total votes in the plans table as well, I determined it unnecessary since both are housed in the same database. There seemed to be no risk of inconsistency regarding the table that records the average and total votes for each plan.

To prevent excessive requests from users, I implemented rate limiting. Since Django Rest Framework throttles manage rate limits effectively, I opted not to use other rate-limiting packages like Django Rate Limit's decorators. I established four types of throttles:

1. Restrict unauthenticated users from voting requests, even if they are stopped by auth middleware.
2. Limit individual users from voting multiple times within a specific timeframe.
3. Prevent multiple submissions of votes 1 and 2 within a specific duration for a particular plan.
4. Prevent multiple submissions of votes 4 and 5 within a specific duration for a specific plan.

I had some additional ideas but was uncertain if they aligned with the primary goals of the task.

One concept was to handle voting requests asynchronously, processing them in a lazy manner. For example, I could utilize caching to store vote requests and update the database every two minutes.

On a more complex scale, I could consider using Kafka or RabbitMQ for a queue mechanism, allowing concurrent request handling across multiple threads.
