import os
import json

# CREATE
def create_status_file(status_file_path, server, workers):
    data = {
        workers: [
            {
                "server_name": server,
                "status": "idle",
                "file": "none"
            }
        ]
    }
    with open(status_file_path, 'w') as status_file:
        json.dump(data, status_file, indent=4)
        status_file.write('\n')

# UPDATE
def update_status_file(status_file_path, server, key, value, workers):
    with open(status_file_path, 'r') as status_file:
        data = json.load(status_file)
    for worker in data[workers]:
        if worker['server_name'] == server:
            worker[key] = value
            break
    with open(status_file_path, 'w') as status_file:
        json.dump(data, status_file, indent=4)
        status_file.write('\n')

# ADD
def add_server_to_status_file(status_file_path, server, workers):
    with open(status_file_path, 'r') as status_file:
        data = json.load(status_file)
    new_server = {
        "server_name": server,
        "status": "idle",
        "file": "none"
    }
    data[workers].append(new_server)
    with open(status_file_path, 'w') as status_file:
        json.dump(data, status_file, indent=4)
        status_file.write('\n')

# VERIFY
def verify_server_in_status_file(status_file_path, server, workers):
    check = False
    with open(status_file_path, 'r') as status_file:
        data = json.load(status_file)
    for worker in data[workers]:
        if worker['server_name'] == server:
            check = True
            break
    return check


videos_parent_path = "/home/avelis/vilicus/"
status_filename = "vilicus_status.json"
workers = 'vilicus_workers'
status_file_path = videos_parent_path + status_filename

create_status_file(status_file_path, os.uname().nodename, workers)
update_status_file(status_file_path, os.uname().nodename, 'status', 'manifest', workers)
if verify_server_in_status_file(status_file_path, 'good-server', workers) == False:
    add_server_to_status_file(status_file_path, 'good-server', workers)
