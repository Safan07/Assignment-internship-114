# ========================= Q6: Automated License Plate Testing =========================
import random
import string
import pytest
from difflib import SequenceMatcher

# ------------------ Core function ------------------
def string_similarity_alignment(str1, str2):
    matcher = SequenceMatcher(None, str1, str2)
    similarity_percentage = matcher.ratio() * 100
    return similarity_percentage

# ------------------ License Plate Generators ------------------
def random_valid_plate():
    state = ''.join(random.choices(string.ascii_uppercase, k=2))
    district = ''.join(random.choices(string.digits, k=2))
    series = ''.join(random.choices(string.ascii_uppercase, k=2))
    number = str(random.randint(1, 9999))
    return f"{state}{district}{series}{number}"

def random_invalid_plate(valid_plate, failure_chance=0.05):
    """Generate invalid plate; sometimes accidental match to simulate failure."""
    if random.random() < failure_chance:
        return valid_plate
    plate = list(valid_plate)
    while True:
        idx = random.randint(0, len(plate)-1)
        new_char = random.choice(string.ascii_uppercase + string.digits)
        if plate[idx] != new_char:
            plate[idx] = new_char
            break
    return ''.join(plate)

# ------------------ Generate Test Plates ------------------
NUM_TESTS = 1000
valid_plates = [random_valid_plate() for _ in range(NUM_TESTS // 2)]
invalid_plates = [random_invalid_plate(p, failure_chance=0.05) for p in valid_plates]

# ------------------ Pytest Tests ------------------
@pytest.mark.parametrize("plate", valid_plates)
def test_valid_plate(plate):
    similarity = string_similarity_alignment(plate, plate)
    assert similarity == 100

@pytest.mark.parametrize("valid,invalid", zip(valid_plates, invalid_plates))
def test_invalid_plate(valid, invalid):
    similarity = string_similarity_alignment(valid, invalid)
    # Invalid plate should ideally be less than 100
    assert similarity < 100

# ------------------ Run pytest with verbose output and custom summary ------------------
if __name__ == "__main__":
    print("Running Automated License Plate Tests...\n")
    # Run pytest in verbose mode
    exit_code = pytest.main([__file__, "-v", "--disable-warnings"])

    # Custom summary
    print("\n=== CUSTOM SUMMARY ===")
    print(f"Total tests executed: {NUM_TESTS}")
    if exit_code == 0:
        print("All tests passed ✅")
    else:
        print("Some tests failed ❌ (see verbose output above)")
    print("=====================")
