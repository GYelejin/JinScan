from paramiko import *
from log import log_event
import jc

class ScanProfile:
    def __init__(self, login, password, host="localhost", port=22):
        self.login = login
        self.password = password
        self.host = host
        self.port = port

    def __str__(self):
        return f"Login: {self.login}, Password: {self.password}, Port: {self.port}, IP Address: {self.host}"

    def __iter__(self):
        return iter((self.login, self.password, self.host, self.port))

def execute_on_remote_host(profile, commands):
    try:
        with SSHClient() as ssh:
            ssh.set_missing_host_key_policy(AutoAddPolicy())
            ssh.connect(profile.host, port=profile.port, username=profile.login, password=profile.password)
            log_event("info", f"SSH connection to {profile.host} established")
            output = []
            for command in commands:
                _stdin, stdout, _stderr = ssh.exec_command(command)
                log_event("info", f"Command {command} executed on {profile.host}")
                exit_code = stdout.channel.recv_exit_status()
                if exit_code == 0:
                    cmd_output = stdout.read().decode()
                    output.append(cmd_output)
                    log_event("info", cmd_output)
                else:
                    cmd_output = f"{exit_code=} : {_stderr.read().decode()}"
                    output.append(cmd_output)
                    log_event("error", cmd_output)
            log_event("info", f"SSH connection to {profile.host} closed")   
    except Exception as e:
        log_event("error", f"Error executing commands on {profile.host}: {e}")
        return [] 
    return output

def detect_os(profile):
    commands = ["cat /etc/os-release", "uname -a"]
    os_release_raw, uname_raw = execute_on_remote_host(profile, commands) 

    os_release = jc.parse('os_release', os_release_raw)
    uname = jc.parse('uname', uname_raw)
    os_release.update(uname)
    log_event("info", f"OS detected on {profile.host}: {os_release}")
    return os_release

def enumerate_services(profile):
    commands = ["systemctl list-units --type=service --state=running"]
    services_raw = execute_on_remote_host(profile, commands)[0]
    services = jc.parse('systemctl', services_raw)
    log_event("info", f"Services enumerated on {profile.host}: {services}")
    return {"services": services}

def enumerate_programs(profile):
    commands = ["dpkg --list", "rpm -qa", "pacman -Q"]
    programs_raw = execute_on_remote_host(profile, commands)
    programs = []
    for program in programs_raw:
        programs.extend(program.split("\n"))
    log_event("info", f"Programs enumerated on {profile.host}: {programs}")
    return {"programs": programs}

def check_open_ports(profile):
    commands = ["ss -tulwn"]
    open_ports_raw = execute_on_remote_host(profile, commands)[0]
    open_ports = jc.parse('ss', open_ports_raw)
    log_event("info", f"Open ports checked on {profile.host}: {open_ports}")
    return {"open_ports": open_ports}

def check_uptime(profile):
    commands = ["uptime"]
    uptime_raw = execute_on_remote_host(profile, commands)[0]
    uptime = jc.parse('uptime', uptime_raw)
    log_event("info", f"Uptime checked on {profile.host}: {uptime}")
    return {"uptime": uptime}

def full_scan(profile):
    # TODO: Add more scan functions. ex: enumerate_programs(profile)
    results = dict()
    results.update(detect_os(profile))
    results.update(enumerate_services(profile))
    results.update(check_open_ports(profile))
    results.update(check_uptime(profile))
    print(results)
    return results
