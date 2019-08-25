run-demo:
	pipenv run huey_consumer.py demo.huey -w 2

run-demo-custom-consumer:
	pipenv run python huey_custom_consumer.py demo.huey -w 2