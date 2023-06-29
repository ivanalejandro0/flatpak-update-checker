#!/usr/bin/env python3
import subprocess
import sys

MIN_PYTHON = (3, 5)
# I'm using `subprocess.run`, which requires Python >= 3.5
# on Python < 3.5 `subprocess.check_output` can be used instead
if sys.version_info < MIN_PYTHON:
    sys.exit("Error: Python %s.%s or later is required." % MIN_PYTHON)

try:
    # list available updates
    result = subprocess.run(['flatpak', 'remote-ls', '--updates'],
                            stdout=subprocess.PIPE)
    flatpak_updates = result.stdout.decode('utf-8')

    # list installed apps
    result = subprocess.run(['flatpak', 'list'], stdout=subprocess.PIPE)
    flatpak_app_list = result.stdout.decode('utf-8')
except FileNotFoundError:
    sys.exit("Error: there was a problem running the `flatpak` binary, maybe it's not installed.")


# parse the list of apps that can be updated
updates: dict[str, str] = {}
for line in flatpak_updates.splitlines():
    line = line.strip()
    fields = line.split('\t')
    # name = fields[0]
    app_id = fields[1]
    version: str = fields[2]
    updates[app_id] = version

# parse the list of installed apps
app_list: dict[str, str] = {}
for line in flatpak_app_list.splitlines():
    line = line.strip()
    fields = line.split('\t')
    # name = fields[0]
    app_id = fields[1]
    version: str = fields[2]
    app_list[app_id] = version

to_update = []
for app in updates.keys():
    update_type = "update"
    if not app_list[app] or not updates[app]:
        # some apps appear listed with no version,
        # I don't know what that means
        update_type = "unknown"
    elif app_list[app] == updates[app]:
        # flatpak says that there's an update available but the version is
        # the same as the locally installed one. This means that there was a
        # change on the flatpak itself and the app was rebuilt, there's not a
        # new version/release of the app.
        update_type = "rebuild"

    to_update.append({
        'app_id': app,
        'installed': app_list[app],
        'upstream': updates[app],
        'update_type': update_type,
    })

if len(to_update) == 0:
    print("Everything is up to date")
    sys.exit(0)

for app in to_update:
    versions = ""
    if app['update_type'] != "unknown":
        versions = f"{app['installed']} -> {app['upstream']} "
    print(f"{app['app_id']}: {versions}[{app['update_type']}]")

