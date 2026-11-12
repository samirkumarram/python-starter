import json
from pathlib import Path

def evaluate_cv(cv_path: Path, json_path: Path) -> list[str]:
    original_text = cv_path.read_text(encoding = "utf-8").lower()
    extracted_data = json.loads(json_path.read_text(encoding = "utf-8"))
    mismatches = []
    fields_to_check = ["full_name", "email", "phone", "location", "summary"]
    for field in fields_to_check:
        value = extracted_data.get(field)
        if value and value.lower() not in original_text:
            mismatches.append(field)
    for skill in extracted_data.get("skills", []):
        if skill.lower() not in original_text:
            mismatches.append(f"skill: {skill}")
    return mismatches

def main():
    input_dir = Path("day5_samples/cvs")
    output_dir = Path("results")
    total = 0
    passed = 0
    failed = 0
    for cv_path in sorted(input_dir.glob("*.txt")):
        json_path = output_dir / f"{cv_path.stem}.json"

        if not json_path.exists():
            print(f"Missing output: {json_path.name}")
            failed += 1
            total += 1
            continue
        total += 1
        try:
            mismatches = evaluate_cv(cv_path, json_path)
            if mismatches:
                failed += 1
                print(f"REVIEW: {cv_path.name} - {mismatches}")
            else:
                passed += 1
                print(f"PASS: {cv_path.name}")
        except (ValueError, OSError, AttributeError) as error:
            failed += 1
            print(f"ERROR: {cv_path.name} - {error}")
    print("\nEvaluation completed!")
    print(f"Total CVs: {total}")
    print(f"Passed: {passed}")
    print(f"Need review: {failed}")

if __name__ == "__main__":
    main()