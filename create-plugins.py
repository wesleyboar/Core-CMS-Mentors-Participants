#!/usr/bin/env python3
"""
Convert ACSC mentor/participant CSV data to Django CMS plugin JSON format
with structured Q&A content and a single row containing all cards.
Uses descriptive image placeholders and consistent output file names.
"""

import csv
import json
import html

# Question mappings for mentors and participants
mentor_questions = {
    "What aspects of the program are you most looking forward to? Why?": "What aspects of the program are you most looking forward to?",
    "What did you want to be as a kid and why?": "What did you want to be as a kid and why?",
    "If you could design your own invention right now, what would it do?": "If you could design your own invention right now, what would it do?",
    "What social or societal challenge do you care most about and why?": "What social or societal challenge do you care most about and why?",
    "What was the best advice you received in college?": "What was the best advice you received in college?",
    "Is there a topic in your field you think everyone should know a little about?": "Is there a topic in your field you think everyone should know a little about?"
}

participant_questions = {
    "What is your current major and why did you choose it?": "Why did you choose your major?",
    "What did you want to be as a kid and why?": "What did you want to be as a kid and why?",
    "Describe your perfect day.": "Describe your perfect day.",
    "What social or societal challenge do you care most about and why?": "What social or societal challenge do you care most about and why?",
    "What was the best advice you received in college?": "What was the best advice you received in college?",
    "Would you rather live without internet or your phone?": "Would you rather live without internet or your phone?"
}

def build_structured_html(entry, questions):
    """Build structured Q&A HTML block."""
    html_parts = []
    for field, heading in questions.items():
        answer = entry.get(field, "").strip()
        if answer:
            html_parts.append(f"<h4>{html.escape(heading)}</h4>")
            html_parts.append(f"<p>{html.escape(answer)}</p>")
    return "\n".join(html_parts)

def generate_plugins(data, questions, is_mentor, start_pk):
    """Generate plugin structure for mentors or participants with a single row."""
    plugins = []
    pk_counter = start_pk

    # Create one row plugin
    row_pk = pk_counter
    pk_counter += 1
    plugins.append({
        "pk": row_pk,
        "creation_date": "2025-11-07T00:00:00.000Z",
        "position": 0,
        "plugin_type": "Bootstrap4GridRowPlugin",
        "parent_id": None,
        "data": {
            "vertical_alignment": "",
            "horizontal_alignment": "",
            "gutters": False,
            "tag_type": "div",
            "attributes": {}
        }
    })

    for position, entry in enumerate(data):
        # Column plugin
        column_pk = pk_counter
        pk_counter += 1
        plugins.append({
            "pk": column_pk,
            "creation_date": "2025-11-07T00:00:00.000Z",
            "position": position,
            "plugin_type": "Bootstrap4GridColumnPlugin",
            "parent_id": row_pk,
            "data": {
                "column_type": "col",
                "column_alignment": "",
                "tag_type": "div",
                "attributes": {},
                "xs_col": 12, "sm_col": 12, "md_col": 12, "lg_col": 6, "xl_col": 6
            }
        })

        # Style plugin
        style_pk = pk_counter
        pk_counter += 1
        plugins.append({
            "pk": style_pk,
            "creation_date": "2025-11-07T00:00:00.000Z",
            "position": 0,
            "plugin_type": "StylePlugin",
            "parent_id": column_pk,
            "data": {
                "template": "default",
                "label": "Card w/ Image",
                "tag_type": "div",
                "class_name": "card--image-left",
                "additional_classes": "card--plain",
                "id_name": "",
                "attributes": {}
            }
        })

        # Header text plugin
        text_pk = pk_counter
        pk_counter += 1
        name = entry.get("First Name", "") + " " + entry.get("Last Name", "")
        institution = entry.get("Current University / Workplace", entry.get("University", "")).strip()
        major = entry.get("Current major and / or work reponsibilities", entry.get("Major", "")).strip()
        header_html = f"<h3>{html.escape(name)}</h3>\n\n<p><strong>Academic Institution:</strong><br>\n{html.escape(institution)}</p>\n\n<p><strong>{'Work Responsibilities' if is_mentor else 'Field of Study'}:</strong><br>\n{html.escape(major)}</p>"
        plugins.append({
            "pk": text_pk,
            "creation_date": "2025-11-07T00:00:00.000Z",
            "position": 0,
            "plugin_type": "TextPlugin",
            "parent_id": style_pk,
            "data": {"body": header_html}
        })

        # Picture plugin with descriptive placeholder
        picture_pk = pk_counter
        pk_counter += 1
        picture_id = 2826
        plugins.append({
            "pk": picture_pk,
            "creation_date": "2025-11-07T00:00:00.000Z",
            "position": 1,
            "plugin_type": "Bootstrap4PicturePlugin",
            "parent_id": style_pk,
            "data": {
                "template": "default",
                "picture": picture_id,
                "picture_fluid": True
            }
        })

        # Body text plugin (structured Q&A)
        body_pk = pk_counter
        pk_counter += 1
        body_html = build_structured_html(entry, questions)
        plugins.append({
            "pk": body_pk,
            "creation_date": "2025-11-07T00:00:00.000Z",
            "position": 1,
            "plugin_type": "TextPlugin",
            "parent_id": column_pk,
            "data": {"body": body_html}
        })

    return plugins

# Load CSVs
with open("2025+ACSC+MENTOR+Participant+Agreement+and+PreSurvey+(SC25)_October+22,+2025_13.20.csv", encoding="utf-8-sig") as f:
    mentor_data = list(csv.DictReader(f))

with open("2025+ACSC+Participant+Agreement+and+Pre-Survey+(SC25)_October+22,+2025_13.29.csv", encoding="utf-8-sig") as f:
    participant_data = list(csv.DictReader(f))

# Generate plugins with single row
mentor_plugins = generate_plugins(mentor_data, mentor_questions, is_mentor=True, start_pk=230000)
participant_plugins = generate_plugins(participant_data, participant_questions, is_mentor=False, start_pk=230500)

# Save output with consistent names
with open("mentors-2025-generated.json", "w", encoding="utf-8") as f:
    json.dump(mentor_plugins, f, indent=2)

with open("participants-2025-generated.json", "w", encoding="utf-8") as f:
    json.dump(participant_plugins, f, indent=2)

print("✅ Structured Q&A JSON files generated successfully with descriptive image placeholders and consistent naming.")