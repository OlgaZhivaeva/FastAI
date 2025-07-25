lint: ## Проверяет линтерами код в репозитории
	ruff check ./src

format: ## Запуск автоформатера
	ruff check --fix ./src

help: ## Отображает список доступных команд и их описания
#	@echo "Список доступных команд:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
