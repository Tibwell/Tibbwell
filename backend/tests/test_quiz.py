"""
Unit tests for the TibbWell Quiz module
Tests scoring logic, temperament determination, and combination naming
"""
import sys
import os
import pytest

# Add parent directory to path so we can import from api
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from api.quiz import (
    TEMPERAMENTS,
    COMBINATION_NAMES,
    calculate_temperament_scores,
    determine_dominant_temperaments,
    get_combination_name,
    QuizAnswer,
    TEMPERAMENT_INFO,
)


class TestCalculateTemperamentScores:
    """Tests for the calculate_temperament_scores function"""

    def test_all_sanguinous(self):
        """All answers mapped to Sanguinous should give Sanguinous=25"""
        answers = [
            QuizAnswer(question_id=i, selected_temperament="Sanguinous")
            for i in range(1, 26)
        ]
        scores = calculate_temperament_scores(answers)
        assert scores["Sanguinous"] == 25
        assert scores["Bilious"] == 0
        assert scores["Phlegmatic"] == 0
        assert scores["Melancholic"] == 0

    def test_all_bilious(self):
        """All answers mapped to Bilious"""
        answers = [
            QuizAnswer(question_id=i, selected_temperament="Bilious")
            for i in range(1, 26)
        ]
        scores = calculate_temperament_scores(answers)
        assert scores["Bilious"] == 25
        assert scores["Sanguinous"] == 0

    def test_all_phlegmatic(self):
        """All answers mapped to Phlegmatic"""
        answers = [
            QuizAnswer(question_id=i, selected_temperament="Phlegmatic")
            for i in range(1, 26)
        ]
        scores = calculate_temperament_scores(answers)
        assert scores["Phlegmatic"] == 25
        assert scores["Sanguinous"] == 0

    def test_all_melancholic(self):
        """All answers mapped to Melancholic"""
        answers = [
            QuizAnswer(question_id=i, selected_temperament="Melancholic")
            for i in range(1, 26)
        ]
        scores = calculate_temperament_scores(answers)
        assert scores["Melancholic"] == 25
        assert scores["Bilious"] == 0

    def test_mixed_answers(self):
        """Mixed answers should produce proportional scores"""
        answers = [
            QuizAnswer(question_id=1, selected_temperament="Sanguinous"),
            QuizAnswer(question_id=2, selected_temperament="Sanguinous"),
            QuizAnswer(question_id=3, selected_temperament="Bilious"),
            QuizAnswer(question_id=4, selected_temperament="Bilious"),
            QuizAnswer(question_id=5, selected_temperament="Phlegmatic"),
            QuizAnswer(question_id=6, selected_temperament="Melancholic"),
        ]
        scores = calculate_temperament_scores(answers)
        assert scores["Sanguinous"] == 2
        assert scores["Bilious"] == 2
        assert scores["Phlegmatic"] == 1
        assert scores["Melancholic"] == 1

    def test_empty_answers(self):
        """Empty answers should produce zero scores"""
        scores = calculate_temperament_scores([])
        assert scores["Sanguinous"] == 0
        assert scores["Bilious"] == 0
        assert scores["Phlegmatic"] == 0
        assert scores["Melancholic"] == 0
        assert sum(scores.values()) == 0

    def test_invalid_temperament_ignored(self):
        """Invalid temperament strings should be ignored"""
        answers = [
            QuizAnswer(question_id=1, selected_temperament="Sanguinous"),
            QuizAnswer(question_id=2, selected_temperament="Invalid"),
            QuizAnswer(question_id=3, selected_temperament="Unknown"),
        ]
        scores = calculate_temperament_scores(answers)
        assert scores["Sanguinous"] == 1
        assert scores["Bilious"] == 0
        assert scores["Phlegmatic"] == 0
        assert scores["Melancholic"] == 0

    def test_case_sensitivity(self):
        """Temperament names should be case-sensitive (capitalized)"""
        answers = [
            QuizAnswer(question_id=1, selected_temperament="sanguinous"),  # lowercase
            QuizAnswer(question_id=2, selected_temperament="Sanguinous"),
        ]
        scores = calculate_temperament_scores(answers)
        assert scores["Sanguinous"] == 1  # only the capitalized one counts


