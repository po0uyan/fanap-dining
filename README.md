# fanap-dining
an implementation of fanap-dining telegram bot service for easy access for employees the main service is hosted on [dining.fanap.ir](dining.fanap.ir)

this project uses python-rq so you need to implement a scaled rq service for this project to work.
daemonize your service using systemd, supervisord or any other similar service.
register your id for the bot and then it'll be all available for your reservation.

