"""
Simple command-line interface to music service
"""

# Standard library modules
import argparse
import cmd
import re

# Installed packages
import requests

# The services check only that we pass an authorization,
# not whether it's valid
DEFAULT_AUTH = 'Bearer A'


def parse_args():
    argp = argparse.ArgumentParser(
        'mcli',
        description='Command-line query interface to music service'
        )
    argp.add_argument(
        'music_name',
        help="DNS name or IP address of music server"
        )
    argp.add_argument(
        'playlist_name',
        help="DNS name or IP address of playlist server"
        )
    argp.add_argument(
        'music_port',
        type=int,
        help="Port number of music server"
        )
    argp.add_argument(
        'playlist_port',
        type=int,
        help="Port number of playlist server"
        )
    return argp.parse_args()


def get_music_url(name, port):
    return "http://{}:{}/api/v1/music/".format(name, port)

def get_playlist_url(name, port):
    return "http://{}:{}/api/v1/playlist/".format(name, port)


def parse_quoted_strings(arg):
    """
    Parse a line that includes words and '-, and "-quoted strings.
    This is a simple parser that can be easily thrown off by odd
    arguments, such as entries with mismatched quotes.  It's good
    enough for simple use, parsing "-quoted names with apostrophes.
    """
    mre = re.compile(r'''(\w+)|'([^']*)'|"([^"]*)"''')
    args = mre.findall(arg)
    return [''.join(a) for a in args]


class Mcli(cmd.Cmd):
    def __init__(self, args):
        self.music_name = args.music_name
        self.playlist_name = args.playlist_name
        self.music_port = args.music_port
        self.playlist_port = args.playlist_port
        cmd.Cmd.__init__(self)
        self.prompt = 'mql: '
        self.intro = """
Command-line interface to music service.
Enter 'help' for command list.
'Tab' character autocompletes commands.
"""


    ## music service

    def do_read(self, arg):
        """
        Read a single song or list all songs.

        Parameters
        ----------
        song:  music_id (optional)
            The music_id of the song to read. If not specified,
            all songs are listed.

        Examples
        --------
        read 6ecfafd0-8a35-4af6-a9e2-cbd79b3abeea
            Return "The Last Great American Dynasty".
        read
            Return all songs (if the server supports this).

        Notes
        -----
        Some versions of the server do not support listing
        all songs and will instead return an empty list if
        no parameter is provided.
        """
        url = get_music_url(self.music_name, self.music_port)
        r = requests.get(
            url+arg.strip(),
            headers={'Authorization': DEFAULT_AUTH}
            )
        if r.status_code != 200:
            print("Non-successful status code:", r.status_code)
        items = r.json()
        if 'Count' not in items:
            print("0 items returned")
            return
        print("{} items returned".format(items['Count']))
        for i in items['Items']:
            print("{}  {:20.20s} {}".format(
                i['music_id'],
                i['Artist'],
                i['SongTitle']))


    def do_create(self, arg):
        """
        Add a song to the database.

        Parameters
        ----------
        artist: string
        title: string

        Both parameters can be quoted by either single or double quotes.

        Examples
        --------
        create 'Steely Dan'  "Everyone's Gone to the Movies"
            Quote the apostrophe with double-quotes.

        create Chumbawamba Tubthumping
            No quotes needed for single-word artist or title name.
        """
        url = get_music_url(self.music_name, self.music_port)
        args = parse_quoted_strings(arg)
        payload = {
            'Artist': args[0],
            'SongTitle': args[1]
        }
        r = requests.post(
            url,
            json=payload,
            headers={'Authorization': DEFAULT_AUTH}
        )
        print(r.json())


    def do_delete(self, arg):
        """
        Delete a song.

        Parameters
        ----------
        song: music_id
            The music_id of the song to delete.

        Examples
        --------
        delete 6ecfafd0-8a35-4af6-a9e2-cbd79b3abeea
            Delete "The Last Great American Dynasty".
        """
        url = get_music_url(self.music_name, self.music_port)
        r = requests.delete(
            url+arg.strip(),
            headers={'Authorization': DEFAULT_AUTH}
            )
        if r.status_code != 200:
            print("Non-successful status code:", r.status_code)


    def do_quit(self, arg):
        """
        Quit the program.
        """
        return True

    def do_test(self, arg):
        """
        Run a test stub on the music server.
        """
        url = get_music_url(self.music_name, self.music_port)
        r = requests.get(
            url+'test',
            headers={'Authorization': DEFAULT_AUTH}
            )
        if r.status_code != 200:
            print("Non-successful status code:", r.status_code)

    def do_shutdown(self, arg):
        """
        Tell the music cerver to shut down.
        """
        url = get_music_url(self.music_name, self.music_port)
        r = requests.get(
            url+'shutdown',
            headers={'Authorization': DEFAULT_AUTH}
            )
        if r.status_code != 200:
            print("Non-successful status code:", r.status_code)

    
    ## playlist service

    def do_createPlaylist(self, arg):
        """
        Add a playlist of song titles to the database.

        Parameters
        ----------
        Name: string
        Playlist: string

        Both parameters can be quoted by either single or double quotes.
        """
        url = get_playlist_url(self.playlist_name, self.playlist_port)
        args = parse_quoted_strings(arg)
        payload = {
            'Name': args[0],
            'Playlist': [x for x in args[1:]]
        }
        r = requests.post(
            url,
            json=payload,
            headers={'Authorization': DEFAULT_AUTH}
        )
        print(r.json())
        if r.status_code != 200:
            print("Non-successful status code:", r.status_code)


    def do_readPlaylist(self, arg):
        """
        Read a playlist, return its name and list all songs.

        Parameters
        ----------
        playlist_id:  int
            The playlist_id of the playlist to read. 
        """
        url = get_playlist_url(self.playlist_name, self.playlist_port)
        r = requests.get(
            url+arg.strip(),
            headers={'Authorization': DEFAULT_AUTH}
            )
        if r.status_code != 200:
            print("Non-successful status code:", r.status_code)
        items = r.json()
        if 'Count' not in items:
            print("0 items returned")
            return
        print("{} items returned".format(items['Count']))
        for i in items['Items']:
            print("{}  {:20.20s} {}".format(
                i['playlist_id'],
                i['Name'],
                i['Playlist']))


    def do_deletePlaylist(self, arg):
        """
        Delete a playlist.

        Parameters
        ----------
        playlist_id: int
            The playlist_id of the playlist to delete.

        Examples
        --------
        delete 6ecfafd0-8a35-4af6-a9e2-cbd79b3abeea
            Delete the corresponding playlist.
        """
        url = get_playlist_url(self.playlist_name, self.playlist_port)
        r = requests.delete(
            url+arg.strip(),
            headers={'Authorization': DEFAULT_AUTH}
            )
        if r.status_code != 200:
            print("Non-successful status code:", r.status_code)
            

if __name__ == '__main__':
    args = parse_args()
    Mcli(args).cmdloop()