
Comandi utili:
    $ cat response.json | jq -r '.image' | base64 -D -o  img.jpg
    $ kc cp openwhisk/$(kc-srv redis openwhisk):/data/img.jpg /Volumes/Ramdisk/img.jpg