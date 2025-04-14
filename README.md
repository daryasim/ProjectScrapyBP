## Installation and Setup

* Clone/download the project from the repository.
* Download and install Python [from the official website](https://www.python.org/downloads/).
* Download and install [SQLite database browser](https://sqlitebrowser.org/dl/).
* Navigate to the project directory using the command line or terminal and create + activate a virtual environment using the following command:

```bash
python -m venv .venv
#activation on Windows
.\.venv\Scripts\activate
#activation on MacOS/Linux
source .venv/bin/activate
```
* Install dependencies:
```bash
pip install -r requirements.txt
```
* To run all spiders at once, navigate to the folder containing the *spiders_run.py* file and enter the following command:
```bash
python spiders_run.py
```
* To run a specific spider, navigate to the */spiders* folder and enter the following command (replace *spider_name* with the name of the spider):
```bash
scrapy crawl spider_name
```
* To check the list of target websites (add/remove), go to the *websites.json* file.
* To view the collected text data, open the database file *data.db* using the previously installed tool.
## Scheduling Spider Runs
* For Windows: Open Task Scheduler, and under the *Actions* section, click *Create Basic Task*. Then choose the interval and time to run the task and add the *schedule_spiders.bat* file (make sure to replace the path in the file with the correct path based on the location of your project on your system). When the set time is reached, the terminal will open and the spiders will be run.

