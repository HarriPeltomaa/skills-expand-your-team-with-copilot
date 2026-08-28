import unittest
from unittest.mock import patch

from src.backend.routers import activities


class ActivityDifficultyFilterTests(unittest.TestCase):
    @patch("src.backend.routers.activities.activities_collection")
    def test_specific_difficulty_includes_universal_activities(self, mock_collection):
        mock_collection.find.return_value = [
            {
                "_id": "Math Club",
                "description": "Solve challenging problems",
                "difficulty": "Intermediate",
                "participants": [],
                "max_participants": 10,
            },
            {
                "_id": "Chess Club",
                "description": "Learn strategies",
                "participants": [],
                "max_participants": 12,
            },
        ]

        result = activities.get_activities(difficulty="Intermediate")

        mock_collection.find.assert_called_once_with(
            {
                "$or": [
                    {"difficulty": "Intermediate"},
                    {"difficulty": {"$exists": False}},
                    {"difficulty": None},
                ]
            }
        )
        self.assertEqual(set(result.keys()), {"Math Club", "Chess Club"})

    @patch("src.backend.routers.activities.activities_collection")
    def test_all_levels_only_requests_activities_without_difficulty(self, mock_collection):
        mock_collection.find.return_value = [
            {
                "_id": "Chess Club",
                "description": "Learn strategies",
                "participants": [],
                "max_participants": 12,
            }
        ]

        activities.get_activities(difficulty="all")

        mock_collection.find.assert_called_once_with(
            {
                "$or": [
                    {"difficulty": {"$exists": False}},
                    {"difficulty": None},
                ]
            }
        )


if __name__ == "__main__":
    unittest.main()
