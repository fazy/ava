import os
import toml

from copy import deepcopy
from typing import Dict, Any


class ProfileLoader(object):
    def __init__(self, profile_dir: str):
        self.profile_dir = profile_dir

    def read_profile(self, profile: str) -> Dict[str, Any]:
        config = {
            "engine": "text-davinci-003",
            "temperature": 0.3,
            "n": 1,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "max_tokens": 1000,
            "prompt_template": "{{__INPUT__}}"
        }

        if os.path.exists(self.get_profile_path("default")):
            self.merge_config_from_file(config, "default")

        if profile != 'default' and profile is not None:
            self.merge_config_from_file(config, profile)

        return config

    def merge_config_from_file(self, config: Dict, profile: str) -> Dict:
        profile_file_path = self.get_profile_path(profile)
        merged_config = deepcopy(config)

        try:
            with open(profile_file_path) as f:
                merged_config.update(
                    {k: v for k, v in toml.load(f).items() if k in merged_config})
        except FileNotFoundError:
            raise RuntimeError(
                f"Error reading profile {profile}, file {profile_file_path}")
        except toml.TomlDecodeError as e:
            raise RuntimeError(f"Error parsing config: {e}")

        return merged_config

    def get_profile_path(self, profile: str) -> str:
        if profile == 'default':
            return f"{self.profile_dir}/default.toml"
        else:
            return f"{self.profile_dir}/{profile}.toml"
