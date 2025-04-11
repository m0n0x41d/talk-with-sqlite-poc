.PHONY: text-to-sql text-to-code help

help:
	@echo "Available targets:"
	@echo "  text-to-sql   - Run SQL generation script"
	@echo "  text-to-code  - Run code generation script"
	@echo "  help          - Show this help message"

text-to-sql:
	@echo "Running SQL generation script..."
	@uv run text_to_sql.py

text-to-code:
	@echo "Running code generation script..."
	@uv run text_to_code.py