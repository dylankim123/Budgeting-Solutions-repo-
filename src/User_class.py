import os, random
from typing import Optional

US_STATES = {s.strip() for s in (
    "Alabama, Alaska, Arizona, Arkansas, California, Colorado, Connecticut, Delaware, Florida, Georgia, "
    "Hawaii, Idaho, Illinois, Indiana, Iowa, Kansas, Kentucky, Louisiana, Maine, Maryland, "
    "Massachusetts, Michigan, Minnesota, Mississippi, Missouri, Montana, Nebraska, Nevada, "
    "New Hampshire, New Jersey, New Mexico, New York, North Carolina, North Dakota, Ohio, Oklahoma, "
    "Oregon, Pennsylvania, Rhode Island, South Carolina, South Dakota, Tennessee, Texas, Utah, "
    "Vermont, Virginia, Washington, West Virginia, Wisconsin, Wyoming"
).split(",")}

class User:
    """This class represents a user and makes a unique username."""
#Cleans and validates username, checks if username exists, and creates/validates user name
    def __init__(self, username: str, state: Optional[str] = None,
                 user_id: Optional[str] = None, storage_path: str = "users.txt") -> None:
        self._storage_path = storage_path
        u = self._clean_username(username)
        if self.is_username_taken(u, storage_path): raise ValueError("Username already exists")
        self._username = u
        self._state = self._clean_state(state)
        if user_id is None:
            self._user_id = self._generate_user_id(storage_path)
        else:
            if not (isinstance(user_id, str) and len(user_id) == 6 and user_id.isdigit()): raise ValueError("Invalid user_id")
            if self._is_user_id_taken(user_id, storage_path): raise ValueError("Invalid user_id")
            self._user_id = user_id

    @property
    def username(self) -> str: return self._username
    @username.setter
    def username(self, new_username: str) -> None:
        u = self._clean_username(new_username)
        if u.lower() != self._username.lower() and self.is_username_taken(u, self._storage_path): raise ValueError("Username already exists")
        self._username = u

    @property
    def state(self) -> Optional[str]: return self._state
    @state.setter
    def state(self, new_state: Optional[str]) -> None: self._state = self._clean_state(new_state)

    @property
    def user_id(self) -> str: return self._user_id
    @property
    def storage_path(self) -> str: return self._storage_path

    def save(self) -> None:
        """Append 'username,state,user_id' to storage; creates file/dir if missing."""
        if self.is_username_taken(self._username, self._storage_path): raise ValueError("Username already exists")
        d = os.path.dirname(self._storage_path)
        if d and not os.path.exists(d): os.makedirs(d, exist_ok=True)
        with open(self._storage_path, "a", encoding="utf-8") as f:
            f.write(f"{self._username},{self._state or ''},{self._user_id}\n")

    @staticmethod
    def is_username_taken(username: str, storage_path: str = "users.txt") -> bool:
        u = username.strip().lower()
        if not u: return False
        try:
            with open(storage_path, "r", encoding="utf-8") as f:
                for line in f:
                    if (line.rstrip("\n").split(",")[0].strip().lower() == u): return True
        except FileNotFoundError:
            return False
        return False

    @classmethod
    def _generate_user_id(cls, storage_path: str) -> str:
        for _ in range(1000):
            cand = f"{random.randint(0, 999_999):06d}"
            if not cls._is_user_id_taken(cand, storage_path): return cand
        raise RuntimeError("Unable to generate a unique user_id")

    @staticmethod
    def _is_user_id_taken(user_id: str, storage_path: str) -> bool:
        try:
            with open(storage_path, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.rstrip("\n").split(",")
                    if len(parts) >= 3 and parts[2].strip() == user_id: return True
        except FileNotFoundError:
            return False
        return False

    @staticmethod
    def _clean_username(username: str) -> str:
        if not isinstance(username, str): raise ValueError("Invalid username")
        u = username.strip()
        if not u: raise ValueError("Invalid username")
        return u

    @staticmethod
    def _clean_state(state: Optional[str]) -> Optional[str]:
        if state is None: return None
        if not isinstance(state, str): raise ValueError("Invalid state")
        s = state.strip().title()
        if s not in US_STATES: raise ValueError("Invalid state")
        return s

    def __str__(self) -> str: return f"User({self._username}, {self._state or 'None'}, id={self._user_id})"
    def __repr__(self) -> str: return f"User(username={self._username!r}, state={self._state!r}, user_id={self._user_id!r}, storage_path={self._storage_path!r})"
