import os
import re


# Find the default Firefox profile path.
Profile_Path = ''
if os.name == 'nt':  # Windows
    base_path = os.path.join(os.getenv('APPDATA'), 'Mozilla', 'Firefox', 'Profiles')
elif os.name == 'posix':  # Linux / macOS
    base_path = os.path.expanduser('~/.mozilla/firefox/')
else:
    raise Exception("Unsupported OS")

# Look for the default profile directory
for folder_name in os.listdir(base_path):
    if '.default-release' in folder_name:
        Profile_Path = os.path.join(base_path, folder_name)
        break

if not Profile_Path:
    raise Exception("Default Firefox profile not found.")


Prefs_File = os.path.join(Profile_Path, 'prefs.js')


def setProxyServer(use_proxy, host, port):
    proxy_settings = {
        'network.proxy.type': 1 if use_proxy else 0,
        'network.proxy.http': f'"{host}"' if use_proxy else '""',
        'network.proxy.http_port': port if use_proxy else 0,
        'network.share_proxy_settings': 'true' if use_proxy else 'false',
        'network.proxy.no_proxies_on': '""'
    }

    if not os.path.exists(Prefs_File):
        raise Exception(f"prefs.js file not found at {Prefs_File}")
    
    with open(Prefs_File, 'r') as file:
        lines = file.readlines()

    # Update or add the required proxy settings
    new_lines = []
    for line in lines:
        updated = False
        for key, value in proxy_settings.items():
            if re.match(rf'user_pref\("{re.escape(key)}",', line):
                new_lines.append(f'user_pref("{key}", {value});\n')
                updated = True
                break
        if not updated:
            new_lines.append(line)

    # Add any missing settings
    for key, value in proxy_settings.items():
        if not any(f'user_pref("{key}",' in line for line in new_lines):
            new_lines.append(f'user_pref("{key}", {value});\n')

    # Write the updated prefs.js file
    with open(Prefs_File, 'w') as file:
        file.writelines(new_lines)

    print(f"Updated proxy settings in {Prefs_File}")

def enableProxyServer(host, port):
    setProxyServer(True, host, port)

def disableProxyServer():
    setProxyServer(False, 0, 0)


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8080
    #enableProxyServer(host, port)
    disableProxyServer()