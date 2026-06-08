import json

from groq import Groq

from dotenv import load_dotenv

import os


load_dotenv()


client=Groq(

    api_key=os.getenv(

        "GROQ_API_KEY"

    )

)


PROFILE_FILE=(

"outputs/processed/doctor_profiles.json"

)


def load_profiles():

    with open(

        PROFILE_FILE,

        "r",

        encoding="utf-8"

    ) as f:

        return json.load(

            f

        )


def find_profile(

        profiles,

        doctor_name

):

    doctor_name=doctor_name.lower()

    for p in profiles:

        saved_name=(

            p.get(

                "doctor_name",

                ""

            )

            .lower()

        )

        if doctor_name in saved_name:

            return p

    for p in profiles:

        saved_name=(

            p.get(

                "doctor_name",

                ""

            )

            .lower()

        )

        first_last=" ".join(

            saved_name.split()[:2]

        )

        if doctor_name in first_last:

            return p

    return None

def compare_kols(

        doctor1,

        doctor2

):

    profiles=load_profiles()

    p1=find_profile(

        profiles,

        doctor1

    )

    p2=find_profile(

        profiles,

        doctor2

    )

    if p1 is None:

        print(

            "Doctor 1 not found"

        )

        return

    if p2 is None:

        print(

            "Doctor 2 not found"

        )

        return

    prompt=f"""

Compare these two KOLs.

Doctor 1:

{json.dumps(

p1,

indent=2

)}

Doctor 2:

{json.dumps(

p2,

indent=2

)}

Provide:

1. Expertise overlap

2. Key differences

3. Research similarity

4. Influence comparison

5. Short final summary

"""

    response=client.chat.completions.create(

        model=

        "llama-3.3-70b-versatile",

        messages=[

            {

                "role":"user",

                "content":prompt

            }

        ],

        temperature=0.2

    )

    print(

        "\nCOMPARISON:\n"

    )

    print(

        response.choices[0]

        .message.content

    )


if __name__=="__main__":

    compare_kols(

        "Eric Topol",

        "Deepak L. Bhatt"

    )
