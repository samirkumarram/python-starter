from pathlib import Path

from llm_document_extractor.config import load_settings
from llm_document_extractor.llm_client import LLMClient

from llm_document_extractor.prompt_manager import PromptManager
from llm_document_extractor.document_reader import DocumentReader
from llm_document_extractor.document_extractor import DocumentExtractor
from llm_document_extractor.workflow import CVExtractionWorkflow

def main():
    settings = load_settings()
    llm_client = LLMClient(settings)
    prompt_manager = PromptManager()
    document_reader = DocumentReader()
    document_extractor = DocumentExtractor(llm_client, prompt_manager)
    workflow = CVExtractionWorkflow(document_reader, document_extractor)

    input_dir = Path("day5_samples/cvs")
    output_dir = Path("results")
    output_dir.mkdir(parents = True, exist_ok = True)
    cv_files = sorted(input_dir.glob("*.txt"))
    if not cv_files:
        print("No CV files found!")
        return

    successful = 0
    failed = 0

    for cv_path in cv_files:
        try:
            result = workflow.run(cv_path)
            output_path = output_dir / f"{cv_path.stem}.json"
            output_path.write_text(result.model_dump_json(indent = 2), encoding = "utf-8")
            successful += 1
            print(f"Successfully processed: {cv_path.name}")
        except Exception as error:
            failed += 1
            print(f"Failed to process {cv_path.name}: {error}")
    print("\nBatch extraction completed")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"\nOutput directory: {output_dir}")
if __name__ == "__main__":
    main()