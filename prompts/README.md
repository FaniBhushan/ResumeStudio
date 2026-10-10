# Customizing Resume Studio prompts

The app's editable AI prompt templates live in this folder. Each `.txt` file is read when its action runs, so save a prompt edit and use the action again to pick it up; restarting Streamlit is not needed.

Keep the `$name` placeholders intact. They are filled with the current user input immediately before the selected local AI CLI receives the request. Text inside those placeholders is treated as untrusted reference data by the prompt instructions.

| File | Used for | Placeholders |
| --- | --- | --- |
| `refine_text.txt` | Summary, role, and achievement wording suggestions | `$targeting`, `$context`, `$text` |
| `refine_targeting.txt` | Optional job-description context for text suggestions | `$job_description` |
| `cv_import.txt` | Mapping an uploaded selectable-text CV into editable fields | `$cv_text` |
| `categorize_achievements.txt` | Sorting achievement lines into three impact groups | `$achievements` |
| `ats_review.txt` | Comparing CV content with a job description | `$cv_json`, `$job_description` |
| `cover_letter.txt` | Drafting a letter from CV content or user notes | `$cv_content`, `$user_description`, `$job_description` |
| `structured_output_suffix.txt` | JSON response instruction for providers without native schema output | `$schema_text` |

The JSON response schemas remain in `src/cv_builder/processes.py`; they define the shape the app validates. Editing prompt wording does not change those required fields. Review suggested text and extracted fields before saving or applying them.
