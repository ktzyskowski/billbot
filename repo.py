import json


class Repository:
    """Data repository that is persisted through .txt files"""

    def __init__(self, dbpath='db.json'):
        """Initialize the repository."""
        self._dbpath = dbpath
        self._load()

    def _load(self):
        try:
            with open(self._dbpath, 'r') as fp:
                self._data = json.load(fp)
        except FileNotFoundError:
            self._data = {}

    def _save(self):
        with open(self._dbpath, 'w') as fp:
            json.dump(self._data, fp)

    def put(self, k, v):
        self._data[k] = v
        self._save()  # persist the data

    def get(self, k):
        return self._data[k]

    def contains(self, k):
        return k in self._data
