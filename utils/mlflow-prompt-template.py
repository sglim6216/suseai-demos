import mlflow

mlflow.set_tracking_uri("http://192.168.64.11:5000")
# Use double curly braces for variables in the template
initial_template = """\
Summarize content you are provided with in {{ num_sentences }} sentences.

Sentences: {{ sentences }}
"""

# Register a new prompt
prompt = mlflow.register_prompt(
    name="summarization-prompt",
    template=initial_template,
    # Optional: Provide a commit message to describe the changes
    commit_message="New version",
    # Optional: Specify any additional metadata about the prompt version
    version_metadata={
        "author": "alessandro.festa1@suse.com",
    },
    # Optional: Set tags applies to the prompt (across versions)
    tags={
        "task": "summarization",
        "language": "en",
    },
)

# The prompt object contains information about the registered prompt
print(f"Created prompt '{prompt.name}' (version {prompt.version})")

# new_template = """\
# You are an expert summarizer but also a pirate. Condense the following content into exactly {{ num_sentences }} clear and informative sentences that capture the key points.
# Use a pirate joke at the beginning of the answer. Also use bullet points as formatted style in your response.

# Sentences: {{ sentences }}

# Your summary should:
# - Contain exactly {{ num_sentences }} sentences
# - Include only the most important information
# - Be written in a neutral, objective tone
# - Maintain the same level of formality as the original text
# """

# # Register a new version of an existing prompt
# updated_prompt = mlflow.register_prompt(
#     name="summarization-prompt",  # Specify the existing prompt name
#     template=new_template,
#     commit_message="Updated v2 of the summarization",
#     version_metadata={
#         "author": "alessandro.festa1@suse.com",
#     },
# )

# # The prompt object contains information about the registered prompt
# print(f"Created prompt '{updated_prompt.name}' (version {updated_prompt.version})")