class TestDetermineDominantTemperaments:
    """Tests for the determine_dominant_temperaments function"""

    def test_normal_case(self):
        """Highest score should be dominant, second highest sub-dominant"""
        scores = {"Sanguinous": 10, "Bilious": 8, "Phlegmatic": 5, "Melancholic": 2}
        dominant, sub_dominant = determine_dominant_temperaments(scores)
        assert dominant == "Sanguinous"
        assert sub_dominant == "Bilious"

    def test_tie_break(self):
        """Tie between first and second should be handled"""
        scores = {"Sanguinous": 8, "Bilious": 8, "Phlegmatic": 5, "Melancholic": 4}
        dominant, sub_dominant = determine_dominant_temperaments(scores)
        # With a tie, it should pick consistently
        assert dominant in ["Sanguinous", "Bilious"]
        assert sub_dominant in ["Sanguinous", "Bilious"]
        assert dominant != sub_dominant

    def test_bilious_dominant(self):
        """Bilious as dominant"""
        scores = {"Sanguinous": 3, "Bilious": 12, "Phlegmatic": 5, "Melancholic": 5}
        dominant, sub_dominant = determine_dominant_temperaments(scores)
        assert dominant == "Bilious"
        assert sub_dominant in ["Phlegmatic", "Melancholic"]

    def test_phlegmatic_dominant(self):
        """Phlegmatic as dominant"""
        scores = {"Sanguinous": 4, "Bilious": 3, "Phlegmatic": 10, "Melancholic": 8}
        dominant, sub_dominant = determine_dominant_temperaments(scores)
        assert dominant == "Phlegmatic"
        assert sub_dominant == "Melancholic"

    def test_melancholic_dominant(self):
        """Melancholic as dominant"""
        scores = {"Sanguinous": 2, "Bilious": 5, "Phlegmatic": 6, "Melancholic": 12}
        dominant, sub_dominant = determine_dominant_temperaments(scores)
        assert dominant == "Melancholic"
        assert sub_dominant == "Phlegmatic"

    def test_all_equal(self):
        """All four temperaments equal should still pick top two"""
        scores = {"Sanguinous": 6, "Bilious": 6, "Phlegmatic": 6, "Melancholic": 6}
        dominant, sub_dominant = determine_dominant_temperaments(scores)
        assert dominant in TEMPERAMENTS
        assert sub_dominant in TEMPERAMENTS
        assert dominant != sub_dominant

    def test_first_two_equal_others_lower(self):
        """Tie between first two, others much lower"""
        scores = {"Sanguinous": 10, "Bilious": 10, "Phlegmatic": 2, "Melancholic": 3}
        dominant, sub_dominant = determine_dominant_temperaments(scores)
        assert dominant in ["Sanguinous", "Bilious"]
        assert sub_dominant in ["Sanguinous", "Bilious"]
        assert dominant != sub_dominant
        assert "Phlegmatic" not in [dominant, sub_dominant]
        assert "Melancholic" not in [dominant, sub_dominant]


class TestGetCombinationName:
    """Tests for the get_combination_name function"""

    def test_valid_combination(self):
        """Known combination should return correct name"""
        name = get_combination_name("Sanguinous", "Bilious")
        assert name == "Sanguinous-Bilious"

    def test_reverse_order(self):
        """Reverse dominant/sub-dominant should still map"""
        name = get_combination_name("Bilious", "Sanguinous")
        assert name == "Sanguinous-Bilious"  # Both map to same canonical name

    def test_another_valid(self):
        """Known combination: Bilious-Melancholic"""
        name = get_combination_name("Bilious", "Melancholic")
        assert name == "Bilious-Melancholic"

    def test_another_reverse(self):
        """Reverse: Melancholic-Bilious"""
        name = get_combination_name("Melancholic", "Bilious")
        assert name == "Bilious-Melancholic"

    def test_nonexistent_combination(self):
        """Unknown combination falls back to {dominant}-{sub_dominant}"""
        name = get_combination_name("Sanguinous", "Unknown")
        assert name == "Sanguinous-Unknown"

    def test_all_valid_combinations_exist(self):
        """All 12 possible temperament combinations should exist in COMBINATION_NAMES"""
        combos = [
            ("Sanguinous", "Bilious"),
            ("Sanguinous", "Phlegmatic"),
            ("Sanguinous", "Melancholic"),
            ("Bilious", "Sanguinous"),
            ("Bilious", "Phlegmatic"),
            ("Bilious", "Melancholic"),
            ("Phlegmatic", "Sanguinous"),
            ("Phlegmatic", "Bilious"),
            ("Phlegmatic", "Melancholic"),
            ("Melancholic", "Sanguinous"),
            ("Melancholic", "Bilious"),
            ("Melancholic", "Phlegmatic"),
        ]
        for dominant, sub_dominant in combos:
            name = get_combination_name(dominant, sub_dominant)
            assert name is not None
            assert isinstance(name, str)
            assert "-" in name

    def test_each_temperament_as_dominant(self):
        """Each temperament should appear as dominant in some combination"""
        for t in TEMPERAMENTS:
            others = [x for x in TEMPERAMENTS if x != t]
            for other in others:
                name = get_combination_name(t, other)
                assert name is not None


