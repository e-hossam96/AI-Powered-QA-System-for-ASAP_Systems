"""Testing endpoints using requests."""

import requests
from rich import print

base_url = "http://localhost:8000"


# 1. base-request
def base_request():
    response = requests.get(base_url)
    print(response.status_code, response.text)


# 2. data-push-asset
def data_push_asset():
    url = f"{base_url}/data/push/asset"
    files = {"asset": open(r"C:/Users/ehhho/Downloads/papers/gpt2.pdf", "rb")}
    response = requests.post(url, files=files)
    print(response.status_code, response.text)


# 3. data-process-asset
def data_process_asset():
    url = f"{base_url}/data/process/asset"
    payload = {"chunk_size": 2000, "overlap_size": 100, "do_reset": True}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    print(response.status_code, response.text)


# 4. data-process-webpage
def data_process_webpage():
    url = f"{base_url}/data/process/webpage"
    payload = {
        "asset_name_or_url": "https://en.wikipedia.org/wiki/Roman_Empire",
        "chunk_size": 2000,
        "overlap_size": 100,
        "do_reset": False,
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    print(response.status_code, response.text)


# 5. index-push
def index_push():
    url = f"{base_url}/index/push"
    payload = {"do_reset": True}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    print(response.status_code, response.text)


# 6. index-search
def index_search():
    url = f"{base_url}/index/search"
    payload = {"text": "How long did the roman empire rule?", "limit": 4}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    print(response.status_code, response.text)


# 7. rag-query
def rag_query():
    chat_history = [
        {
            "role": "system",
            "content": "You are an assistant to generate a response for the user.\nYou have one helper tool called `search_knowledge_base` that gets documents relevant to the user query.\n\nIf this is the first time the user interacts with you, always use the tool. If a conversation has already start, always analyze the previous messages to decide whether or not to call the tool and whether you should change the user query to make it clearer or not. Most probably you will use the call if this is NOT the first user query. Avoid calling the tool for repeated questions.\n\nThe tool will provide you with a set of docuemnts associated with the user's query. You have to generate a response based on the documents provided. Ignore the documents that are not relevant to the user's query. You have to generate response in the same language as the user's query. You can applogize to the user if you are not able to generate a response.\n\nBe polite and respectful to the user. Be precise and concise in your response and avoid unnecessary information.",
        },
        {"role": "user", "content": "How long did the roman empire rule?"},
        {
            "role": "assistant",
            "tool_calls": [
                {
                    "id": "call_1wfpqqeb",
                    "function": {
                        "arguments": {"text": "how long did the roman empire rule"},
                        "name": "search_knowledge_base",
                    },
                    "type": "function",
                    "index": 0,
                }
            ],
        },
        {
            "role": "tool",
            "content": {
                "text": "How long did the roman empire rule?",
                "relevant_knowledge": "## Document No: 1\n### Content: The Roman Empire was the era of Roman civilisation lasting from 27 BC to 476 AD. Rome ruled the Mediterranean and much of Europe, Western Asia and North Africa. The Romans conquered most of this during the Republic , and it was ruled by emperors following Octavian 's assumption of effective sole rule in 27 BC. The western empire collapsed in 476 AD, but the eastern empire lasted until the fall of Constantinople in 1453. By 100 BC, the city of Rome had expanded its rule to most of the Mediterranean and beyond. However, it was severely destabilised by civil wars and political conflicts , which culminated in the victory of Octavian over Mark Antony and Cleopatra at the Battle of Actium in 31 BC, and the subsequent conquest of the Ptolemaic Kingdom in Egypt. In 27 BC, the Roman Senate granted Octavian overarching military power ( imperium ) and the new title of Augustus , marking his accession as the first Roman emperor . The vast Roman territories were organized into senatorial provinces, governed by proconsuls who were appointed by lot annually, and imperial provinces, which belonged to the emperor but were governed by legates . [ 19 ] The first two centuries of the Empire saw a period of unprecedented stability and prosperity known as the Pax Romana ( lit. ' Roman Peace ' ). Rome reached its greatest territorial extent under Trajan ( r. 98–117 AD ), but a period of increasing trouble and decline began under Commodus ( r. 180–192 ). In the 3rd century, the Empire underwent a 49-year crisis that threatened its existence due to civil war, plagues and barbarian invasions . The Gallic and Palmyrene empires broke away from the state and a series of short-lived emperors led the Empire, which was later reunified under Aurelian ( r. 270–275 ). The civil wars ended with the victory of Diocletian ( r. 284–305 ), who set up two different imperial courts in the Greek East and Latin West . Constantine the Great ( r. 306–337 ), the first Christian emperor , moved the imperial seat\n## Document No: 2\n### Content: The Roman Empire was the era of Roman civilisation lasting from 27 BC to 476 AD. Rome ruled the Mediterranean and much of Europe, Western Asia and North Africa. The Romans conquered most of this during the Republic, and it was ruled by emperors following Octavian's assumption of effective sole rule in 27 BC. The western empire collapsed in 476 AD, but the eastern empire lasted until the fall of Constantinople in 1453. By 100 BC, the city of Rome had expanded its rule to most of the Mediterranean and beyond. However, it was severely destabilised by civil wars and political conflicts, which culminated in the victory of Octavian over Mark Antony and Cleopatra at the Battle of Actium in 31 BC, and the subsequent conquest of the Ptolemaic Kingdom in Egypt. In 27 BC, the Roman Senate granted Octavian overarching military power (imperium) and the new title of Augustus, marking his accession as the first Roman emperor. The vast Roman territories were organized into senatorial provinces, governed by proconsuls who were appointed by lot annually, and imperial provinces, which belonged to the emperor but were governed by legates. The first two centuries of the Empire saw a period of unprecedented stability and prosperity known as the Pax Romana (lit. 'Roman Peace'). Rome reached its greatest territorial extent under Trajan (r. 98–117 AD), but a period of increasing trouble and decline began under Commodus (r. 180–192). In the 3rd century, the Empire underwent a 49-year crisis that threatened its existence due to civil war, plagues and barbarian invasions. The Gallic and Palmyrene empires broke away from the state and a series of short-lived emperors led the Empire, which was later reunified under Aurelian (r. 270–275). The civil wars ended with the victory of Diocletian (r. 284–305), who set up two different imperial courts in the Greek East and Latin West. Constantine the Great (r. 306–337), the first Christian emperor, moved the imperial seat from Rome to Byzantium in 330,\n## Document No: 3\n### Content: Italy was ruled by Odoacer alone. [ 50 ] [ 51 ] [ 53 ] The Eastern Roman Empire, called the Byzantine Empire by later historians, continued until the reign of Constantine XI Palaiologos , the last Roman emperor. He died in battle in 1453 against Mehmed II and his Ottoman forces during the siege of Constantinople . Mehmed II adopted the title of caesar in an attempt to claim a connection to the former Empire. [ 54 ] [ 55 ] His claim was soon recognized by the Patriarchate of Constantinople , but not by most European monarchs. The Roman Empire was one of the largest in history, with contiguous territories throughout Europe, North Africa, and the Middle East. [ 56 ] The Latin phrase imperium sine fine (\"empire without end\" [ 57 ] ) expressed the ideology that neither time nor space limited the Empire. In Virgil 's Aeneid , limitless empire is said to be granted to the Romans by Jupiter . [ 58 ] This claim of universal dominion was renewed when the Empire came under Christian rule in the 4th century. [ h ] In addition to annexing large regions, the Romans directly altered their geography, for example cutting down entire forests . [ 60 ] Roman expansion was mostly accomplished under the Republic , though parts of northern Europe were conquered in the 1st century, when Roman control in Europe, Africa, and Asia was strengthened. Under Augustus , a \"global map of the known world\" was displayed for the first time in public at Rome, coinciding with the creation of the most comprehensive political geography that survives from antiquity, the Geography of Strabo . [ 61 ] When Augustus died, the account of his achievements ( Res Gestae ) prominently featured the geographical cataloguing of the Empire. [ 62 ] Geography alongside meticulous written records were central concerns of Roman Imperial administration . [ 63 ] The Empire reached its largest expanse under Trajan ( r. 98–117 ), [ 64 ] encompassing 5 million km 2 . [ 16 ] [ 17 ] The traditional population estimate of 55–60\n## Document No: 4\n### Content: Eastern Roman Empire, called the Byzantine Empire by later historians, continued until the reign of Constantine XI Palaiologos, the last Roman emperor. He died in battle in 1453 against Mehmed II and his Ottoman forces during the siege of Constantinople. Mehmed II adopted the title of caesar in an attempt to claim a connection to the former Empire. His claim was soon recognized by the Patriarchate of Constantinople, but not by most European monarchs. Geography and demography The Roman Empire was one of the largest in history, with contiguous territories throughout Europe, North Africa, and the Middle East. The Latin phrase imperium sine fine (\"empire without end\") expressed the ideology that neither time nor space limited the Empire. In Virgil's Aeneid, limitless empire is said to be granted to the Romans by Jupiter. This claim of universal dominion was renewed when the Empire came under Christian rule in the 4th century. In addition to annexing large regions, the Romans directly altered their geography, for example cutting down entire forests. Roman expansion was mostly accomplished under the Republic, though parts of northern Europe were conquered in the 1st century, when Roman control in Europe, Africa, and Asia was strengthened. Under Augustus, a \"global map of the known world\" was displayed for the first time in public at Rome, coinciding with the creation of the most comprehensive political geography that survives from antiquity, the Geography of Strabo. When Augustus died, the account of his achievements (Res Gestae) prominently featured the geographical cataloguing of the Empire. Geography alongside meticulous written records were central concerns of Roman Imperial administration. The Empire reached its largest expanse under Trajan (r. 98–117), encompassing 5 million km2. The traditional population estimate of 55–60 million inhabitants accounted for between one-sixth and one-fourth of the world's total population and made it the most populous unified",
            },
            "tool_call_id": "call_1wfpqqeb",
        },
        {
            "role": "assistant",
            "content": "The Roman Empire lasted for approximately 500 years, from 27 BC to 476 AD. It was one of the largest empires in history, covering a vast territory that included Europe, North Africa, and parts of Asia. The empire was ruled by various emperors, including Augustus, Trajan, and Constantine, who played important roles in shaping its expansion and legacy.\n\nThe Roman Empire's territorial reach was at its greatest during the reign of Trajan (98-117 AD), when it encompassed around 5 million square kilometers. The empire's population is estimated to have been between 55-60 million inhabitants, which accounted for approximately one-sixth to one-fourth of the world's total population at that time.\n\nThe Roman Empire was known for its significant contributions to law, architecture, engineering, and governance. Its legacy can still be seen in many modern countries and cities, particularly in Europe and North Africa.\n\nHowever, the empire began to decline in the 3rd century AD due to internal conflicts, external pressures, and economic strain. The Western Roman Empire eventually fell to barbarian invasions in 476 AD, while the Eastern Roman Empire, also known as the Byzantine Empire, survived for another thousand years until its capital, Constantinople, was conquered by the Ottoman Empire in 1453 AD.\n\nOverall, the Roman Empire's impact on world history has been profound and lasting, shaping the course of politics, culture, and society for centuries to come.",
        },
    ]
    if len(chat_history) == 0:
        payload = {"text": "How long did the roman empire rule?", "limit": 4}
    else:
        payload = {
            "text": "what happened?",
            "limit": 4,
            "chat_history": chat_history,
        }

    url = f"{base_url}/rag/query"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    print(response.status_code, response.text)


if __name__ == "__main__":
    base_request()
    data_push_asset()
    data_process_asset()
    data_process_webpage()
    index_push()
    index_search()
    rag_query()
