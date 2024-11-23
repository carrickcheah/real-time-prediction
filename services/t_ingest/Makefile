run-dev:
	cp dev.env .env
	poetry run python src/main.py

build:
	docker build -t t_ingest .

run: build
	docker run \
		--network=redpanda_network \
		--env-file prod.env \
		t_ingest