class TestTemperamentInfo:
    """Tests for TEMPERAMENT_INFO data"""

    def test_all_temperaments_present(self):
        """All four temperaments should have info"""
        for t in TEMPERAMENTS:
            assert t in TEMPERAMENT_INFO
            assert "name" in TEMPERAMENT_INFO[t]
            assert "quality" in TEMPERAMENT_INFO[t]
            assert "element" in TEMPERAMENT_INFO[t]
            assert "description" in TEMPERAMENT_INFO[t]

    def test_sanguinous_quality(self):
        """Sanguinous quality should be Hot & Moist"""
        assert TEMPERAMENT_INFO["Sanguinous"]["quality"] == "Hot & Moist"
        assert TEMPERAMENT_INFO["Sanguinous"]["element"] == "Air"

    def test_bilious_quality(self):
        """Bilious quality should be Hot & Dry"""
        assert TEMPERAMENT_INFO["Bilious"]["quality"] == "Hot & Dry"
        assert TEMPERAMENT_INFO["Bilious"]["element"] == "Fire"

    def test_phlegmatic_quality(self):
        """Phlegmatic quality should be Cold & Moist"""
        assert TEMPERAMENT_INFO["Phlegmatic"]["quality"] == "Cold & Moist"
        assert TEMPERAMENT_INFO["Phlegmatic"]["element"] == "Water"

    def test_melancholic_quality(self):
        """Melancholic quality should be Cold & Dry"""
        assert TEMPERAMENT_INFO["Melancholic"]["quality"] == "Cold & Dry"
        assert TEMPERAMENT_INFO["Melancholic"]["element"] == "Earth"


class TestCombinationNamesData:
    """Tests for COMBINATION_NAMES data completeness"""

    def test_twelve_combinations(self):
        """There should be exactly 12 combination mappings (2 per pair order)"""
        assert len(COMBINATION_NAMES) == 12

    def test_no_duplicate_keys(self):
        """No duplicate keys in COMBINATION_NAMES"""
        keys = list(COMBINATION_NAMES.keys())
        assert len(keys) == len(set(keys))  # 12 unique keys

    def test_six_unique_combination_values(self):
        """There should be 6 unique combination names (each appears twice due to order mapping)"""
        values = list(COMBINATION_NAMES.values())
        assert len(set(values)) == 6

    def test_each_value_has_hyphen(self):
        """All combination names should have a hyphen between two temperament names"""
        for name in COMBINATION_NAMES.values():
            assert "-" in name
            parts = name.split("-")
            assert len(parts) == 2
            assert parts[0] in TEMPERAMENTS or parts[1] in TEMPERAMENTS

    @pytest.mark.parametrize("dominant,sub_dominant,expected", [
        ("Sanguinous", "Bilious", "Sanguinous-Bilious"),
        ("Sanguinous", "Phlegmatic", "Sanguinous-Phlegmatic"),
        ("Sanguinous", "Melancholic", "Sanguinous-Melancholic"),
        ("Bilious", "Phlegmatic", "Bilious-Phlegmatic"),
        ("Bilious", "Melancholic", "Bilious-Melancholic"),
        ("Phlegmatic", "Melancholic", "Phlegmatic-Melancholic"),
    ])
    def test_specific_combinations(self, dominant, sub_dominant, expected):
        """Parametrized test for specific combinations"""
        name = get_combination_name(dominant, sub_dominant)
        assert name == expected