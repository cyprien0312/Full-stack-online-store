.PHONY: elt-up elt-run elt-tables elt-preview

elt-up:
	docker compose up -d --build backend db elt

elt-run:
	docker compose exec elt bash -lc "python flows/users_flow.py && cd dbt_project && export DBT_PROFILES_DIR=. && dbt deps && dbt run"

elt-tables:
	docker compose exec elt python scripts/show_tables.py

elt-preview:
	docker compose exec elt python scripts/preview_users.py


