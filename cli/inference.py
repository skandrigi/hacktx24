from openai import OpenAI
import re

client = OpenAI()

s = "<<<<<<< HEAD\
this is some content to mess with\
=======\
totally different content to merge later\
>>>>>>> new_branch_to_merge_later"


def get_completion(git_conflict):
    conflicts = re.findall(
        r"<<<<<<< HEAD(.*?)=======(.*?)>>>>>>> .*?$", git_conflict, re.DOTALL
    )

    print(s, conflicts)

    for index, (current_branch, incoming_branch) in enumerate(conflicts):
        print(
            f"Conflict {index + 1}:\nCurrent Branch:\n{current_branch.strip()}\nIncoming Branch:\n{incoming_branch.strip()}\n"
        )


print(get_completion(s))


# completion = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Write a haiku about recursion in programming."},
#     ],
# )
#
# print(completion.choices[0].message)
