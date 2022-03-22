"""
Python  API for the music service.
"""

# Standard library modules

# Installed packages
import requests


class PlayList():
    """Python API for the music service.

    Handles the details of formatting HTTP requests and decoding
    the results.

    Parameters
    ----------
    url: string
        The URL for accessing the music service. Often
        'http://cmpt756s2:30001/'. Note the trailing slash.
    auth: string
        Authorization code to pass to the music service. For many
        implementations, the code is required but its content is
        ignored.
    """
    def __init__(self, url, auth):
        self._url = url
        self._auth = auth

    def create(self, playlist_name, song_list=[]):
        """Create an playlist name, song pair.

        Parameters
        ----------
        playlist_name : string
            The name of the playlist.
        song_list: string
            default is an empty list.

        Returns
        -------
        (number, string)
            The number is the HTTP status code returned by Music.
            The string is the UUID of this song in the music database.
        """
        payload = {'Name': playlist_name, 'Playlist': song_list}
        if type(song_list) == list:
            payload['Playlist'] = ",".join(song_list)
        r = requests.post(
            self._url,
            json=payload,
            headers={'Authorization': self._auth}
        )
        return r.status_code, r.json()['playlist_id']

    def write_song(self, playlist_id, m_id):
        '''write a song to the playlist.

        Parameters
        ----------
        playlist_id: string
            The UUID of this playist in the music database.
        song_id: string
            The UUID of this song in the music database.

        Returns
        -------
        number
            The HTTP status code returned by the music service.
        '''
        r = requests.post(
            f"{self._url}{playlist_id}/add",
            json={'music_id': m_id},
            headers={'Authorization': self._auth}
        )
        return r.status_code

    def delete_song(self, playlist_id, m_id):
        '''delete a song in the playlist.

        Parameters
        ----------
        playlist_id: string
            The UUID of this playist in the music database.
        song_id: string
            The UUID of this song in the music database.

        Returns
        -------
        number
            The HTTP status code returned by the music service.
        '''
        requests.post(
            f"{self._url}{playlist_id}/delete",
            json={'music_id': m_id},
            headers={'Authorization': self._auth}
        )

    def read(self, playlist_id):
        """Read a playlist.

        Parameters
        ----------
        playlist_id: string
            The UUID of this playist in the music database.

        Returns
        -------
        status, playlist_name, songs in that playlist
        """
        r = requests.get(
            self._url + playlist_id,
            headers={'Authorization': self._auth}
            )
        if r.status_code != 200:
            return r.status_code, None, None

        item = r.json()['Items'][0]
        return r.status_code, item['Name'], item['Playlist']

    def delete(self, playlist_id):
        """Delete a playlist.

        Parameters
        ----------
        playlist_id: string
            The UUID of this playlist in the music database.

        Returns
        -------
        Does not return anything. The music delete operation
        always returns 200, HTTP success.
        """
        requests.delete(
            self._url + playlist_id,
            headers={'Authorization': self._auth}
        )
