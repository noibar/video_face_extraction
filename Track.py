import pickle
import numpy as np


class Tracks:
    def __init__(self, feature_size=2048):
        self.tracks = {}
        self.frames = {}
        self.labels = {}
        self.img = {}
        self.features_shape = (feature_size)

    def add_track_features(self, track_id, time, features, label, path):
        if track_id not in self.tracks:
            self.tracks[track_id] = {}
        self.tracks[track_id][time] = features
        if time not in self.frames:
            self.frames[time] = {}
        self.frames[time][track_id] = features
        self.labels[track_id] = label
        self.img[(track_id,time)] = path

    def create_track_representation(self, track_id, features_func, should_norm):
        track_frames_features = [f.reshape(self.features_shape) for f in self.tracks[track_id].values()]
        if features_func is not None:
            track_frames_features = features_func(track_frames_features)
        track_representation = np.average(track_frames_features, axis=0)

        if should_norm:
            norm = np.linalg.norm(track_representation)
            track_representation = track_representation / norm
        return track_representation

    def get_tracks_representations(self, should_norm=True, features_func=None):
        track_representations = {}
        for track_id in self.tracks:
            track_representations[track_id] = self.create_track_representation(track_id, features_func, should_norm)
        return track_representations

    def get_tracks_labels(self):
        return self.labels

    def save(self, path):
        print('saving tracks to:', path)
        with open(path, 'wb') as f:
            pickle.dump(self, f)

    def load(self, path):
        print('loading tracks from:', path)
        with open(path, 'rb') as f:
            tracks = pickle.load(f)
            self.tracks = tracks.tracks
            self.frames = tracks.frames
            self.labels = tracks.labels
            self.img = tracks.img
