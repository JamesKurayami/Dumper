SQL Injection Dumper is a Python script designed to test and exploit SQL injection vulnerabilities on websites using a series of SQL payloads. The purpose of this project is to demonstrate how an SQL injection can be used to retrieve sensitive information from a database. The script allows performing several actions:


**Test SQL injection vulnerability: It sends a series of SQL payloads to detect if the application is vulnerable.
Extract database information: Once the vulnerability is confirmed, it can retrieve the target database name.
List database tables: The script allows discovering the tables present in the database.

**Explore table columns: After identifying the tables, it retrieves the columns of each table.

**Dump table data: Finally, the tool extracts the data from vulnerable tables based on the selected columns.


Features:
**SQL injection testing with multiple payload types (Union-based, Boolean-based, etc.).

**Extraction of the database, tables, and columns via injected SQL queries.
Dumping of data from vulnerable tables in raw format.

**Customizable payloads: You can easily add new payloads to the list.

**Command-line interface with color output for better readability of results.


Prerequisites:
Python 3.x
The requests library (install it via pip install requests)


Usage:
Basic Test with Parameters- python Dumper.py https://example.com/news.php?id=1
Payload Test- python Dumper.py https://example.com/news.php?id=1 --file payload_list.txt
Test with -u argument- python Dumper.py -u https://example.com/news.php?id=1


Important Notes:
**Ethical usage: This script is provided for educational purposes. You must obtain explicit authorization before testing any target.

**License: This project is under the MIT license. Use it at your own risk.

**Warning: Using this tool to compromise websites without authorization is illegal and may lead to legal consequences. The author will not be responsible for any malicious use of this code.
