import requests


DATASET_ID = "4e54dd6c-30f8-4f86-86a7-3c109a89528e"


def fetch_payments(

        doctor_name

):

    first = doctor_name.split()[0]

    last = doctor_name.split()[-1]

    url=(

f"https://openpaymentsdata.cms.gov/api/1/datastore/query/{DATASET_ID}/0"

    )

    params={

        "physician_first_name":

            first.upper(),

        "physician_last_name":

            last.upper()

    }

    try:

        response=requests.get(

            url,

            params=params,

            timeout=60

        )

        print(

            "Status:",

            response.status_code

        )

        data=response.json()

        rows=data.get(

            "results",

            []

        )

        total=0

        companies=set()

        for row in rows:

            try:

                total += float(

                    row.get(

                        "total_amount_of_payment_usdollars",

                        0

                    )

                )

            except:

                pass

            company=row.get(

                "submitting_applicable_manufacturer_or_applicable_gpo_name"

            )

            if company:

                companies.add(

                    company

                )

        return {

            "payment_count":

                len(rows),

            "total_payment":

                round(

                    total,

                    2

                ),

            "companies":

                list(

                    companies

                )[:10]

        }

    except Exception as e:

        print(e)

        return {

            "payment_count":0,

            "total_payment":0,

            "companies":[]

        }


if __name__=="__main__":

    print(

        fetch_payments(

            "Deepak Bhatt"

        )

    )
