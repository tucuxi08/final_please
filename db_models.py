from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# 사용자 정보
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    preferred_genre = db.Column(db.String(50))
    password = db.Column(db.String(255), nullable=False)

    playlists = db.relationship('Playlist', back_populates='user', cascade='all, delete')


# 곡 정보
class Track(db.Model):
    __tablename__ = 'tracks'
    track_id = db.Column(db.String(50), primary_key=True)
    track_name = db.Column(db.String(255), nullable=False)
    artist_name = db.Column(db.String(255))
    spotify_url = db.Column(db.Text)
    preview_url = db.Column(db.Text)

    audio_features = db.relationship('AudioFeature', back_populates='track', uselist=False, cascade='all, delete')


# 오디오 특성
class AudioFeature(db.Model):
    __tablename__ = 'audio_features'
    track_id = db.Column(db.String(50), db.ForeignKey('tracks.track_id', ondelete='CASCADE'), primary_key=True)
    danceability = db.Column(db.Float)
    energy = db.Column(db.Float)
    valence = db.Column(db.Float)
    tempo = db.Column(db.Float)
    acousticness = db.Column(db.Float)
    instrumentalness = db.Column(db.Float)
    speechiness = db.Column(db.Float)
    liveness = db.Column(db.Float)
    source_version = db.Column(db.String(20))
    fetched_at = db.Column(db.DateTime, default=datetime.utcnow)

    track = db.relationship('Track', back_populates='audio_features')


# 플레이리스트
class Playlist(db.Model):
    __tablename__ = 'playlist'
    playlist_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'))
    playlist_name = db.Column(db.String(255), nullable=False)

    user = db.relationship('User', back_populates='playlists')
    tracks = db.relationship('PlaylistTrack', back_populates='playlist', cascade='all, delete')


# 플레이리스트-트랙 관계
class PlaylistTrack(db.Model):
    __tablename__ = 'playlist_tracks'
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.playlist_id', ondelete='CASCADE'), primary_key=True)
    track_id = db.Column(db.String(50), db.ForeignKey('tracks.track_id', ondelete='CASCADE'), primary_key=True)

    playlist = db.relationship('Playlist', back_populates='tracks')
    track = db.relationship('Track')


# 공동 등장 통계
class TrackPairStat(db.Model):
    __tablename__ = 'track_pair_stats'
    track_a = db.Column(db.String(50), db.ForeignKey('tracks.track_id', ondelete='CASCADE'), primary_key=True)
    track_b = db.Column(db.String(50), db.ForeignKey('tracks.track_id', ondelete='CASCADE'), primary_key=True)
    co_count = db.Column(db.Integer)
    a_count = db.Column(db.Integer)
    b_count = db.Column(db.Integer)
    score_pmi = db.Column(db.Float)
    score_jaccard = db.Column(db.Float)
    score_lift = db.Column(db.Float)
    last_computed_at = db.Column(db.DateTime, default=datetime.utcnow)
    