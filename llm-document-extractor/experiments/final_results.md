# LLM Document Extractor - Experiment Results

## 1. CV Extraction: Hosted vs Local Model

I tested the CV extraction pipeline using 10 synthetic CVs with
both a hosted model and a local model.

| Metric                       | Hosted Model (Groq) | Local Model (Ollama) |
|------------------------------|---------------------|----------------------|
| Model                        | openai/gpt-oss-20b  | qwen3.5:2b           |
| CVs processed                | 10                  | 10                   |
| Successful extractions       | 10                  | 10                   |
| Failed extractions           | 0                   | 0                    |
| Field accuracy               | 100%                | 100%                 |
| Average processing time      | Not fully measured  | 96.18 seconds        |

The Groq batch processed CV02 to CV10 in 9.94 seconds.
CV01 was processed separately, and its time was not recorded.
Therefore, a comparable average time for all 10 CVs is unavailable.

The local model took 961.78 seconds to process all 10 CVs,
with an average of 96.18 seconds per CV.

Both models produced accurate results in my manual evaluation.
The hosted model was much faster in the measured batch.

## 2. Temperature and Fixed-Seed Experiment

I tested the local model using the same CV and prompt.

- At temperature 0, I ran the model three times. All three outputs were identical.
- At temperature 0.8, I also ran it three times. The outputs were very similar, but the experience year fields were returned as strings instead of numbers.
- I then ran the model once with temperature 0.8 and seed 42. The output format was similar to the other high-temperature runs.

The experiment showed that temperature did not create major content differences for this simple CV. However, the output data types changed. The fixed seed did not show a noticeable difference in this single test.

## 3. Context-Size Experiment

I tested a long document containing repeated CV information.

| Setting       | Context size | Processing time | Result                       |
|---------------|--------------|-----------------|------------------------------|
| Default model | 4,096        | 309.15 seconds  | Incomplete candidate summary |
| Custom model  | 8,192        | 381.38 seconds  | Incomplete candidate analysis|

I created a custom Ollama model with a context size of 8,192 using a Modelfile.

Both runs completed within the 10-minute limit, but neither produced the expected structured JSON output.

Increasing the context size did not solve the problem. The model struggled to process the long document and follow the expected output format.

## 4. Multimodal Invoice Extraction

I tested the local Qwen model with two invoice sources:
- A normal invoice image (PNG).
- A scanned invoice page converted from PDF to PNG.

I used the same Pydantic schema and invoice extraction prompts for both tests.

### Invoice Image Result

The model successfully extracted the invoice number, dates, seller and buyer names, seller address, total amount and tax amount.

It returned null for fields that were not available, such as buyer address, currency and payment status.

The extracted JSON passed Pydantic validation.

### Scanned PDF Result

I converted the scanned PDF page into an image and resized it to reduce the image size before sending it to the local model.

The model extracted the main invoice details correctly, including:
- Invoice number: INV-2026-0533
- Invoice date: 2026-03-14
- Due date: 2026-04-13
- Total amount: 26786.00
- Tax amount: 4086.00

However, the model kept explanatory text such as "(invented)" and "(invented address)" in some names and addresses, even after I added instructions to remove those annotations.

The response passed Pydantic validation, but this experiment showed that schema validation does not guarantee factual accuracy or perfect instruction following.

### Multimodal Experiment Conclusion

The local model was able to process both an invoice image and a scanned PDF page. It extracted most of the required information correctly, but it still had some difficulty following text-cleanup instructions.

## 5. What I Learned

During this assignment, I learned how to build a document extraction system using an LLM.

I learned how to connect to both hosted and local models using an OpenAI-compatible client. I also worked with settings, timeouts, retries, fallback models and token usage.

I understood how Pydantic helps validate the JSON returned by a model. I also learned that valid JSON does not always mean the extracted information is correct.

The experiments showed me that hosted models can be much faster than small local models. I also learned that changing temperature, seed and context size can affect model behaviour, but does not guarantee better results.

The multimodal experiment helped me understand how an LLM can extract information from invoice images and scanned documents.

## 6. AI-Assistance Log

| Area | How AI helped | What I checked |
|---|---|---|
| LLM client | Helped explain client configuration, retries and timeouts | Reviewed the code and ran tests |
| Pydantic schema | Helped understand schema design and validation | Checked the generated JSON against the schema |
| Prompt management | Helped organise system and extraction prompts | Checked that document text was kept separate from instructions |
| Ollama errors | Helped investigate context and timeout errors | Changed settings and reran the scripts |
| Invoice extraction | Helped improve extraction instructions | Compared model output with the original invoice |
| Experiments | Helped interpret temperature, seed and context results | Used actual output files and recorded timings |

I used AI mainly to understand errors, discuss possible fixes and improve prompts. I did not accept every model output blindly. I checked the code, ran the scripts and compared extracted information with the original documents.