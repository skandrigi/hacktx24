import asyncio
import openai
import re


calculate_discount_code = """
def calculate_discount(user, order_total, seasonal_promotion=False):
    \"\"\"Calculate discount based on user membership level and promotions\"\"\"
    # New tiered discount system
    discounts = {
        "bronze": 0.05,
        "silver": 0.10,
        "gold": 0.15,
        "platinum": 0.20
    }
    
    base_discount = discounts.get(user.tier, 0.02)  # Default 2% for non-members
    
    # Volume discount tiers
    if order_total >= 2000:
        volume_discount = 0.10
    elif order_total >= 1000:
        volume_discount = 0.05
    else:
        volume_discount = 0
    
    # Special seasonal promotion
    promo_discount = 0.05 if seasonal_promotion else 0
    
    final_discount = min(base_discount + volume_discount + promo_discount, 0.30)
    return order_total * (1 - final_discount)
"""


async def get_completion(git_conflict):
    conflicts = re.findall(
        r"<<<<<<< HEAD(.*?)=======(.*?)>>>>>>> .*?$", git_conflict, re.DOTALL
    )

    for index, (current_branch, incoming_branch) in enumerate(conflicts):
        print(
            f"Conflict {index + 1}:\nCurrent Branch:\n{current_branch.strip()}\nIncoming Branch:\n{incoming_branch.strip()}\n"
        )

    with open("prompt.txt", "r") as f:
        text = f.read()
        completion = await openai.ChatCompletion.acreate(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a helpful coding tutor. Follow the following format to answer the next question: ",
                },
                {
                    "role": "user",
                    "content": f"{text} Q: Given this following code with a merge conflict:\n {git_conflict} \nWhat would each version do?",
                },
            ],
        )

    return completion.choices[0].message.content


def extract_answer(completion):
    pattern = r"HEAD version:\s*(.*?)(?=\n\n|INCOMING version:|BOTH versions:)|INCOMING version:\s*(.*?)(?=\n\n|BOTH versions:|$)|BOTH versions:\s*(.*?)(?=\n\n|$)"
    matches = re.findall(pattern, completion, re.DOTALL)

    # Flatten the matches and filter out empty strings
    result = tuple(part.strip() for match in matches for part in match if part.strip())
    return result


async def main():
    completion = await get_completion(calculate_discount_code)
    answer = extract_answer(completion)
    print(answer)


if __name__ == "__main__":
    asyncio.run(main())
