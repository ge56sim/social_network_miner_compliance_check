import requests

API_URL = "https://api-inference.huggingface.co/models/OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5"
headers = {"Authorization": ""}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


def main():
    output = query({
        "inputs": "Name all activities in the following text: I play cards and my girlfriend cooks."
    })
    # Print result from language model
    print(output)


if __name__ == "__main__":
    main()


"""
"Can you create a json output based on the following instruction and input text given,"
                  " where the for each activity in the text an actor consumer will be provided (the one who is executing the activity. Empty string if not given)"
                  " and an actor receiver is given the one who is addressed by the data produced by the activity."
                  " Sort the json document in chronological order according to the activities which are given in the following text."
                  " The input text is the following:"
                  " A small company manufactures customized bicycles. Whenever the sales department receives an order, a new process instance is created. A member of the sales department can then reject or accept the order for a customized bike. In the former case, the process instance is finished. In the latter case, the storehouse and the engineering department are informed. The storehouse immediately processes the part list of the order and checks the required quantity of each part. If the part is available in-house, it is reserved. If it is not available, it is back-ordered. This procedure is repeated for each item on the part list. In the meantime, the engineering department prepares everything for the assembling of the ordered bicycle. If the storehouse has successfully reserved or back-ordered every item of the part list and the preparation activity has finished, the engineering department assembles the bicycle. Afterwards, the sales department ships the bicycle to the customer and finishes the process instance."
"""