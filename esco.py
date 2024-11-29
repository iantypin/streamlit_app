import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional

import requests
from esco_skill_extractor import SkillExtractor


class EscoExtractor:
    def __init__(self):
        self.skill_extractor = SkillExtractor()

    def fetch_skill_title(self, uri: str, skill_name: str) -> Optional[str]:
        """
        Fetches the skill title from the ESCO API. Falls back to checking the web interface if the API returns 404.
        """
        try:
            response = self._get_api_response(uri)
            return response.get("title", None)
        except requests.HTTPError as e:
            if e.response.status_code == 404 and self._is_skill_on_web(uri):
                logging.warning(f"Skill available on the web but not in the API: {uri}")
                return skill_name  # Fallback to original skill name if on the web
            else:
                logging.error(f"HTTP error while fetching skill for URI {uri}: {e}")
        return None

    def validate_skills(self, skills: list[str]) -> list[str]:
        """
        Validates a list of skills by matching them with ESCO skill URIs and fetching their titles using threading.
        """
        skill_uris = self.skill_extractor.get_skills(skills)
        validated_skills = {}

        def process_skill(skill, uris):
            """
            Processes a single skill by fetching its title for each URI.
            """
            validated = {}
            if uris:
                for uri in uris:
                    title = self.fetch_skill_title(uri, skill)
                    if title:
                        new_value = {skill: title}
                        validated.update(new_value)
            else:
                logging.info(f"Skill not found in ESCO: {skill}")
            return validated

        # Use ThreadPoolExecutor for parallel processing
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {
                executor.submit(process_skill, skill, uris): skill
                for skill, uris in zip(skills, skill_uris)
            }

            for future in as_completed(futures):
                try:
                    result = future.result()
                    validated_skills.update(result)
                except Exception as e:
                    logging.error(f"Error processing skill {futures[future]}: {e}")

        return validated_skills

    def _get_api_response(self, uri: str) -> dict:
        """
        Sends a request to the ESCO API and returns the JSON response.
        """
        response = requests.get(
            'https://ec.europa.eu/esco/api/resource/skill', params={"uri": uri, "language": "en"}
        )
        response.raise_for_status()
        return response.json()

    def _is_skill_on_web(self, uri: str) -> bool:
        """
        Checks if a skill is available on the ESCO web interface.
        """
        params = {"uri": uri, "language": 'en'}
        response = requests.get("https://esco.ec.europa.eu/en/classification/skill", params=params)
        return response.status_code == 200