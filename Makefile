requirements:
	@echo Installing requirements...
	python3 -m pip install -r requirements.txt

install: requirements
	@echo Adding to the crontab to run daily at 9am...
	(crontab -l; echo "0 9 * * * python3 $(CURDIR)/task_bot.py $(CURDIR)/api_keys.json") | crontab -
