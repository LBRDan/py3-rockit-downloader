import sys
import os
import json


class RockitTrack:
    def __init__(self,  track_id, album_id, album_title, track_no, referer):
        self.album_id = album_id
        self.album_title = album_title
        self.track_id = track_id
        self.referer = referer
        self.track_no = track_no

    def download(self, requests):
        s = requests.Session()
        s.headers.update({'referer': self.referer})
        response = s.post('https://www.rockit.it/w/ajax/play.php',
                          {'id': self.track_id, '0k': 'okmobile'})
        resp = json.loads(response.content)
        self.album_id = resp['album']
        self.title = resp['title']
        self.artist_name = resp['author']

        aw_url = resp['url']

        if 'tipo' in resp and resp['tipo'] != 'intero':
            print("[ERROR] Track " + self.title +
                  " not exists, is not downloadable.")
            return

        if aw_url is "":
            print("[ERROR] Track " + self.title +
                  " not exists, is not downloadable.")
            return

        filename = "download/" + \
            self.album_title.replace(" ", "_") + "/" + \
            self.title.replace(" ", "_") + ".mp3"
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, 'wb') as file:
            print("Download " + self.title + "...\n")
            s = requests.Session()
            s.headers.update({'referer': self.referer})
            response = s.get(aw_url, stream=True)
            total_length = response.headers.get('content-length')

            if total_length is None:
                file.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    file.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s] %d of 100 percent" % (
                        '=' * done, ' ' * (50 - done), done * 2))
                    sys.stdout.flush()
                print("\n[SUCCESS] Track " + self.title +
                      " downloaded successfully.")
