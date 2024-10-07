import os
import requests 
import hashlib

def main():
    version = input('version: ')
    path = os.path.expanduser('~/.minecraft/mods/')
    backup_path = os.path.expanduser('~/.minecraft/mods.bak/')

    if not os.path.exists(backup_path):
        print(f"creating {backup_path}")
        os.mkdir(backup_path)

    files = os.listdir(path)
    for file in files:
        if file.endswith(".jar"):
            src_path = os.path.join(path, file)
            dst_path = os.path.join(backup_path, file)
            os.rename(src_path, dst_path)

            jar_file = os.path.join(backup_path, file)
            with open(jar_file, 'rb') as mod:
                data=mod.read()
                hashed_files = hashlib.sha1(data).hexdigest()
                r = requests.post(
                    url = "https://api.modrinth.com/v2/version_files/update",
                    headers = {
                        'User-Agent' : 'just updating mods',
                        'Content-Type' : 'application/json'
                        },
                    json = {
                        "hashes": [ f'{hashed_files}' ],
                        "algorithm": "sha1",
                        "loaders": [ "fabric" ],
                        "game_versions": [ f'{version}'
                        ]
                    }
                )

                response = r.json()
                for key, value in response.items():
                    urls = value["files"][0]["url"]
                    filename = value["files"][0]["filename"]
                    print("[+] downloading: ", urls)
                    r = requests.get(urls)

                    updated_mod = path + filename
                    with open(updated_mod, 'wb') as file:
                        file.write(r.content)


if __name__ == '__main__':
    main()
