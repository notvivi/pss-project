#!/usr/bin/env python3

import telnetlib
import json
import time


class Router:
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password

    def display(self):
        print(self)


def main_loop(routers):
    running = True
    commands = ["help", "ntp", "exit", "globalconfig"]

    while running:
        command = input("Enter command, use help for listing all usable commands>>").lower()
        if command == "help":
            print("All usable commands:")
            for command in commands:
                print(command)
        elif command == "ntp":
            answer = input("add/delete/show>>").lower()
            if answer == "add":
                ntp_add(routers)
            elif answer == "delete":
                ntp_delete(routers)
            elif answer == "show":
                ntp_show(routers)
            else:
                print("Unknown command, returning to start.")
        elif command == "globalconfig":
            global_standard_config(routers)
        elif command == "exit":
            running = False
        else:
            print("Unknown command, try again.")

def ntp_delete(routers):
    ntp_ip = input("Enter ntp ip address that you want to delete")

    for router in routers:
        try:
            tn = telnetlib.Telnet(router.ip, timeout=10)
            tn.read_until(b"Username: ")
            tn.write(router.username.encode('ascii') + b"\n")
            tn.read_until(b"Password: ")
            tn.write(router.password.encode('ascii') + b"\n")
            tn.write(b"conf t\n")
            time.sleep(1)
            tn.write(f"no ntp server {ntp_ip}\n".encode('ascii'))
            time.sleep(1)
            tn.write(b"exit\n")
            time.sleep(1)
            tn.write(b"wr\n")
            time.sleep(1)
            print(f"{ntp_ip} for {router.ip} has been deleted")

        except Exception as e:
            print(f"Failed to connect to {router.ip}: {e}")


def ntp_show(routers):
    for router in routers:
        try:
            tn = telnetlib.Telnet(router.ip, timeout=10)
            tn.read_until(b"Username: ")
            tn.write(router.username.encode('ascii') + b"\n")
            tn.read_until(b"Password: ")
            tn.write(router.password.encode('ascii') + b"\n")
            tn.write(b"sh run | i ntp\n")
            time.sleep(1)
            tn.write(b"exit\n")
            time.sleep(1)
            output = tn.read_very_eager().decode('ascii')
            ntp_lines = [line for line in output.splitlines() if "ntp server" in line]
            print(f"NTP servers for {router.ip}:")
            for line in ntp_lines:
                print(line)
        except Exception as e:
            print(f"Failed to connect to {router.ip}: {e}")


def ntp_add(routers):
    npt_ip = input("Choose your ntp server ip>>")

    for router in routers:
        print(f"Connecting to {router.ip}...")
        try:
            tn = telnetlib.Telnet(router.ip, timeout=10)
            tn.read_until(b"Username: ")
            tn.write(router.username.encode('ascii') + b"\n")
            tn.read_until(b"Password: ")
            tn.write(router.password.encode('ascii') + b"\n")
            tn.write(b"conf t\n")
            time.sleep(1)

            tn.write(b"clock timezone CET 1 0\n")
            time.sleep(1)
            tn.write(b"clock summer-time CEST recurring last Sun Mar 2:00 last Sun Oct 3:00\n")
            time.sleep(1)
            tn.write(f"ntp server {npt_ip}\n".encode('ascii'))
            time.sleep(1)
            tn.write(b"exit\n")
            time.sleep(1)
            tn.write(b"wr\n")
            time.sleep(1)
            output = tn.read_very_eager().decode('ascii')
            print(f"Output for {router.ip}: {output}")
        except Exception as e:
            print(f"Failed to connect to {router.ip}: {e}")


def global_standard_config(routers):
    for router in routers:
        print(f"Connecting to {router.ip}...")
        try:
            tn = telnetlib.Telnet(router.ip, timeout=10)
            tn.read_until(b"Username: ")
            tn.write(router.username.encode('ascii') + b"\n")
            tn.read_until(b"Password: ")
            tn.write(router.password.encode('ascii') + b"\n")
            tn.write(b"conf t\n")
            time.sleep(1)
            tn.write(b"service timestamps debug datetime local\n")
            time.sleep(1)
            tn.write(b"service timestamps log datetime local\n")
            time.sleep(1)
            tn.write(b"service password-encryption\n")
            time.sleep(1)
            tn.write(b"no ip http server\n")
            time.sleep(1)
            tn.write(b"no ip http secure-server\n")
            time.sleep(1)
            tn.write(b"clock timezone CET 1 0\n")
            time.sleep(1)
            tn.write(b"clock summer-time CEST recurring last Sun Mar 2:00 last Sun Oct 3:00\n")
            time.sleep(1)
            tn.write(b"exit\n")
            time.sleep(1)
            tn.write(b"wr\n")
            time.sleep(1)
            output = tn.read_very_eager().decode('ascii')
            print(f"Output for {router.ip}: {output}")
        except Exception as e:
            print(f"Failed to connect to {router.ip}: {e}")


if __name__ == "__main__":
    with open("/home/user/routers.json") as f:
        jsondata = json.load(f)
        routers = [Router(router["ip"], router["username"], router["password"]) for router in jsondata]
    main_loop(routers)
