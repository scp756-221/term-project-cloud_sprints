"""
Test the *_original_artist routines.

These tests are invoked by running `pytest` with the
appropriate options and environment variables, as
defined in `conftest.py`.
"""

# Standard libraries

# Installed packages
import pytest

# Local modules
import music
import playlist


@pytest.fixture
def mserv(request, music_url, auth):
    return music.Music(music_url, auth)


@pytest.fixture
def plserv(request, playlist_url, auth):
    return playlist.PlayList(playlist_url, auth)


@pytest.fixture
def song1(request):
    return ('Taylor Swift', 'The Last Great American Dynasty')


@pytest.fixture
def song2(request):
    return ('Backxwash', 'Bad Juju')


@pytest.fixture
def playlist1(request):
    return ('TESTlist')


def test_create_delete_playlist(plserv, mserv, song1, song2, playlist1):
    trc, m_id1 = mserv.create(song1[0], song1[1])
    trc, m_id2 = mserv.create(song2[0], song2[1])
    trc, p_id = plserv.create(playlist1, [m_id1, m_id2])
    assert trc == 200
    trc, plname, plist = plserv.read(p_id)
    assert trc == 200 and plname == playlist1 and plist == [m_id1, m_id2]
    plserv.delete(p_id)
    mserv.delete(m_id1)
    mserv.delete(m_id2)


def test_update_playlist(plserv, mserv, song1, song2, playlist1):
    trc, m_id1 = mserv.create(song1[0], song1[1])
    trc, m_id2 = mserv.create(song2[0], song2[1])
    trc, p_id = plserv.create(playlist1, [m_id1])
    trc = plserv.write_song(p_id, m_id2)
    assert trc == 200
    trc, plname, plist = plserv.read(p_id)
    assert trc == 200 and plname == playlist1 and plist == [m_id1, m_id2]
    trc = plserv.delete_song(p_id, m_id2)
    assert trc == 200
    trc, plname, plist = plserv.read(p_id)
    assert trc == 200 and plname == playlist1 and plist == [m_id1]
    plserv.delete(p_id)
    mserv.delete(m_id1)
    mserv.delete(m_id2)
